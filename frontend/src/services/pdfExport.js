/**
 * PDF Export Pipeline
 *
 * Simplified, reliable approach:
 * - Uses html2pdf.js with standard margins
 * - NO jsPDF post-processing (which conflicts with html2canvas rendering)
 * - Headers/footers are baked into the HTML report itself
 * - Clean page breaks via CSS
 */

const PDF_CONFIG = {
  margin: [12, 10, 18, 10], // top, right, bottom (extra for footer), left (mm)
  containerWidth: 700,
  scale: 2,
  format: 'a4',
}

/**
 * Build a descriptive filename from diagnosis metadata.
 */
function buildFilename(meta) {
  const date = new Date().toISOString().slice(0, 10)
  const diagnosis = (meta.diagnosis || '').replace(/[^a-zA-Z0-9 ]/g, '').trim().replace(/\s+/g, '-').slice(0, 40)
  const age = meta.patientAge || ''
  const gender = (meta.patientGender || '').charAt(0).toUpperCase()
  const parts = ['MedDiagnose', date]
  if (diagnosis) parts.push(diagnosis)
  if (age && gender) parts.push(`${age}${gender}`)
  return parts.join('_') + '.pdf'
}

/**
 * Add branded headers, footers, disclaimers, and watermarks to every page.
 */
function addPageFooters(pdf, meta) {
  const totalPages = pdf.internal.getNumberOfPages()
  const pageWidth = pdf.internal.pageSize.getWidth()
  const pageHeight = pdf.internal.pageSize.getHeight()
  const date = meta.date || new Date().toLocaleDateString()

  for (let i = 1; i <= totalPages; i++) {
    pdf.setPage(i)

    // ── Top: CONFIDENTIAL + AI-GENERATED badge on every page ──
    pdf.setFontSize(6)
    pdf.setTextColor(203, 213, 225)
    pdf.text('CONFIDENTIAL', 10, 7)

    pdf.setFontSize(5.5)
    pdf.setTextColor(180, 190, 200)
    const aiText = 'AI-GENERATED REPORT — NOT A MEDICAL DIAGNOSIS'
    const aiWidth = pdf.getStringUnitWidth(aiText) * 5.5 / pdf.internal.scaleFactor
    pdf.text(aiText, (pageWidth - aiWidth) / 2, 7)

    pdf.setFontSize(6)
    pdf.setTextColor(203, 213, 225)
    const pageLabel = `${i} / ${totalPages}`
    const plWidth = pdf.getStringUnitWidth(pageLabel) * 6 / pdf.internal.scaleFactor
    pdf.text(pageLabel, pageWidth - 10 - plWidth, 7)

    // ── Bottom footer ──
    // Divider line
    pdf.setDrawColor(226, 232, 240)
    pdf.setLineWidth(0.3)
    pdf.line(10, pageHeight - 16, pageWidth - 10, pageHeight - 16)

    // Left: Brand
    pdf.setFontSize(7)
    pdf.setTextColor(148, 163, 184)
    pdf.text('MedDiagnose AI  |  Clinical Consultation Report', 10, pageHeight - 12)

    // Center: Date
    const dateWidth = pdf.getStringUnitWidth(date) * 7 / pdf.internal.scaleFactor
    pdf.text(date, (pageWidth - dateWidth) / 2, pageHeight - 12)

    // Right: Page
    pdf.setFontSize(7)
    pdf.setTextColor(100, 116, 139)
    const pageText = `Page ${i} of ${totalPages}`
    const textWidth = pdf.getStringUnitWidth(pageText) * 7 / pdf.internal.scaleFactor
    pdf.text(pageText, pageWidth - 10 - textWidth, pageHeight - 12)

    // Disclaimer line at very bottom
    pdf.setFontSize(5.5)
    pdf.setTextColor(180, 190, 200)
    const disclaimer = 'This AI-generated report is for informational purposes only and does not constitute medical advice, diagnosis, or treatment.'
    const discWidth = pdf.getStringUnitWidth(disclaimer) * 5.5 / pdf.internal.scaleFactor
    pdf.text(disclaimer, (pageWidth - discWidth) / 2, pageHeight - 7)
  }
}

/**
 * Generate and trigger PDF download.
 */
export async function downloadPdf(reportHtml, meta = {}) {
  const html2pdf = (await import('html2pdf.js')).default

  const container = document.createElement('div')
  container.style.cssText = `position:fixed;left:-9999px;top:0;width:${PDF_CONFIG.containerWidth}px;opacity:1;pointer-events:none;z-index:-1;overflow:visible;background:#ffffff;`
  container.innerHTML = reportHtml
  document.body.appendChild(container)

  await new Promise(r => setTimeout(r, 300))

  const filename = buildFilename(meta)
  const target = container.firstElementChild || container

  try {
    await html2pdf().set({
      margin: PDF_CONFIG.margin,
      filename,
      image: { type: 'jpeg', quality: 0.95 },
      html2canvas: {
        scale: PDF_CONFIG.scale,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
        windowWidth: PDF_CONFIG.containerWidth,
      },
      jsPDF: { unit: 'mm', format: PDF_CONFIG.format, orientation: 'portrait' },
      pagebreak: { mode: ['css', 'legacy'] },
    }).from(target).toPdf().get('pdf').then((pdfDoc) => {
      addPageFooters(pdfDoc, meta)
    }).save()
  } finally {
    document.body.removeChild(container)
  }
}

/**
 * Generate PDF blob and share via Web Share API (with download fallback).
 */
export async function sharePdf(reportHtml, meta = {}) {
  const html2pdf = (await import('html2pdf.js')).default

  const container = document.createElement('div')
  container.style.cssText = `position:fixed;left:-9999px;top:0;width:${PDF_CONFIG.containerWidth}px;opacity:1;pointer-events:none;z-index:-1;overflow:visible;background:#ffffff;`
  container.innerHTML = reportHtml
  document.body.appendChild(container)

  await new Promise(r => setTimeout(r, 300))

  const filename = buildFilename(meta)
  const target = container.firstElementChild || container

  try {
    const blob = await html2pdf().set({
      margin: PDF_CONFIG.margin,
      filename,
      image: { type: 'jpeg', quality: 0.95 },
      html2canvas: {
        scale: PDF_CONFIG.scale,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
        windowWidth: PDF_CONFIG.containerWidth,
      },
      jsPDF: { unit: 'mm', format: PDF_CONFIG.format, orientation: 'portrait' },
      pagebreak: { mode: ['css', 'legacy'] },
    }).from(target).toPdf().get('pdf').then((pdfDoc) => {
      addPageFooters(pdfDoc, meta)
      return pdfDoc.output('blob')
    })

    const file = new File([blob], filename, { type: 'application/pdf' })

    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      await navigator.share({
        title: `Clinical Report — ${meta.date || new Date().toLocaleDateString()}`,
        files: [file],
      })
    } else {
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      a.click()
      URL.revokeObjectURL(url)
    }
  } finally {
    document.body.removeChild(container)
  }
}

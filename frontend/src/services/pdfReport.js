/**
 * Generates a clean, print-optimized HTML report for PDF export.
 * Branded, structured, and suitable for sharing with healthcare providers.
 */
export function buildPrintReport({
  causes, redFlags, recommendedTests, actionChecklist,
  safetyWarnings, safetyStatusLabel, agentList, totalPipelineTime,
  formatTime, patientAge, patientGender, formattedDate, overallUrgency,
  chiefComplaint, medications, lifestyleRecs, dietaryRecs,
}) {
  const age = patientAge || '—'
  const gender = patientGender || '—'
  const date = formattedDate || new Date().toLocaleDateString()
  const urgency = (overallUrgency || 'routine').toUpperCase()
  const urgencyColor = (urgency === 'URGENT' || urgency === 'EMERGENCY') ? '#dc2626' : urgency === 'SOON' ? '#d97706' : '#059669'
  const urgencyBg = (urgency === 'URGENT' || urgency === 'EMERGENCY') ? '#fef2f2' : urgency === 'SOON' ? '#fffbeb' : '#f0fdf4'

  // ── Header ──
  const headerHtml = `
    <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:3px solid #3b82f6; padding-bottom:16px; margin-bottom:24px;">
      <div>
        <div style="font-size:24px; font-weight:800; color:#1e293b; letter-spacing:-0.5px;">Medical Diagnosis Report</div>
        <div style="font-size:12px; color:#64748b; margin-top:4px;">MedDiagnose AI — Multi-Agent Clinical Analysis</div>
        <div style="font-size:11px; color:#94a3b8; margin-top:2px;">${date}</div>
      </div>
      <div style="text-align:right;">
        <div style="font-size:12px; color:#475569; font-weight:600;">Patient: ${age} y/o ${gender}</div>
        <div style="display:inline-block; background:${urgencyBg}; color:${urgencyColor}; padding:4px 14px; border-radius:20px; font-size:11px; font-weight:700; text-transform:uppercase; margin-top:6px; border:1px solid ${urgencyColor}20;">${urgency}</div>
      </div>
    </div>`

  // ── Chief Complaint ──
  let complaintHtml = ''
  if (chiefComplaint) {
    complaintHtml = `
    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-left:4px solid #3b82f6; border-radius:8px; padding:14px 16px; margin-bottom:20px; page-break-inside:avoid;">
      <div style="font-size:10px; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">Chief Complaint</div>
      <div style="font-size:13px; color:#334155; line-height:1.5;">${chiefComplaint}</div>
    </div>`
  }

  // ── Diagnoses ──
  let diagnosesHtml = ''
  for (let i = 0; i < causes.length; i++) {
    const c = causes[i]
    const urgC = (c.urgency === 'urgent' || c.urgency === 'emergency') ? '#dc2626' : '#16a34a'
    const urgBg2 = (c.urgency === 'urgent' || c.urgency === 'emergency') ? '#fef2f2' : '#f0fdf4'
    const confColor = c.value >= 70 ? '#059669' : c.value >= 40 ? '#d97706' : '#64748b'
    const barWidth = Math.max(c.value, 3)
    const barColor = c.value >= 70 ? '#10b981' : c.value >= 40 ? '#f59e0b' : '#94a3b8'

    diagnosesHtml += `
    <div style="border:1px solid #e2e8f0; border-radius:10px; padding:14px 16px; margin-bottom:10px; page-break-inside:avoid;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <div style="flex:1;">
          <span style="font-weight:700; color:#1e293b; font-size:13px;">${c.cause}</span>
          <span style="background:${urgBg2}; color:${urgC}; padding:2px 10px; border-radius:12px; font-size:9px; font-weight:700; text-transform:uppercase; margin-left:8px;">${c.urgency}</span>
        </div>
        <span style="font-size:22px; font-weight:800; color:${confColor};">${c.value}%</span>
      </div>
      <div style="background:#f1f5f9; border-radius:4px; height:6px; margin-bottom:8px; overflow:hidden;">
        <div style="background:${barColor}; height:100%; border-radius:4px; width:${barWidth}%;"></div>
      </div>
      <div style="font-size:10px; color:#6366f1; font-weight:600; margin-bottom:4px;">${c.specialty || ''}</div>
      <div style="font-size:11px; color:#64748b; line-height:1.6;">${c.explanation || ''}</div>
    </div>`
  }

  // ── Red Flags ──
  let redFlagsHtml = ''
  if (redFlags && redFlags.length > 0) {
    redFlagsHtml = `
    <div style="background:#fef2f2; border:1px solid #fecaca; border-left:4px solid #dc2626; border-radius:8px; padding:14px 16px; margin-bottom:20px; page-break-inside:avoid;">
      <div style="font-weight:700; color:#dc2626; font-size:12px; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">⚠ Warning Signs Detected</div>
      ${redFlags.map(f => `<div style="font-size:11px; color:#991b1b; margin-bottom:4px; padding-left:8px;">• ${f}</div>`).join('')}
    </div>`
  }

  // ── Recommended Tests ──
  let testsHtml = ''
  if (recommendedTests && recommendedTests.length > 0) {
    testsHtml = `
    <div style="margin-bottom:20px; page-break-inside:avoid;">
      <div style="font-weight:700; color:#1e293b; font-size:13px; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px; border-bottom:1px solid #e2e8f0; padding-bottom:6px;">Recommended Tests</div>
      ${recommendedTests.map((t, i) => `<div style="font-size:11px; color:#475569; margin-bottom:5px; padding-left:4px; line-height:1.5;">☐ ${t}</div>`).join('')}
    </div>`
  }

  // ── Action Items ──
  let actionsHtml = ''
  if (actionChecklist && actionChecklist.length > 0) {
    actionsHtml = `
    <div style="margin-bottom:20px; page-break-inside:avoid;">
      <div style="font-weight:700; color:#1e293b; font-size:13px; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px; border-bottom:1px solid #e2e8f0; padding-bottom:6px;">Action Items</div>
      ${actionChecklist.map(a => {
        const text = typeof a === 'string' ? a : (a.action || JSON.stringify(a))
        return `<div style="font-size:11px; color:#475569; margin-bottom:5px; padding-left:4px; line-height:1.5;">☐ ${text}</div>`
      }).join('')}
    </div>`
  }

  // ── Treatment Plan ──
  let treatmentHtml = ''
  if ((medications && medications.length > 0) || (lifestyleRecs && lifestyleRecs.length > 0)) {
    treatmentHtml = `<div style="margin-bottom:20px; page-break-inside:avoid;">
      <div style="font-weight:700; color:#1e293b; font-size:13px; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px; border-bottom:1px solid #e2e8f0; padding-bottom:6px;">Treatment Recommendations</div>`
    if (medications && medications.length > 0) {
      treatmentHtml += `<div style="font-size:10px; color:#3b82f6; font-weight:700; text-transform:uppercase; margin-bottom:6px;">Medications</div>`
      medications.forEach(med => {
        const name = typeof med === 'string' ? med : med.name
        const dose = med.dose || ''
        const warn = med.warnings || ''
        treatmentHtml += `<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 12px; margin-bottom:6px;">
          <div style="font-size:12px; font-weight:600; color:#1e293b;">${name}</div>
          ${dose ? `<div style="font-size:10px; color:#64748b; margin-top:2px;">${dose}${med.frequency ? ' — ' + med.frequency : ''}</div>` : ''}
          ${warn ? `<div style="font-size:10px; color:#d97706; margin-top:2px;">⚠ ${warn}</div>` : ''}
        </div>`
      })
    }
    if (lifestyleRecs && lifestyleRecs.length > 0) {
      treatmentHtml += `<div style="font-size:10px; color:#059669; font-weight:700; text-transform:uppercase; margin-top:12px; margin-bottom:6px;">Lifestyle Recommendations</div>`
      lifestyleRecs.forEach(rec => {
        treatmentHtml += `<div style="font-size:11px; color:#475569; margin-bottom:4px; padding-left:4px;">✓ ${rec}</div>`
      })
    }
    treatmentHtml += `</div>`
  }

  // ── Safety Review ──
  let safetyHtml = ''
  if (safetyWarnings && safetyWarnings.length > 0) {
    const safetyColor = safetyStatusLabel === 'FAIL' ? '#dc2626' : safetyStatusLabel === 'CAUTION' ? '#d97706' : '#059669'
    safetyHtml = `
    <div style="background:#fffbeb; border:1px solid #fde68a; border-left:4px solid ${safetyColor}; border-radius:8px; padding:14px 16px; margin-bottom:20px; page-break-inside:avoid;">
      <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
        <span style="font-weight:700; color:${safetyColor}; font-size:12px; text-transform:uppercase;">Safety Review</span>
        <span style="background:${safetyColor}15; color:${safetyColor}; padding:2px 10px; border-radius:12px; font-size:10px; font-weight:700;">${safetyStatusLabel}</span>
      </div>
      ${safetyWarnings.map(w => `<div style="font-size:11px; color:#92400e; margin-bottom:4px;">⚠ ${w}</div>`).join('')}
    </div>`
  }

  // ── Agent Performance ──
  let agentHtml = `
  <div style="margin-bottom:20px; page-break-inside:avoid;">
    <div style="font-weight:700; color:#1e293b; font-size:13px; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px; border-bottom:1px solid #e2e8f0; padding-bottom:6px;">Agent Performance</div>
    <table style="width:100%; font-size:11px; border-collapse:collapse;">`
  if (agentList) {
    agentList.forEach(agent => {
      agentHtml += `<tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:5px 0; color:#475569;">${agent.name}</td>
        <td style="padding:5px 0; text-align:right; color:#1e293b; font-weight:600; font-family:monospace;">${agent.timeStr}</td>
      </tr>`
    })
  }
  agentHtml += `<tr style="border-top:2px solid #e2e8f0;">
    <td style="padding:8px 0; color:#1e293b; font-weight:700;">Total Pipeline</td>
    <td style="padding:8px 0; text-align:right; color:#1e293b; font-weight:700; font-family:monospace;">${formatTime ? formatTime(totalPipelineTime) : (totalPipelineTime || 0).toFixed(1) + 's'}</td>
  </tr></table></div>`

  // ── Assemble Full Report ──
  return `
  <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width:720px; margin:0 auto; padding:24px 28px; color:#1e293b; background:#ffffff;">
    ${headerHtml}
    ${complaintHtml}
    ${redFlagsHtml}
    <div style="margin-bottom:20px;">
      <div style="font-weight:700; color:#1e293b; font-size:14px; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:12px; border-bottom:1px solid #e2e8f0; padding-bottom:6px;">Differential Diagnoses</div>
      ${diagnosesHtml}
    </div>
    ${testsHtml}
    ${actionsHtml}
    ${treatmentHtml}
    ${safetyHtml}
    ${agentHtml}
    <div style="margin-top:28px; padding-top:14px; border-top:2px solid #e2e8f0; text-align:center;">
      <div style="font-size:9px; color:#94a3b8; line-height:1.6; max-width:500px; margin:0 auto;">
        This report is generated by MedDiagnose AI for informational purposes only. It does not constitute medical advice, diagnosis, or treatment.
        Always consult a qualified healthcare professional for medical decisions. In emergencies, call local emergency services immediately.
      </div>
      <div style="font-size:8px; color:#cbd5e1; margin-top:8px;">Generated by MedDiagnose AI — Multi-Agent Clinical Analysis Platform</div>
    </div>
  </div>`
}

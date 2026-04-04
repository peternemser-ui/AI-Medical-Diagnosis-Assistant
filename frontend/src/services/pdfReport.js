/**
 * PDF Report Generator -- Clinical Consultation Report
 *
 * Returns a single HTML string for html2pdf.js rendering.
 * Information architecture: Cover, Executive Summary, Top Actions,
 * Differentials, Tests, Safety, Treatment, then Appendices A-D.
 */
export function buildPrintReport({
  causes, redFlags, recommendedTests, actionChecklist,
  safetyWarnings, safetyStatusLabel, agentList, totalPipelineTime,
  formatTime, patientAge, patientGender, formattedDate, overallUrgency,
  chiefComplaint, medications, lifestyleRecs, dietaryRecs,
  patientSummary, bodySystems, warningSignsData,
  tcmRecommendations, ayurvedicRecommendations, holisticRecommendations,
  chatTranscript, estimatedCost, tokenUsage,
  specialistDoctor, specialistSpecialty,
}) {
  // -- Sanitization --------------------------------------------------------
  const sanitize = (text) => {
    if (!text) return ''
    if (typeof text === 'object') {
      return text.title || text.message || text.issue || text.description
        || text.text || text.name || text.feature || text.action
        || text.recommendation || JSON.stringify(text)
    }
    let s = String(text)
    if (s.startsWith('{') && s.includes("':")) {
      for (const key of ['feature','title','name','message','issue','test','action','recommendation']) {
        const match = s.match(new RegExp(`'${key}':\\s*'([^']*(?:''[^']*)*)'`))
        if (match) {
          let extracted = match[1].replace(/''/g, "'")
          const detailMatch = s.match(/'(?:diagnostic_impact|detail|description|reasoning)':\s*'([^']*(?:''[^']*)*)'/)
          if (detailMatch) extracted += ' -- ' + detailMatch[1].replace(/''/g, "'")
          return extracted
        }
      }
      try {
        const jsonStr = s.replace(/'/g, '"').replace(/True/g, 'true').replace(/False/g, 'false').replace(/None/g, 'null')
        const obj = JSON.parse(jsonStr)
        s = obj.title || obj.issue || obj.name || obj.feature || JSON.stringify(obj)
      } catch { /* use raw string */ }
    }
    return s.replace(/\u2014/g, '--').replace(/\u2013/g, '-').replace(/\u2018|\u2019/g, "'")
      .replace(/\u201C|\u201D/g, '"').replace(/\u2022/g, '*').replace(/\u2026/g, '...')
      .replace(/\u2192/g, '->').replace(/\u2190/g, '<-').replace(/\u00A0/g, ' ')
      .replace(/[\u0080-\u009F]/g, '').replace(/\uFFFD/g, '--')
  }
  const san = sanitize
  const sanArr = (arr) => Array.isArray(arr) ? arr.map(i => san(i)).filter(Boolean) : []
  const toSentence = (s) => { const t = san(s); return t ? t.charAt(0).toUpperCase() + t.slice(1).toLowerCase() : '' }

  // -- Constants -----------------------------------------------------------
  const font = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
  const date = formattedDate || new Date().toLocaleDateString()
  const age = patientAge || '--'
  const gender = patientGender || '--'
  const urgency = (overallUrgency || 'routine').toUpperCase()
  const urgMap = { EMERGENCY: '#dc2626', URGENT: '#dc2626', SOON: '#f59e0b' }
  const urgBgMap = { EMERGENCY: '#fef2f2', URGENT: '#fef2f2', SOON: '#fffbeb' }
  const uColor = urgMap[urgency] || '#10b981'
  const uBg = urgBgMap[urgency] || '#ecfdf5'
  const cleanFlags = sanArr(redFlags)
  const cleanWarnings = sanArr(safetyWarnings)
  const topCauses = (causes || []).slice(0, 5)
  const top = topCauses[0] || null

  // -- Style tokens --------------------------------------------------------
  const avoid = 'page-break-inside:avoid;break-inside:avoid;'
  const keepWithNext = 'page-break-after:avoid;break-after:avoid;'
  const forceBreak = 'page-break-before:always;break-before:page;'

  const badge = (text, bg, color) =>
    `<span style="display:inline-block;background:${bg};color:${color};padding:2px 8px;border-radius:12px;font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;">${text}</span>`

  // Heading with anchor content — wraps heading + a preview of content in one
  // unbreakable block so the heading is NEVER orphaned at page bottom.
  // html2pdf.js ignores page-break-after:avoid, so we use a physical wrapper.
  // Heading wrapped with min-height so html2pdf.js pushes it to next page
  // if less than ~80px remains at the bottom of current page
  const heading = (title, accent) =>
    `<div style="margin-top:20px;min-height:60px;${avoid}"><table style="width:100%;border-collapse:collapse;margin-bottom:10px;"><tr>
      <td style="width:4px;"><div style="width:4px;height:16px;border-radius:2px;background:${accent};"></div></td>
      <td style="font-size:13px;font-weight:700;color:#0f172a;text-transform:uppercase;letter-spacing:1px;padding-left:8px;">${title}</td>
    </tr></table></div>`

  const card = (content, opts = {}) => {
    const bg = opts.bg || '#f8fafc'
    const border = opts.border || '#e2e8f0'
    const leftBar = opts.leftBar ? `border-left:4px solid ${opts.leftBar};` : ''
    return `<div style="background:${bg};border:1px solid ${border};border-radius:8px;padding:12px;margin-bottom:8px;${avoid}${leftBar}">${content}</div>`
  }

  // -- 1. COVER / HEADER ---------------------------------------------------
  const headerHtml = `
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:8px;padding:20px 24px;margin-bottom:20px;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#3b82f6,#8b5cf6,#ec4899);"></div>
      <table style="width:100%;border-collapse:collapse;"><tr>
        <td style="vertical-align:middle;">
          <div style="font-size:18px;font-weight:900;color:#ffffff;margin-bottom:2px;">MedDiagnose AI</div>
          <div style="font-size:9px;color:#94a3b8;letter-spacing:1px;text-transform:uppercase;">Clinical Consultation Report</div>
        </td>
        <td style="text-align:right;vertical-align:middle;">
          <div style="font-size:12px;color:#e2e8f0;font-weight:600;margin-bottom:4px;">${date}</div>
          <div style="font-size:10px;color:#cbd5e1;">Patient: ${age} y/o ${gender}</div>
          <div style="margin-top:6px;">${badge(urgency, uBg, uColor)}</div>
        </td>
      </tr></table>
      ${chiefComplaint ? `<div style="margin-top:12px;padding-top:10px;border-top:1px solid #334155;">
        <div style="font-size:8px;color:#64748b;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px;">Chief Complaint</div>
        <div style="font-size:11px;color:#e2e8f0;line-height:1.5;max-width:500px;">${san(chiefComplaint)}</div>
      </div>` : ''}
      ${specialistDoctor ? `<div style="margin-top:10px;padding-top:8px;border-top:1px solid #334155;">
        <div style="font-size:8px;color:#64748b;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px;">Specialist Consultation</div>
        <div style="font-size:11px;color:#e2e8f0;">${san(specialistDoctor)} — <span style="color:${specialistSpecialty === 'cardiology' ? '#ef4444' : specialistSpecialty === 'dermatology' ? '#f43f5e' : specialistSpecialty === 'neurology' ? '#a855f7' : '#3b82f6'}">${san((specialistSpecialty || '').replace(/_/g, ' '))}</span></div>
      </div>` : ''}
    </div>`

  // -- 2. EXECUTIVE SUMMARY ------------------------------------------------
  let summaryHtml = ''
  if (top) {
    const conf = top.value || 0
    const cColor = conf >= 70 ? '#10b981' : conf >= 40 ? '#f59e0b' : '#64748b'
    const cBg = conf >= 70 ? '#ecfdf5' : conf >= 40 ? '#fffbeb' : '#f8fafc'
    const summaryText = san(top.explanation || patientSummary || '')
    summaryHtml = heading('Executive Summary', '#3b82f6') + card(`
      <table style="width:100%;border-collapse:collapse;"><tr style="vertical-align:top;">
        <td style="width:76px;padding-right:16px;">
          <div style="width:68px;height:68px;border-radius:50%;background:${cBg};border:3px solid ${cColor};text-align:center;padding-top:14px;">
            <div style="font-size:22px;font-weight:900;color:${cColor};line-height:1;">${conf}%</div>
            <div style="font-size:7px;font-weight:700;color:${cColor};text-transform:uppercase;">confidence</div>
          </div>
        </td>
        <td>
          <div style="font-size:9px;font-weight:700;color:#3b82f6;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Primary Diagnosis</div>
          <div style="font-size:16px;font-weight:800;color:#0f172a;line-height:1.3;margin-bottom:2px;">${san(top.cause)}</div>
          <div style="font-size:10px;color:#64748b;font-weight:600;margin-bottom:8px;">${top.specialty || 'General Medicine'}</div>
          ${summaryText ? `<div style="font-size:11px;color:#334155;line-height:1.6;max-width:500px;">${summaryText}</div>` : ''}
          ${cleanFlags.length ? `<div style="margin-top:8px;">${badge(cleanFlags.length + ' red flag' + (cleanFlags.length > 1 ? 's' : ''), '#fef2f2', '#dc2626')}</div>` : ''}
        </td>
      </tr></table>`, { bg: '#f0f9ff', border: '#bae6fd' })
  }

  // -- 3. TOP 3 ACTIONS ----------------------------------------------------
  let actionsHtml = ''
  if (actionChecklist && actionChecklist.length > 0) {
    const cleanActions = sanArr(actionChecklist).slice(0, 5)
    const categorize = (text) => {
      const t = text.toLowerCase()
      if (t.includes('right now') || t.includes('immediately') || t.includes('emergency') || t.includes('urgent'))
        return { label: 'RIGHT NOW', color: '#dc2626', bg: '#fef2f2', border: '#fecaca' }
      if (t.includes('this week') || t.includes('soon') || t.includes('schedule'))
        return { label: 'THIS WEEK', color: '#f59e0b', bg: '#fffbeb', border: '#fde68a' }
      return { label: 'ONGOING', color: '#10b981', bg: '#ecfdf5', border: '#a7f3d0' }
    }
    const items = cleanActions.map((text, i) => {
      const cat = categorize(text)
      return `<div style="padding:8px 12px;background:${cat.bg};border:1px solid ${cat.border};border-radius:8px;margin-bottom:6px;${avoid}">
        <table style="width:100%;border-collapse:collapse;"><tr style="vertical-align:top;">
          <td style="width:24px;">
            <div style="width:20px;height:20px;border-radius:50%;background:${cat.color};color:#fff;text-align:center;line-height:20px;font-size:9px;font-weight:800;">${i + 1}</div>
          </td>
          <td style="padding-left:8px;">
            <div style="font-size:7px;font-weight:700;color:${cat.color};text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">${cat.label}</div>
            <div style="font-size:10px;color:#1e293b;line-height:1.5;max-width:500px;">${text}</div>
          </td>
        </tr></table>
      </div>`
    }).join('')
    actionsHtml = heading('Top Actions', '#f59e0b') + card(items, { bg: '#ffffff' })
  }

  // -- 4. DIFFERENTIAL DIAGNOSES -------------------------------------------
  let diffHtml = ''
  if (topCauses.length > 0) {
    const cards = topCauses.map((c, i) => {
      const v = c.value || 0
      const barColor = v >= 70 ? '#10b981' : v >= 40 ? '#f59e0b' : '#94a3b8'
      const urgLabel = c.urgency || 'routine'
      const urgC = (urgLabel === 'urgent' || urgLabel === 'emergency') ? '#dc2626' : urgLabel === 'soon' ? '#f59e0b' : '#10b981'
      const urgBg2 = (urgLabel === 'urgent' || urgLabel === 'emergency') ? '#fef2f2' : urgLabel === 'soon' ? '#fffbeb' : '#ecfdf5'

      let detail = ''
      if (i === 0) {
        const feats = c.supporting_features || c.supportingFeatures || []
        const opp = c.opposing_features || c.opposingFeatures || []
        if (c.explanation) detail += `<div style="font-size:10px;color:#475569;line-height:1.6;margin-top:6px;max-width:500px;">${san(c.explanation)}</div>`
        if (feats.length) detail += `<div style="margin-top:6px;font-size:9px;font-weight:700;color:#10b981;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:3px;">Supporting</div>` +
          feats.slice(0, 4).map(f => `<div style="font-size:10px;color:#475569;padding-left:12px;line-height:1.4;margin-bottom:2px;position:relative;"><span style="position:absolute;left:0;color:#10b981;font-weight:700;">+</span>${san(f)}</div>`).join('')
        if (opp.length) detail += `<div style="margin-top:4px;font-size:9px;font-weight:700;color:#f59e0b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:3px;">Against</div>` +
          opp.slice(0, 3).map(f => `<div style="font-size:10px;color:#78716c;padding-left:12px;line-height:1.4;margin-bottom:2px;position:relative;"><span style="position:absolute;left:0;color:#f59e0b;">-</span>${san(f)}</div>`).join('')
      } else {
        if (c.explanation) detail += `<div style="font-size:10px;color:#64748b;line-height:1.5;margin-top:4px;max-width:500px;">${san(c.explanation)}</div>`
      }

      return `<div style="border:1px solid ${i === 0 ? '#bfdbfe' : '#e2e8f0'};border-radius:8px;padding:10px 14px;margin-bottom:6px;background:${i === 0 ? '#f8faff' : '#ffffff'};${avoid}">
        <table style="width:100%;border-collapse:collapse;"><tr style="vertical-align:middle;">
          <td>
            ${i === 0 ? `<span style="font-size:7px;font-weight:700;color:#3b82f6;background:#eff6ff;padding:1px 6px;border-radius:8px;text-transform:uppercase;">Most Likely</span> ` : ''}
            <span style="font-size:${i === 0 ? '14' : '12'}px;font-weight:700;color:#0f172a;">${san(c.cause)}</span>
          </td>
          <td style="width:55px;text-align:right;">
            <div style="font-size:18px;font-weight:900;color:${barColor};line-height:1;">${v}%</div>
          </td>
        </tr></table>
        <table style="width:100%;border-collapse:collapse;margin-top:4px;"><tr style="vertical-align:middle;">
          <td><div style="background:#f1f5f9;border-radius:4px;height:4px;overflow:hidden;"><div style="background:${barColor};height:100%;border-radius:4px;width:${Math.max(v, 3)}%;"></div></div></td>
        </tr></table>
        <div style="margin-top:4px;">${badge(urgLabel, urgBg2, urgC)} <span style="font-size:9px;color:#6366f1;font-weight:600;margin-left:4px;">${c.specialty || ''}</span></div>
        ${detail}
      </div>`
    }).join('')
    diffHtml = heading('Differential Diagnoses', '#6366f1') + cards
  }

  // -- 5. PRIORITY TESTS ---------------------------------------------------
  let testsHtml = ''
  if (recommendedTests && recommendedTests.length > 0) {
    const all = sanArr(recommendedTests)
    const top5 = all.slice(0, 5)
    const rest = all.slice(5)
    const topItems = top5.map((t, i) =>
      `<div style="padding:6px 10px;background:${i % 2 === 0 ? '#eff6ff' : '#f8fafc'};border-radius:6px;border:1px solid #e0e7ff;margin-bottom:4px;${avoid}">
        <table style="width:100%;border-collapse:collapse;"><tr style="vertical-align:top;">
          <td style="width:20px;"><div style="width:16px;height:16px;border:2px solid #3b82f6;border-radius:3px;text-align:center;line-height:14px;font-size:8px;font-weight:800;color:#3b82f6;">${i + 1}</div></td>
          <td style="padding-left:8px;font-size:10px;color:#1e293b;line-height:1.5;font-weight:500;max-width:500px;">${t}</td>
        </tr></table>
      </div>`).join('')
    let restHtml = ''
    if (rest.length > 0) {
      restHtml = `<div style="margin-top:8px;font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Additional Tests</div>` +
        rest.map(t => `<div style="font-size:10px;color:#475569;padding-left:14px;line-height:1.5;margin-bottom:2px;position:relative;"><span style="position:absolute;left:2px;color:#94a3b8;">&bull;</span>${t}</div>`).join('')
    }
    testsHtml = heading('Priority Tests', '#0ea5e9') +
      card(`<div style="font-size:9px;color:#64748b;margin-bottom:8px;">Top 5 of ${all.length} recommended</div>${topItems}${restHtml}`, { bg: '#ffffff', border: '#bae6fd' })
  }

  // -- 6. SAFETY REVIEW ----------------------------------------------------
  const safetyLabel = safetyStatusLabel || 'PASS'
  const safetyColor = safetyLabel === 'FAIL' ? '#dc2626' : safetyLabel === 'CAUTION' ? '#f59e0b' : '#10b981'
  const safetyBg = safetyLabel === 'FAIL' ? '#fef2f2' : safetyLabel === 'CAUTION' ? '#fffbeb' : '#ecfdf5'
  let safetyContent = `<div style="margin-bottom:8px;">${badge(safetyLabel, safetyBg, safetyColor)}</div>`

  if (cleanWarnings.length > 0) {
    safetyContent += cleanWarnings.map(w => {
      const sev = w.toLowerCase()
      let sevLabel = 'Monitor', sevColor = '#f59e0b', sevBg = '#fffbeb'
      if (sev.includes('critical') || sev.includes('danger') || sev.includes('emergency')) { sevLabel = 'Critical'; sevColor = '#dc2626'; sevBg = '#fef2f2' }
      else if (sev.includes('important') || sev.includes('warning') || sev.includes('caution')) { sevLabel = 'Important'; sevColor = '#f59e0b'; sevBg = '#fffbeb' }
      return `<div style="padding:8px 12px;border-left:3px solid ${sevColor};background:${sevBg};border-radius:0 6px 6px 0;margin-bottom:6px;${avoid}">
        <table style="width:100%;border-collapse:collapse;"><tr style="vertical-align:top;">
          <td><div style="font-size:10px;font-weight:700;color:#0f172a;line-height:1.4;max-width:500px;">${w}</div></td>
          <td style="width:60px;text-align:right;">${badge(sevLabel, sevBg, sevColor)}</td>
        </tr></table>
      </div>`
    }).join('')
  } else if (cleanFlags.length === 0) {
    safetyContent += `<div style="font-size:10px;color:#10b981;padding:8px 12px;background:#ecfdf5;border-radius:6px;">No safety concerns identified. All checks passed.</div>`
  }

  if (cleanFlags.length > 0) {
    safetyContent += `<div style="font-size:9px;font-weight:700;color:#dc2626;text-transform:uppercase;letter-spacing:0.5px;margin:10px 0 4px 0;">Red Flags</div>`
    safetyContent += cleanFlags.map(f =>
      `<div style="font-size:10px;color:#7f1d1d;margin-bottom:3px;padding:4px 8px;background:#fef2f2;border-radius:4px;border-left:2px solid #dc2626;line-height:1.4;max-width:500px;">${f}</div>`).join('')
  }
  const safetyHtml = heading('Safety Review', '#dc2626') + card(safetyContent, { bg: '#ffffff' })

  // -- 7. TREATMENT OVERVIEW -----------------------------------------------
  let treatmentHtml = ''
  let hasTreatment = false
  let treatContent = ''

  if (medications && medications.length > 0) {
    hasTreatment = true
    treatContent += `<div style="font-size:9px;font-weight:700;color:#3b82f6;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">Medications</div>`
    medications.forEach(med => {
      const name = typeof med === 'string' ? med : (med.name || '')
      const purpose = typeof med === 'string' ? '' : (med.purpose || med.dose || '')
      const warn = typeof med === 'string' ? '' : (med.warnings || med.warning || '')
      treatContent += card(`
        <div style="font-size:11px;font-weight:700;color:#0f172a;">${san(name)}</div>
        ${purpose ? `<div style="font-size:10px;color:#475569;margin-top:2px;">${san(purpose)}${med.frequency ? ' -- ' + san(med.frequency) : ''}</div>` : ''}
        ${warn ? `<div style="font-size:9px;color:#dc2626;margin-top:3px;font-weight:600;padding:3px 6px;background:#fef2f2;border-radius:4px;">Warning: ${san(warn)}</div>` : ''}
      `, { bg: '#f0fdf4', border: '#dcfce7' })
    })
  }

  if (lifestyleRecs && lifestyleRecs.length > 0) {
    hasTreatment = true
    treatContent += `<div style="font-size:9px;font-weight:700;color:#10b981;text-transform:uppercase;letter-spacing:0.5px;margin-top:10px;margin-bottom:6px;">Lifestyle</div>`
    treatContent += sanArr(lifestyleRecs).map(r =>
      `<div style="font-size:10px;color:#334155;margin-bottom:3px;padding-left:14px;line-height:1.5;position:relative;max-width:500px;"><span style="position:absolute;left:2px;color:#10b981;font-weight:700;">&bull;</span>${r}</div>`).join('')
  }

  if (dietaryRecs && dietaryRecs.length > 0) {
    hasTreatment = true
    treatContent += `<div style="font-size:9px;font-weight:700;color:#65a30d;text-transform:uppercase;letter-spacing:0.5px;margin-top:10px;margin-bottom:6px;">Dietary Guidance</div>`
    treatContent += sanArr(dietaryRecs).map(r =>
      `<div style="font-size:10px;color:#334155;margin-bottom:3px;padding-left:14px;line-height:1.5;position:relative;max-width:500px;"><span style="position:absolute;left:2px;color:#65a30d;font-weight:700;">&bull;</span>${r}</div>`).join('')
  }

  if (warningSignsData && warningSignsData.length > 0) {
    hasTreatment = true
    treatContent += `<div style="font-size:9px;font-weight:700;color:#dc2626;text-transform:uppercase;letter-spacing:0.5px;margin-top:10px;margin-bottom:6px;">Seek Immediate Care If</div>`
    warningSignsData.forEach(sign => {
      treatContent += `<div style="font-size:10px;color:#7f1d1d;margin-bottom:3px;padding:4px 8px;background:#fef2f2;border-radius:4px;border-left:2px solid #dc2626;line-height:1.4;max-width:500px;">${san(sign)}</div>`
    })
  }

  if (!hasTreatment) treatContent = `<div style="font-size:10px;color:#94a3b8;font-style:italic;">Treatment details will appear after a complete diagnosis.</div>`
  treatmentHtml = heading('Treatment Overview', '#10b981') + card(treatContent, { bg: '#ffffff' })

  // ========================================================================
  // APPENDICES
  // ========================================================================

  // -- Appendix A: Detailed Clinical Reasoning -----------------------------
  let appendixA = ''
  if (causes && causes.length > 0) {
    let content = ''
    causes.forEach((c, i) => {
      const feats = c.supporting_features || c.supportingFeatures || []
      const opp = c.opposing_features || c.opposingFeatures || []
      if (!c.explanation && feats.length === 0 && opp.length === 0) return
      content += `<div style="margin-bottom:12px;padding:8px 12px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;${avoid}">
        <div style="font-size:11px;font-weight:700;color:#0f172a;margin-bottom:4px;">${i + 1}. ${san(c.cause)} (${c.value}%)</div>
        ${c.explanation ? `<div style="font-size:10px;color:#475569;line-height:1.6;margin-bottom:6px;max-width:500px;">${san(c.explanation)}</div>` : ''}
        ${feats.length ? `<div style="font-size:9px;font-weight:700;color:#10b981;margin-bottom:3px;">Supporting Features</div>` +
          feats.map(f => `<div style="font-size:10px;color:#475569;padding-left:12px;line-height:1.4;margin-bottom:2px;position:relative;"><span style="position:absolute;left:0;color:#10b981;font-weight:700;">+</span>${san(f)}</div>`).join('') : ''}
        ${opp.length ? `<div style="font-size:9px;font-weight:700;color:#f59e0b;margin-top:4px;margin-bottom:3px;">Opposing Features</div>` +
          opp.map(f => `<div style="font-size:10px;color:#78716c;padding-left:12px;line-height:1.4;margin-bottom:2px;position:relative;"><span style="position:absolute;left:0;color:#f59e0b;">-</span>${san(f)}</div>`).join('') : ''}
      </div>`
    })
    if (content) {
      appendixA = `<div style="${forceBreak}">${heading('Appendix A: Detailed Clinical Reasoning', '#6366f1')}${content}</div>`
    }
  }

  // -- Appendix B: Full Test Rationale -------------------------------------
  let appendixB = ''
  if (recommendedTests && recommendedTests.length > 0) {
    const all = sanArr(recommendedTests)
    const rows = all.map((t, i) =>
      `<tr><td style="padding:5px 8px;font-size:10px;color:#334155;border-bottom:1px solid #f1f5f9;vertical-align:top;width:20px;font-weight:700;color:#64748b;">${i + 1}</td>
       <td style="padding:5px 8px;font-size:10px;color:#1e293b;border-bottom:1px solid #f1f5f9;line-height:1.5;">${t}</td></tr>`).join('')
    appendixB = `<div style="${forceBreak}">${heading('Appendix B: Full Test Rationale', '#0ea5e9')}
      <table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:6px;">${rows}</table></div>`
  }

  // -- Appendix C: Conversation Summary ------------------------------------
  let appendixC = ''
  const intakeParts = []
  if (chiefComplaint) intakeParts.push(`<div style="font-size:9px;font-weight:700;color:#64748b;text-transform:uppercase;margin-bottom:3px;">Chief Complaint</div><div style="font-size:10px;color:#1e293b;line-height:1.5;margin-bottom:8px;max-width:500px;">${san(chiefComplaint)}</div>`)
  if (patientSummary) intakeParts.push(`<div style="font-size:9px;font-weight:700;color:#64748b;text-transform:uppercase;margin-bottom:3px;">Patient Summary</div><div style="font-size:10px;color:#1e293b;line-height:1.5;margin-bottom:8px;max-width:500px;">${san(patientSummary)}</div>`)
  intakeParts.push(`<div style="font-size:9px;font-weight:700;color:#64748b;text-transform:uppercase;margin-bottom:3px;">Demographics</div><div style="font-size:10px;color:#1e293b;margin-bottom:8px;">${age} y/o ${gender}</div>`)

  if (bodySystems && bodySystems.length > 0) {
    const active = bodySystems.filter(s => s.active)
    if (active.length > 0) {
      intakeParts.push(`<div style="font-size:9px;font-weight:700;color:#64748b;text-transform:uppercase;margin-bottom:3px;">Body Systems Involved</div>
        <div style="margin-bottom:8px;">${active.map(s => `<span style="display:inline-block;background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;padding:2px 6px;border-radius:4px;font-size:9px;margin:2px;">${s.full || s.name}</span>`).join(' ')}</div>`)
    }
  }

  if (chatTranscript && chatTranscript.length > 0) {
    const userMsgs = chatTranscript.filter(m => m.role === 'user' || m.sender === 'user').slice(0, 5)
    if (userMsgs.length > 0) {
      intakeParts.push(`<div style="font-size:9px;font-weight:700;color:#64748b;text-transform:uppercase;margin-bottom:3px;">Key Patient Statements</div>`)
      userMsgs.forEach(msg => {
        const text = san(msg.content || msg.text || msg.message || '')
        if (text) intakeParts.push(`<div style="font-size:10px;color:#334155;padding:4px 8px;background:#eff6ff;border-left:2px solid #3b82f6;border-radius:0 4px 4px 0;margin-bottom:4px;line-height:1.45;max-width:500px;">${text}</div>`)
      })
    }
  }

  // Alt medicine in appendix C
  const altSections = [
    { title: 'Traditional Chinese Medicine', data: tcmRecommendations, color: '#ef4444' },
    { title: 'Ayurvedic Medicine', data: ayurvedicRecommendations, color: '#f59e0b' },
    { title: 'Naturopathic & Holistic', data: holisticRecommendations, color: '#22c55e' },
  ]
  const altContent = altSections.map(({ title, data, color }) => {
    if (!data || data.length === 0) return ''
    let html = `<div style="font-size:10px;font-weight:700;color:${color};margin:8px 0 4px 0;">${title}</div>`
    data.forEach(cat => {
      html += `<div style="font-size:9px;font-weight:600;color:#64748b;margin:4px 0 2px 0;">${cat.category}</div>`
      const recs = cat.recommendations || []
      recs.forEach(r => { html += `<div style="font-size:10px;color:#475569;padding-left:12px;line-height:1.4;margin-bottom:2px;position:relative;"><span style="position:absolute;left:0;color:${color};">&bull;</span>${san(r)}</div>` })
    })
    return html
  }).filter(Boolean).join('')

  if (altContent) {
    intakeParts.push(`<div style="margin-top:10px;padding-top:8px;border-top:1px solid #e2e8f0;">
      <div style="font-size:9px;font-weight:700;color:#64748b;text-transform:uppercase;margin-bottom:3px;">Complementary Medicine Notes</div>${altContent}
      <div style="margin-top:8px;padding:4px 8px;background:#fffbeb;border:1px solid #fde68a;border-radius:4px;font-size:8px;color:#92400e;line-height:1.5;"><strong>Disclaimer:</strong> Alternative treatments are informational only. Consult a healthcare provider before use.</div>
    </div>`)
  }

  if (intakeParts.length > 0) {
    appendixC = `<div style="${forceBreak}">${heading('Appendix C: Conversation Summary', '#3b82f6')}${card(intakeParts.join(''), { bg: '#ffffff' })}</div>`
  }

  // -- Appendix D: Technical Notes -----------------------------------------
  let appendixD = ''
  const techParts = []

  if (agentList && agentList.length > 0) {
    const rows = agentList.map(a =>
      `<tr><td style="padding:3px 6px;font-size:8px;color:#475569;border-bottom:1px solid #f1f5f9;">${a.name}</td>
       <td style="padding:3px 6px;border-bottom:1px solid #f1f5f9;width:80px;"><div style="background:#f1f5f9;border-radius:3px;height:3px;overflow:hidden;"><div style="background:${a.color || '#3b82f6'};height:100%;border-radius:3px;width:${a.barWidth || 0}%;"></div></div></td>
       <td style="padding:3px 6px;text-align:right;color:#0f172a;font-weight:600;font-size:8px;font-family:monospace;border-bottom:1px solid #f1f5f9;width:45px;">${a.timeStr || (formatTime ? formatTime(a.time) : '')}</td></tr>`).join('')
    const totalStr = formatTime ? formatTime(totalPipelineTime) : (totalPipelineTime || 0).toFixed(1) + 's'
    techParts.push(`<div style="font-size:8px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Agent Pipeline Timing</div>
      <table style="width:100%;border-collapse:collapse;">${rows}
        <tr style="border-top:1px solid #e2e8f0;"><td style="padding:4px 6px;color:#0f172a;font-weight:700;font-size:9px;">Total</td><td></td>
        <td style="padding:4px 6px;text-align:right;color:#3b82f6;font-weight:800;font-size:9px;font-family:monospace;">${totalStr}</td></tr>
      </table>`)
  }

  if (estimatedCost) techParts.push(`<div style="font-size:8px;color:#475569;margin-top:6px;">Estimated cost: <strong style="color:#0f172a;">$${estimatedCost}</strong></div>`)

  if (tokenUsage) {
    const tu = typeof tokenUsage === 'object' ? tokenUsage : {}
    const parts = []
    if (tu.input) parts.push(`Input: ${tu.input}`)
    if (tu.output) parts.push(`Output: ${tu.output}`)
    if (tu.total) parts.push(`Total: ${tu.total}`)
    if (parts.length) techParts.push(`<div style="font-size:8px;color:#475569;margin-top:4px;">Tokens: ${parts.join(' | ')}</div>`)
  }

  if (techParts.length > 0) {
    appendixD = `<div style="${forceBreak}">${heading('Appendix D: Technical Notes', '#94a3b8')}${card(techParts.join(''), { bg: '#f8fafc' })}</div>`
  }

  // -- Footer (repeating via @media print) ---------------------------------
  const footerCss = `<style>@media print {
    @page { margin: 20mm 15mm 25mm 15mm; }
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    h1, h2, h3, h4, h5, h6, table { page-break-after: avoid; break-after: avoid; orphans: 3; widows: 3; }
    div[data-section] { page-break-inside: avoid; break-inside: avoid; }
  }</style>`

  const footerHtml = `
    <div style="margin-top:24px;border-top:1px solid #e2e8f0;padding-top:12px;">
      <div style="font-size:8px;color:#94a3b8;line-height:1.6;max-width:500px;">
        This report was generated by MedDiagnose AI using a 7-agent clinical analysis pipeline.
        It is intended for informational purposes only and does not constitute medical advice,
        diagnosis, or treatment. Always consult a qualified healthcare professional.
      </div>
      <div style="font-size:7px;color:#cbd5e1;margin-top:6px;">MedDiagnose AI | Clinical Report | ${date}</div>
    </div>`

  // -- DISCLAIMER BANNER ---------------------------------------------------
  const disclaimerBanner = `
    <div style="background:#fffbeb;border:1px solid #fde68a;border-left:4px solid #f59e0b;border-radius:6px;padding:10px 14px;margin-bottom:16px;${avoid}">
      <table style="width:100%;border-collapse:collapse;"><tr style="vertical-align:top;">
        <td style="width:20px;padding-right:8px;"><div style="font-size:14px;line-height:1;">&#9888;</div></td>
        <td>
          <div style="font-size:9px;font-weight:800;color:#92400e;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">Important Medical Disclaimer</div>
          <div style="font-size:9px;color:#78350f;line-height:1.5;">This AI-generated clinical report is for <strong>informational purposes only</strong> and does not constitute medical advice, diagnosis, or treatment. The analysis was produced by artificial intelligence and has not been reviewed by a licensed physician. Always seek the guidance of a qualified healthcare professional for any medical condition. If you are experiencing a medical emergency, call 911 or your local emergency services immediately.</div>
        </td>
      </tr></table>
    </div>`

  // -- ASSEMBLE ------------------------------------------------------------
  return `<div style="font-family:${font};max-width:700px;margin:0 auto;padding:20px 24px;color:#1e293b;background:#ffffff;line-height:1.6;font-size:11px;">
    ${footerCss}
    ${headerHtml}
    ${disclaimerBanner}
    ${summaryHtml}
    ${(redFlags.length > 0 || urgency === 'urgent' || urgency === 'emergency') ? heading('⚡ Recommended Next Steps', '#ef4444') + card(`
      <table style="width:100%;border-collapse:collapse;">
        ${redFlags.length > 0 ? '<tr><td style="padding:6px 10px;vertical-align:top;width:14px;"><div style="width:10px;height:10px;border-radius:50%;background:#ef4444;"></div></td><td style="padding:6px 0;font-size:11px;font-weight:600;color:#991b1b;">Seek medical attention — warning signs detected</td></tr>' : ''}
        ${recommendedTests.length > 0 ? '<tr><td style="padding:6px 10px;vertical-align:top;width:14px;"><div style="width:10px;height:10px;border-radius:50%;background:#f59e0b;"></div></td><td style="padding:6px 0;font-size:11px;font-weight:600;color:#92400e;">Schedule appointment — ' + recommendedTests.length + ' test(s) recommended</td></tr>' : ''}
        <tr><td style="padding:6px 10px;vertical-align:top;width:14px;"><div style="width:10px;height:10px;border-radius:50%;background:#10b981;"></div></td><td style="padding:6px 0;font-size:11px;font-weight:600;color:#065f46;">Follow self-care recommendations and monitor symptoms</td></tr>
      </table>
    `, { bg: '#fef2f2', border: '#fecaca' }) : ''}
    ${actionsHtml}
    ${diffHtml}
    ${testsHtml}
    ${safetyHtml}
    ${treatmentHtml}
    ${appendixA}
    ${appendixB}
    ${appendixC}
    ${appendixD}
    ${footerHtml}
  </div>`
}

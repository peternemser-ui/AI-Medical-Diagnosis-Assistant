/**
 * Generates a clean, print-optimized HTML report for PDF export.
 */
export function buildPrintReport({ causes, redFlags, recommendedTests, actionChecklist, safetyWarnings, safetyStatusLabel, agentList, totalPipelineTime, formatTime, patientAge, patientGender, formattedDate, overallUrgency }) {
  const age = patientAge || '—'
  const gender = patientGender || '—'
  const date = formattedDate
  const urgency = (overallUrgency || 'routine').toUpperCase()

  // Diagnoses
  let diagnosesHtml = ''
  for (let i = 0; i < causes.length; i++) {
    const c = causes[i]
    const urgColor = (c.urgency === 'urgent' || c.urgency === 'emergency') ? '#dc2626' : '#16a34a'
    const urgBg = (c.urgency === 'urgent' || c.urgency === 'emergency') ? '#fef2f2' : '#f0fdf4'
    const confColor = c.value >= 70 ? '#059669' : c.value >= 40 ? '#d97706' : '#64748b'
    diagnosesHtml += '<div style="border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:8px; page-break-inside:avoid;">'
    diagnosesHtml += '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">'
    diagnosesHtml += '<div>'
    diagnosesHtml += '<span style="font-weight:700; color:#1e293b;">#' + (i+1) + ' ' + c.cause + '</span>'
    diagnosesHtml += '<span style="background:' + urgBg + '; color:' + urgColor + '; padding:2px 8px; border-radius:12px; font-size:10px; font-weight:600; text-transform:uppercase; margin-left:8px;">' + c.urgency + '</span>'
    diagnosesHtml += '</div>'
    diagnosesHtml += '<span style="font-size:20px; font-weight:800; color:' + confColor + '">' + c.value + '%</span>'
    diagnosesHtml += '</div>'
    diagnosesHtml += '<div style="font-size:11px; color:#475569; margin-bottom:4px;">' + (c.specialty || '') + '</div>'
    diagnosesHtml += '<div style="font-size:11px; color:#64748b; line-height:1.5;">' + (c.explanation || '') + '</div>'
    diagnosesHtml += '</div>'
  }

  // Red flags
  let redFlagsHtml = ''
  if (redFlags.length > 0) {
    redFlagsHtml = '<div style="background:#fef2f2; border:1px solid #fecaca; border-radius:8px; padding:12px; margin-bottom:16px; page-break-inside:avoid;">'
    redFlagsHtml += '<div style="font-weight:700; color:#dc2626; font-size:12px; text-transform:uppercase; margin-bottom:6px;">Warning Signs</div>'
    redFlags.forEach(f => { redFlagsHtml += '<div style="font-size:11px; color:#991b1b; margin-bottom:3px;">⚠ ' + f + '</div>' })
    redFlagsHtml += '</div>'
  }

  // Tests
  let testsHtml = ''
  if (recommendedTests.length > 0) {
    testsHtml = '<div style="margin-bottom:16px; page-break-inside:avoid;">'
    testsHtml += '<div style="font-weight:700; color:#1e293b; font-size:12px; text-transform:uppercase; margin-bottom:8px;">Recommended Tests</div>'
    recommendedTests.forEach((t, i) => { testsHtml += '<div style="font-size:11px; color:#475569; margin-bottom:3px; padding-left:8px;">' + (i+1) + '. ' + t + '</div>' })
    testsHtml += '</div>'
  }

  // Actions
  let actionsHtml = ''
  if (actionChecklist.length > 0) {
    actionsHtml = '<div style="margin-bottom:16px; page-break-inside:avoid;">'
    actionsHtml += '<div style="font-weight:700; color:#1e293b; font-size:12px; text-transform:uppercase; margin-bottom:8px;">Action Items</div>'
    actionChecklist.forEach(a => {
      const text = typeof a === 'string' ? a : (a.action || JSON.stringify(a))
      actionsHtml += '<div style="font-size:11px; color:#475569; margin-bottom:3px; padding-left:8px;">☐ ' + text + '</div>'
    })
    actionsHtml += '</div>'
  }

  // Safety
  let safetyHtml = ''
  if (safetyWarnings.length > 0) {
    safetyHtml = '<div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:12px; margin-bottom:16px; page-break-inside:avoid;">'
    safetyHtml += '<div style="font-weight:700; color:#d97706; font-size:12px; text-transform:uppercase; margin-bottom:6px;">Safety Review — ' + safetyStatusLabel + '</div>'
    safetyWarnings.forEach(w => { safetyHtml += '<div style="font-size:11px; color:#92400e; margin-bottom:3px;">⚠ ' + w + '</div>' })
    safetyHtml += '</div>'
  }

  // Agent performance + cost
  let agentHtml = '<div style="margin-bottom:16px; page-break-inside:avoid;">'
  agentHtml += '<div style="font-weight:700; color:#1e293b; font-size:12px; text-transform:uppercase; margin-bottom:8px;">Agent Performance</div>'
  agentHtml += '<table style="width:100%; font-size:11px; border-collapse:collapse;">'
  agentList.forEach(agent => {
    agentHtml += '<tr style="border-bottom:1px solid #f1f5f9;"><td style="padding:4px 0; color:#475569;">' + agent.name + '</td><td style="padding:4px 0; text-align:right; color:#1e293b; font-weight:600;">' + agent.timeStr + '</td></tr>'
  })
  agentHtml += '<tr style="border-top:2px solid #e2e8f0;"><td style="padding:6px 0; color:#1e293b; font-weight:700;">Total Pipeline</td><td style="padding:6px 0; text-align:right; color:#1e293b; font-weight:700;">' + formatTime(totalPipelineTime) + '</td></tr>'

  const modelPref = localStorage.getItem('model_preference') || 'auto'
  const costMap = { auto: 0.015, opus: 0.075, sonnet: 0.015, haiku: 0.005, 'gpt-4o': 0.025, 'gpt-4o-mini': 0.003, 'o3': 0.10, 'gemini-2.5-pro': 0.02, 'gemini-2.5-flash': 0.005 }
  const totalCost = (causes.length > 0 ? 7 : 0) * (costMap[modelPref] || 0.015)
  agentHtml += '<tr><td style="padding:4px 0; color:#64748b; font-size:10px;">Estimated cost</td><td style="padding:4px 0; text-align:right; color:#64748b; font-size:10px;">~$' + totalCost.toFixed(3) + '</td></tr>'
  agentHtml += '</table></div>'

  const urgencyColor = (urgency === 'URGENT' || urgency === 'EMERGENCY') ? '#dc2626' : '#059669'

  return '<div style="font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; max-width:700px; margin:0 auto; padding:20px; color:#1e293b; background:#fff;">'
    + '<div style="border-bottom:2px solid #3b82f6; padding-bottom:12px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:flex-end;">'
    + '<div><div style="font-size:22px; font-weight:800; color:#1e293b;">Medical Diagnosis Report</div>'
    + '<div style="font-size:11px; color:#64748b; margin-top:2px;">MedDiagnose AI — Multi-Agent Analysis</div></div>'
    + '<div style="text-align:right; font-size:11px; color:#64748b;">'
    + '<div>Patient: ' + age + ' ' + gender + '</div>'
    + '<div>' + date + '</div>'
    + '<div style="font-weight:600; color:' + urgencyColor + ';">' + urgency + '</div>'
    + '</div></div>'
    + redFlagsHtml
    + '<div style="margin-bottom:16px;"><div style="font-weight:700; color:#1e293b; font-size:14px; margin-bottom:10px;">Differential Diagnoses</div>' + diagnosesHtml + '</div>'
    + testsHtml + actionsHtml + safetyHtml + agentHtml
    + '<div style="margin-top:24px; padding-top:12px; border-top:1px solid #e2e8f0; font-size:9px; color:#94a3b8; line-height:1.4;">This report is generated by AI for informational purposes only. It does not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.</div>'
    + '</div>'
}

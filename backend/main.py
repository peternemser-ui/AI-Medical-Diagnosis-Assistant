from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json
import re
from dotenv import load_dotenv
from ai_engine import run_diagnosis_prompt, run_simple_ai_prompt

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Health AI API",
    version="1.0.0",
    description="AI-powered health diagnosis API"
)

# CORS middleware - MUST be added BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions for diagnosis
def generate_comprehensive_diagnosis(request, causes, diagnosis_data, red_flags=None, additional_questions=None, recommended_tests=None):
    """Generate a comprehensive diagnosis response using AI results with professional HTML styling"""
    
    # Parse diagnosis data if it's a string
    try:
        if isinstance(diagnosis_data, str):
            diagnosis_json = json.loads(diagnosis_data)
        else:
            diagnosis_json = diagnosis_data
    except:
        diagnosis_json = {"diagnoses": []}
    
    diagnoses = diagnosis_json.get("diagnoses", [])
    red_flags = red_flags or []
    additional_questions = additional_questions or []
    recommended_tests = recommended_tests or []
    
    # Start HTML with embedded CSS
    html = f"""
<div class="medical-assessment">
    <style>
        .medical-assessment {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 820px;
            margin: 0 auto;
            line-height: 1.35;
            color: #e4e4e7;
            font-size: 14px;
        }}
        .assessment-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.25);
        }}
        .assessment-header h1 {{
            margin: 0 0 16px 0;
            font-size: 28px;
            font-weight: 600;
            color: white;
        }}
        .patient-info-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            overflow: hidden;
        }}
        .patient-info-table td {{
            padding: 6px 10px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }}
        .patient-info-table td:first-child {{
            font-weight: 600;
            color: #a78bfa;
            width: 140px;
        }}
        .patient-info-table tr:last-child td {{
            border-bottom: none;
        }}
        .alert-danger {{
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            border-left: 4px solid #b91c1c;
            padding: 20px;
            border-radius: 8px;
            margin: 24px 0;
            box-shadow: 0 4px 6px rgba(239, 68, 68, 0.3);
        }}
        .alert-danger h2 {{
            margin: 0 0 12px 0;
            font-size: 20px;
            color: white;
        }}
        .alert-danger ul {{
            margin: 12px 0 0 0;
            padding-left: 24px;
        }}
        .alert-danger li {{
            margin: 8px 0;
            color: #fef2f2;
        }}
        .section {{
            background: rgba(30, 30, 46, 0.55);
            border-radius: 10px;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid rgba(167, 139, 250, 0.12);
        }}
        .section h2 {{
            margin: 0 0 8px 0;
            font-size: 17px;
            color: #c4b5fd;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .diagnosis-card {{
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.06) 0%, rgba(124, 58, 237, 0.06) 100%);
            border: 1px solid rgba(167, 139, 250, 0.12);
            border-radius: 8px;
            padding: 10px;
            margin: 8px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }}
        .diagnosis-card h3 {{
            margin: 0 0 8px 0;
            font-size: 15px;
            color: #e9d5ff;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .diagnosis-table {{
            width: 100%;
            margin: 16px 0;
            border-collapse: separate;
            border-spacing: 0;
        }}
        .diagnosis-table td {{
            padding: 6px 10px;
            border-bottom: 1px solid rgba(167, 139, 250, 0.08);
        }}
        .diagnosis-table td:first-child {{
            font-weight: 600;
            color: #c4b5fd;
            width: 140px;
        }}
        .diagnosis-table tr:last-child td {{
            border-bottom: none;
        }}
        .confidence-bar {{
            height: 18px;
            background: rgba(30, 30, 46, 0.6);
            border-radius: 8px;
            overflow: hidden;
            position: relative;
            margin: 6px 0;
        }}
        .confidence-fill {{
            height: 100%;
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
            border-radius: 12px;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 12px;
            color: white;
            font-weight: 600;
            font-size: 12px;
        }}
        .confidence-high {{ background: linear-gradient(90deg, #10b981 0%, #059669 100%); }}
        .confidence-medium {{ background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%); }}
        .confidence-low {{ background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%); }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: 600;
            margin: 0 4px;
        }}
        .badge-urgent {{ background: #ef4444; color: white; }}
        .badge-soon {{ background: #f59e0b; color: white; }}
        .badge-routine {{ background: #3b82f6; color: white; }}
        .badge-high {{ background: #10b981; color: white; }}
        .badge-medium {{ background: #f59e0b; color: white; }}
        .badge-low {{ background: #6b7280; color: white; }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 16px;
            margin: 16px 0;
        }}
        .info-card {{
            background: rgba(139, 92, 246, 0.06);
            border: 1px solid rgba(167, 139, 250, 0.12);
            border-radius: 6px;
            padding: 8px;
        }}
        .info-card h4 {{
            margin: 0 0 8px 0;
            font-size: 16px;
            color: #c4b5fd;
        }}
        .info-card p {{
            margin: 0;
            color: #e4e4e7;
            font-size: 14px;
        }}
        .timeline-box {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(37, 99, 235, 0.08) 100%);
            border-left: 4px solid #3b82f6;
            padding: 10px;
            border-radius: 6px;
            margin: 8px 0;
        }}
        .timeline-urgent {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.15) 100%);
            border-left-color: #ef4444;
        }}
        .timeline-soon {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.15) 100%);
            border-left-color: #f59e0b;
        }}
        .checklist {{
            list-style: none;
            padding: 0;
            margin: 12px 0;
        }}
        .checklist li {{
            padding: 6px 0;
            padding-left: 24px;
            position: relative;
        }}
        .checklist li:before {{
            content: "→";
            position: absolute;
            left: 8px;
            color: #c4b5fd;
            font-weight: bold;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }}
        .stat-box {{
            background: rgba(139, 92, 246, 0.06);
            border: 1px solid rgba(167, 139, 250, 0.12);
            border-radius: 6px;
            padding: 10px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            color: #c4b5fd;
            margin: 8px 0;
        }}
        .stat-label {{
            font-size: 13px;
            color: #a1a1aa;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .disclaimer {{
            background: rgba(239, 68, 68, 0.06);
            border: 1px solid rgba(239, 68, 68, 0.12);
            border-radius: 6px;
            padding: 10px;
            margin: 8px 0;
        }}
        .disclaimer h3 {{
            margin: 0 0 6px 0;
            color: #fca5a5;
        }}
        .clinical-reasoning {{
            background: rgba(30, 30, 46, 0.35);
            padding: 8px;
            border-radius: 6px;
            margin-top: 8px;
            border-left: 3px solid #8b5cf6;
        }}
    </style>

    <div class="assessment-header">
        <h1>🏥 AI Medical Assessment</h1>
        <table class="patient-info-table">
            <tr>
                <td>👤 Age</td>
                <td>{request.age} years</td>
            </tr>
            <tr>
                <td>⚧ Gender</td>
                <td>{request.gender}</td>
            </tr>
            <tr>
                <td>🩺 Chief Complaint</td>
                <td>{request.symptoms[:200]}{'...' if len(request.symptoms) > 200 else ''}</td>
            </tr>
        </table>
    </div>
"""
    
    # Red flags section
    if red_flags:
        html += """
    <div class="alert-danger">
        <h2>🚨 Warning Signs Identified</h2>
        <p>The following concerning symptoms have been identified:</p>
        <ul>
"""
        for flag in red_flags:
            html += f"            <li>{flag}</li>\n"
        html += """
        </ul>
        <p><strong>Recommendation:</strong> Seek immediate medical evaluation for these warning signs.</p>
    </div>
"""
    
    # Differential diagnosis section
    if diagnoses:
        html += """
    <div class="section">
        <h2>🔬 Differential Diagnosis</h2>
"""
        
        for i, diagnosis in enumerate(diagnoses[:3], 1):
            condition = diagnosis.get("condition", "Unknown condition")
            confidence = diagnosis.get("confidence", 0)
            explanation = diagnosis.get("explanation", "No explanation provided")
            urgency = diagnosis.get("urgency", "routine")
            specialty = diagnosis.get("specialty", "Primary Care")
            
            confidence_level = "High" if confidence >= 70 else "Moderate" if confidence >= 50 else "Low"
            confidence_class = "high" if confidence >= 70 else "medium" if confidence >= 50 else "low"
            urgency_badge = f'<span class="badge badge-{urgency}">{urgency.upper()}</span>'
            confidence_badge = f'<span class="badge badge-{confidence_class}">{confidence_level}</span>'
            
            html += f"""
        <div class="diagnosis-card">
            <h3>{i}. {condition}</h3>
            
            <table class="diagnosis-table">
                <tr>
                    <td>Confidence Level</td>
                    <td>{confidence_badge} {confidence}%</td>
                </tr>
                <tr>
                    <td>Confidence Bar</td>
                    <td>
                        <div class="confidence-bar">
                            <div class="confidence-fill confidence-{confidence_class}" style="width: {confidence}%">
                                {confidence}%
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>Urgency</td>
                    <td>{urgency_badge}</td>
                </tr>
                <tr>
                    <td>Recommended Specialty</td>
                    <td>{specialty}</td>
                </tr>
            </table>
            
            <div class="clinical-reasoning">
                <strong>📋 Clinical Reasoning:</strong>
                <p style="margin:6px 0 0 0; white-space:pre-wrap;">{explanation}</p>
            </div>
        </div>
"""
        
        html += """
    </div>
"""
    
    # Additional diagnostic questions
    if additional_questions:
        html += """
    <div class="section">
        <h2>🔍 Additional Information Needed</h2>
        <div class="info-grid">
"""
        for i, question in enumerate(additional_questions, 1):
            html += f"""
            <div class="info-card">
                <h4>Question {i}</h4>
                <p>{question}</p>
            </div>
"""
        html += """
        </div>
    </div>
"""
    
    # Recommended tests  
    if recommended_tests:
        html += """
    <div class="section">
        <h2>🧪 Suggested Diagnostic Tests</h2>
        <ul class="checklist">
"""
        for test in recommended_tests:
            html += f"            <li>{test}</li>\n"
        html += """
        </ul>
    </div>
"""
    
    # Clinical recommendations
    recommendations = generate_smart_recommendations(request.symptoms, diagnoses)
    if recommendations:
        html += """
    <div class="section">
        <h2>💊 Clinical Recommendations</h2>
        <div class="info-grid">
"""
        for rec in recommendations:
            html += f"""
            <div class="info-card">
                <h4>{rec['title']}</h4>
                <p>{rec['description']}</p>
            </div>
"""
        html += """
        </div>
    </div>
"""
    
    # Urgency timeline
    urgency_level = assess_urgency_from_diagnoses(diagnoses, red_flags)
    timeline_class = "timeline-urgent" if urgency_level == "urgent" or red_flags else "timeline-soon" if urgency_level == "soon" else ""
    
    html += f"""
    <div class="section">
        <h2>⏱️ Medical Care Timeline</h2>
        <div class="timeline-box {timeline_class}">
"""
    
    if urgency_level == "urgent" or red_flags:
        html += """
            <h3 style="margin-top: 0;">🚨 URGENT - Seek immediate medical attention</h3>
            <ul class="checklist">
                <li>Go to emergency room immediately</li>
                <li>Call emergency services if needed</li>
                <li>Do not delay seeking care</li>
                <li>Have someone accompany you</li>
            </ul>
"""
    elif urgency_level == "soon":
        html += """
            <h3 style="margin-top: 0;">⚠️ SOON - Schedule appointment within 24-48 hours</h3>
            <ul class="checklist">
                <li>Contact your primary care provider</li>
                <li>Consider urgent care if provider unavailable</li>
                <li>Monitor symptoms closely</li>
                <li>Seek care sooner if symptoms worsen</li>
            </ul>
"""
    else:
        html += """
            <h3 style="margin-top: 0;">📅 ROUTINE - Schedule appointment at your convenience</h3>
            <ul class="checklist">
                <li>Contact your primary care provider within 1-2 weeks</li>
                <li>Continue monitoring symptoms</li>
                <li>Seek care sooner if symptoms worsen</li>
                <li>Maintain a symptom diary</li>
            </ul>
"""
    
    html += """
        </div>
    </div>
"""
    
    # Summary statistics
    if diagnoses:
        top_confidence = max(d.get("confidence", 0) for d in diagnoses)
        html += f"""
    <div class="section">
        <h2>📈 Assessment Summary</h2>
        <div class="stat-grid">
            <div class="stat-box">
                <div class="stat-label">Diagnoses Considered</div>
                <div class="stat-value">{len(diagnoses)}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Highest Confidence</div>
                <div class="stat-value">{top_confidence}%</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Urgency Level</div>
                <div class="stat-value">{urgency_level.upper()}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Warning Signs</div>
                <div class="stat-value">{len(red_flags)}</div>
            </div>
        </div>
    </div>
"""
    
    # Disclaimer
    html += """
    <div class="disclaimer">
        <h3>⚠️ MEDICAL DISCLAIMER</h3>
        <p>This AI-generated assessment is for <strong>educational and informational purposes only</strong>.</p>
        <ul class="checklist">
            <li>NOT a substitute for professional medical care</li>
            <li>Always consult qualified healthcare providers</li>
            <li>In emergency, call local emergency services</li>
            <li>Do not delay seeking professional care</li>
        </ul>
        <p style="margin-top: 16px; font-size: 13px; opacity: 0.8;">📋 Assessment generated by AI Medical Diagnosis Assistant v2.5</p>
    </div>

</div>
"""
    
    return html


def generate_comprehensive_diagnosis_text(request, causes, diagnosis_data, red_flags=None, additional_questions=None, recommended_tests=None):
    """Generate a compact plaintext diagnosis summary (no HTML/CSS).

    This is intended for programmatic consumption by the frontend when a
    plain-text answer is preferred to avoid embedding style blocks.
    """
    # Parse diagnosis data if it's a string
    try:
        if isinstance(diagnosis_data, str):
            diagnosis_json = json.loads(diagnosis_data)
        else:
            diagnosis_json = diagnosis_data
    except Exception:
        diagnosis_json = {"diagnoses": []}

    diagnoses = diagnosis_json.get("diagnoses", [])
    red_flags = red_flags or []
    additional_questions = additional_questions or []
    recommended_tests = recommended_tests or []

    lines = []
    lines.append("AI Medical Assessment")
    lines.append("---------------------")
    lines.append(f"Age: {request.age} years | Gender: {request.gender}")
    # Shorten symptoms preview to avoid massive blocks
    symptoms_preview = (request.symptoms[:800] + '...') if len(request.symptoms) > 800 else request.symptoms
    lines.append(f"Chief complaint: {symptoms_preview}")

    # Red flags
    if red_flags:
        lines.append("")
        lines.append("Warning signs identified:")
        for flag in red_flags:
            lines.append(f"- {flag}")
        lines.append("Recommendation: Seek immediate medical evaluation for these warning signs.")

    # Differential diagnoses
    if diagnoses:
        lines.append("")
        lines.append("Differential diagnosis:")
        for i, diagnosis in enumerate(diagnoses[:5], 1):
            condition = diagnosis.get("condition", "Unknown condition")
            confidence = diagnosis.get("confidence", 0)
            explanation = diagnosis.get("explanation", "No explanation provided")
            urgency = diagnosis.get("urgency", "routine")
            specialty = diagnosis.get("specialty", "Primary Care")

            lines.append(f"{i}. {condition} — Confidence: {confidence}% — Urgency: {urgency} — Specialty: {specialty}")
            # Keep explanation compact; trim long text
            expl = explanation.strip()
            if len(expl) > 500:
                expl = expl[:500].rstrip() + '...'
            # Indent explanation on next line for readability
            lines.append(f"   Clinical reasoning: {expl}")

    # Additional questions
    if additional_questions:
        lines.append("")
        lines.append("Additional information needed:")
        for q in additional_questions:
            lines.append(f"- {q}")

    # Recommended tests
    if recommended_tests:
        lines.append("")
        lines.append("Suggested diagnostic tests:")
        for t in recommended_tests:
            lines.append(f"- {t}")

    # Clinical recommendations (smart recommendations)
    recommendations = generate_smart_recommendations(request.symptoms, diagnoses)
    if recommendations:
        lines.append("")
        lines.append("Clinical recommendations:")
        for rec in recommendations:
            title = rec.get('title', '')
            desc = rec.get('description', '')
            lines.append(f"- {title}: {desc}")

    # Urgency timeline
    urgency_level = assess_urgency_from_diagnoses(diagnoses, red_flags)
    lines.append("")
    if urgency_level == 'urgent' or red_flags:
        lines.append("Urgency: URGENT — Seek immediate medical attention (ER or call emergency services).")
    elif urgency_level == 'soon':
        lines.append("Urgency: Soon — Schedule appointment within 24-48 hours.")
    else:
        lines.append("Urgency: Routine — Schedule at your convenience and monitor symptoms.")

    # Summary statistics
    if diagnoses:
        top_confidence = max(d.get("confidence", 0) for d in diagnoses)
        lines.append("")
        lines.append("Assessment summary:")
        lines.append(f"- Diagnoses considered: {len(diagnoses)}")
        lines.append(f"- Highest confidence: {top_confidence}%")
        lines.append(f"- Warning signs count: {len(red_flags)}")

    # Brief disclaimer (single-line)
    lines.append("")
    lines.append("Disclaimer: This AI-generated assessment is for informational purposes only and not a substitute for professional medical care. In emergencies, call local emergency services.")

    # Join with single blank line between sections for compactness
    return "\n".join(lines)


def generate_fallback_diagnosis(request):
    """Generate a fallback diagnosis when AI is not available"""
    
    # Basic symptom analysis
    symptoms_lower = request.symptoms.lower()
    
    # Simple keyword-based assessment
    likely_conditions = []
    
    # Common conditions based on keywords
    if any(word in symptoms_lower for word in ["fever", "temperature", "hot", "chills"]):
        likely_conditions.append("Viral or bacterial infection")
    
    if any(word in symptoms_lower for word in ["cough", "throat", "sore throat"]):
        likely_conditions.append("Upper respiratory infection")
    
    if any(word in symptoms_lower for word in ["headache", "head pain", "migraine"]):
        likely_conditions.append("Headache disorder")
    
    if any(word in symptoms_lower for word in ["stomach", "nausea", "vomit", "diarrhea"]):
        likely_conditions.append("Gastrointestinal issue")
    
    if any(word in symptoms_lower for word in ["pain", "ache", "hurt", "sore"]):
        likely_conditions.append("Musculoskeletal condition")
    
    if not likely_conditions:
        likely_conditions.append("General medical condition")
    
    response_parts = []
    response_parts.append("# Medical Assessment")
    response_parts.append("")
    response_parts.append(f"**Symptoms Analyzed:** {request.symptoms}")
    response_parts.append("")
    response_parts.append(f"**Patient Information:**")
    response_parts.append(f"- Age: {request.age} years")
    response_parts.append(f"- Gender: {request.gender}")
    response_parts.append("")
    
    response_parts.append("## Preliminary Assessment")
    response_parts.append("")
    response_parts.append("Based on your symptoms, the following conditions may be relevant:")
    response_parts.append("")
    
    for condition in likely_conditions[:3]:
        response_parts.append(f"- {condition}")
    
    response_parts.append("")
    response_parts.append("## General Recommendations")
    response_parts.append("")
    response_parts.append("1. **Monitor symptoms** and note any changes")
    response_parts.append("2. **Stay hydrated** with plenty of fluids")
    response_parts.append("3. **Get adequate rest** to support recovery")
    response_parts.append("4. **Consult a healthcare provider** for proper evaluation")
    response_parts.append("5. **Seek immediate care** if symptoms worsen significantly")
    response_parts.append("")
    response_parts.append("⚠️ **Note:** This is a basic assessment. For accurate diagnosis and treatment, please consult with a qualified healthcare professional.")
    
    return "\n".join(response_parts)

def calculate_confidence_scores(causes):
    """Calculate confidence scores from AI diagnosis results"""
    
    if not causes:
        return {"high": 0.6, "medium": 0.3, "low": 0.1}
    
    # Sort causes by confidence
    sorted_causes = sorted(causes, key=lambda x: x.get("value", 0), reverse=True)
    
    total_confidence = sum(cause.get("value", 0) for cause in sorted_causes)
    
    if total_confidence == 0:
        return {"high": 0.6, "medium": 0.3, "low": 0.1}
    
    # Calculate weighted confidence levels
    high_confidence = 0
    medium_confidence = 0
    low_confidence = 0
    
    for cause in sorted_causes:
        confidence = cause.get("value", 0)
        weight = confidence / total_confidence
        
        if confidence >= 70:
            high_confidence += weight
        elif confidence >= 40:
            medium_confidence += weight
        else:
            low_confidence += weight
    
    # Normalize to ensure they sum to 1
    total = high_confidence + medium_confidence + low_confidence
    if total > 0:
        high_confidence /= total
        medium_confidence /= total
        low_confidence /= total
    else:
        high_confidence = 0.6
        medium_confidence = 0.3
        low_confidence = 0.1
    
    return {
        "high": round(high_confidence, 2),
        "medium": round(medium_confidence, 2),
        "low": round(low_confidence, 2)
    }

def generate_smart_recommendations(symptoms, diagnoses):
    """Generate smart recommendations based on symptoms and diagnoses"""
    
    symptoms_lower = symptoms.lower()
    recommendations = []
    
    # Basic monitoring
    recommendations.append({
        "title": "Symptom Monitoring",
        "description": "Keep a detailed log of your symptoms, including timing, severity, and triggers"
    })
    
    # Hydration and rest
    if any(word in symptoms_lower for word in ["fever", "cough", "throat", "tired", "fatigue"]):
        recommendations.append({
            "title": "Rest and Hydration",
            "description": "Ensure adequate sleep and drink plenty of fluids to support your immune system"
        })
    
    # Pain management
    if any(word in symptoms_lower for word in ["pain", "ache", "hurt", "sore"]):
        recommendations.append({
            "title": "Pain Management",
            "description": "Consider appropriate over-the-counter pain relief if suitable for your condition"
        })
    
    # Temperature management
    if any(word in symptoms_lower for word in ["fever", "hot", "chills"]):
        recommendations.append({
            "title": "Temperature Control",
            "description": "Monitor temperature regularly and use appropriate fever reduction methods if needed"
        })
    
    # Breathing support
    if any(word in symptoms_lower for word in ["cough", "breathing", "chest", "lungs"]):
        recommendations.append({
            "title": "Respiratory Support",
            "description": "Use humidifiers, steam inhalation, or other breathing support measures as appropriate"
        })
    
    # Medical consultation
    recommendations.append({
        "title": "Professional Consultation",
        "description": "Schedule an appointment with your healthcare provider for proper evaluation and treatment planning"
    })
    
    return recommendations[:5]  # Return top 5 recommendations

def assess_urgency_from_diagnoses(diagnoses, red_flags):
    """Assess urgency based on AI diagnoses and red flags"""
    
    if red_flags:
        return "urgent"
    
    if not diagnoses:
        return "routine"
    
    # Check urgency levels from AI diagnoses
    urgency_levels = [d.get("urgency", "routine") for d in diagnoses]
    
    if "urgent" in urgency_levels:
        return "urgent"
    elif "soon" in urgency_levels:
        return "soon"
    else:
        return "routine"

def assess_urgency(symptoms, diagnoses):
    """Assess the urgency level of symptoms"""
    
    symptoms_lower = symptoms.lower()
    
    # Urgent keywords
    urgent_keywords = [
        "severe", "intense", "unbearable", "emergency", "can't breathe", 
        "chest pain", "difficulty breathing", "confused", "dizzy", 
        "bleeding", "unconscious", "seizure"
    ]
    
    # Soon keywords
    soon_keywords = [
        "worsening", "getting worse", "high fever", "persistent", 
        "several days", "week", "not improving"
    ]
    
    if any(keyword in symptoms_lower for keyword in urgent_keywords):
        return "urgent"
    
    if any(keyword in symptoms_lower for keyword in soon_keywords):
        return "soon"
    
    # Check diagnosis confidence for urgency
    if diagnoses:
        max_confidence = max(d.get("confidence", 0) for d in diagnoses)
        if max_confidence >= 80:
            return "soon"
    
    return "routine"

# Request models
class DiagnosisRequest(BaseModel):
    symptoms: str
    age: int = 30
    gender: str = "unknown"
    duration: str = "recent"
    severity: int = 5

class FollowupRequest(BaseModel):
    question: str
    previous_messages: list = []
    original_symptoms: str = ""

# Root endpoint
@app.get("/")
async def read_root():
    return {
        "message": "Health AI API is running!",
        "status": "ok",
        "version": "1.0.0",
        "endpoints": [
            "GET /",
            "GET /health",
            "POST /api/diagnose",
            "GET /docs"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Backend is working!",
        "cors": "enabled",
        "timestamp": "2025-08-12"
    }

# Diagnosis endpoint
@app.post("/api/diagnose")
async def diagnose_symptoms(
    diagnosis_request: DiagnosisRequest,
    http_request: Request,
    x_openai_api_key: Optional[str] = Header(None)
):
    try:
        print(f"✅ Received diagnosis request for: {diagnosis_request.symptoms}")
        
        # Get API key from header or environment variable
        api_key = x_openai_api_key or os.getenv("OPENAI_API_KEY")
        
        # Check if OpenAI API key is available
        if not api_key:
            print("⚠️ No OpenAI API key found, using fallback response")
            # Fallback to basic response if no API key
            response_text = generate_fallback_diagnosis(diagnosis_request)
            return {
                "answer": response_text,
                "confidence_scores": {
                    "high": 0.6,
                    "medium": 0.3,
                    "low": 0.1
                },
                "estimated_cost": 0.0,
                "timestamp": "2025-10-29"
            }
        
        print(f"✅ Using OpenAI API key from {'header' if x_openai_api_key else 'environment'}")
        
        # Use AI engine for proper diagnosis
        try:
            ai_result = run_diagnosis_prompt(
                age=diagnosis_request.age,
                gender=diagnosis_request.gender,
                symptoms=diagnosis_request.symptoms,
                image_base64=None,  # Not implemented in frontend yet
                audio_base64=None,  # Not implemented in frontend yet
                api_key=api_key  # Pass API key to AI engine
            )
            
            # Parse the diagnosis result
            diagnosis_data = ai_result.get("diagnosis", "{}")
            causes = ai_result.get("causes", [])
            red_flags = ai_result.get("red_flags", [])
            additional_questions = ai_result.get("additional_questions", [])
            recommended_tests = ai_result.get("recommended_tests", [])
            
            # Generate comprehensive plaintext response (no HTML/CSS)
            response_text = generate_comprehensive_diagnosis_text(
                diagnosis_request, causes, diagnosis_data, red_flags, additional_questions, recommended_tests
            )
            
            # Calculate confidence scores from causes
            confidence_scores = calculate_confidence_scores(causes)
            
            return {
                "answer": response_text,
                "confidence_scores": confidence_scores,
                "estimated_cost": 0.05,
                "timestamp": "2025-10-29",
                "causes": causes,
                "red_flags": red_flags,
                "additional_questions": additional_questions,
                "recommended_tests": recommended_tests
            }
            
        except Exception as ai_error:
            print(f"❌ AI diagnosis failed: {str(ai_error)}")
            # Fallback to enhanced static response
            response_text = generate_fallback_diagnosis(diagnosis_request)
            return {
                "answer": response_text,
                "confidence_scores": {
                    "high": 0.6,
                    "medium": 0.3,
                    "low": 0.1
                },
                "estimated_cost": 0.0,
                "timestamp": "2025-10-29"
            }
        
    except Exception as e:
        print(f"❌ Error in diagnosis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Followup endpoint for medication and additional questions
@app.post("/api/followup")
async def followup_question(
    followup_req: FollowupRequest,
    http_request: Request,
    x_openai_api_key: Optional[str] = Header(None)
):
    try:
        print(f"✅ Received followup question: {followup_req.question}")
        
        # Get API key from header or environment variable
        api_key = x_openai_api_key or os.getenv("OPENAI_API_KEY")
        
        # Analyze the question to provide appropriate response
        question_lower = followup_req.question.lower()
        
        if "medication" in question_lower or "over-the-counter" in question_lower or "otc" in question_lower:
            response_text = """# Over-the-Counter Medication Guidance

⚠️ **Important**: Always consult with a pharmacist or healthcare provider before taking any medication, especially if you have allergies, medical conditions, or take other medications.

## Safe OTC Options by Symptom Category:

### 🌡️ **Fever & Pain Relief:**
- **Acetaminophen (Tylenol)**: 500-1000mg every 6-8 hours (max 3000mg/day)
  - Safe for most people, minimal drug interactions
  - Good for fever, headache, general aches
- **Ibuprofen (Advil, Motrin)**: 200-400mg every 6-8 hours (max 1200mg/day)
  - Anti-inflammatory properties
  - Good for muscle pain, inflammation
  - Avoid if you have kidney disease, stomach ulcers, or heart conditions

### 🤧 **Cold & Respiratory Symptoms:**
- **Decongestants**: 
  - Pseudoephedrine (Sudafed): 30-60mg every 4-6 hours
  - Phenylephrine: 10mg every 4 hours
- **Cough Suppressants**: 
  - Dextromethorphan: 15-30mg every 4 hours for dry cough
- **Expectorants**: 
  - Guaifenesin: 200-400mg every 4 hours to thin mucus
- **Throat lozenges**: For sore throat relief

### 🤢 **Digestive Issues:**
- **Antacids**: Tums, Rolaids for heartburn (follow label instructions)
- **Anti-diarrheal**: Loperamide (Imodium) for diarrhea
- **Simethicone**: For gas and bloating
- **Probiotics**: For digestive health support

### 🩹 **Topical Treatments:**
- **Antiseptic creams**: For minor cuts and scrapes
- **Hydrocortisone cream**: For itching and minor skin irritation
- **Calamine lotion**: For poison ivy, insect bites

## ⚠️ **Critical Safety Guidelines:**

### **Read Labels Carefully:**
- Check active ingredients to avoid duplication
- Follow dosing instructions precisely
- Note contraindications and warnings

### **Avoid if You Have:**
- Known allergies to the medication
- Severe liver or kidney disease (for certain medications)
- Active stomach ulcers (for NSAIDs like ibuprofen)
- Heart conditions (check with doctor first)

### **Drug Interactions:**
- Blood thinners + aspirin/ibuprofen = increased bleeding risk
- ACE inhibitors + ibuprofen = kidney problems
- Multiple acetaminophen products = liver damage risk

### **Special Populations:**
- **Pregnant/Breastfeeding**: Consult healthcare provider first
- **Children**: Use pediatric formulations with proper dosing
- **Elderly**: May need reduced doses, higher side effect risk

## 🚨 **When NOT to Self-Medicate:**

- Symptoms are severe or worsening rapidly
- You have multiple medical conditions
- You're taking prescription medications
- Symptoms persist despite treatment
- You're unsure about drug interactions

## 📞 **Professional Resources:**

- **Pharmacist consultation**: Free at most pharmacies
- **Nurse hotline**: Many insurance plans offer 24/7 nurse lines
- **Poison control**: 1-800-222-1222 for medication overdose concerns

**Remember**: OTC medications treat symptoms but don't cure underlying conditions. If symptoms persist or worsen, seek professional medical evaluation."""

        elif "doctor" in question_lower or "medical" in question_lower or "see" in question_lower:
            response_text = """# When to See a Doctor

Based on your symptoms, here's guidance on seeking medical care:

## See a Doctor Soon (Within 1-2 Days) If:

- Symptoms persist for more than 3-5 days without improvement
- Fever above 101°F (38.3°C) for more than 2 days
- Persistent cough with colored mucus
- Difficulty sleeping due to symptoms
- Symptoms interfere with daily activities

## Seek Urgent Care (Same Day) If:

- Fever above 103°F (39.4°C)
- Severe headache with neck stiffness
- Difficulty breathing or shortness of breath
- Persistent vomiting or inability to keep fluids down
- Signs of dehydration (dizziness, dry mouth, little/no urination)

## Call 911 or Go to ER Immediately If:

- Severe difficulty breathing
- Chest pain or pressure
- Severe allergic reaction (swelling, rash, difficulty breathing)
- Loss of consciousness or confusion
- Severe dehydration symptoms

## Questions to Ask Your Doctor:

1. What could be causing these symptoms?
2. What tests might be needed?
3. What treatments are available?
4. How long should recovery take?
5. When should I follow up?
6. What warning signs should I watch for?

## How to Prepare for Your Visit:

- Write down all symptoms and when they started
- List any medications you're taking
- Note what makes symptoms better or worse
- Bring a list of questions
- Consider bringing a family member for support

**Remember**: It's always better to check with a healthcare professional when in doubt about your symptoms."""

        elif "home" in question_lower or "remedy" in question_lower or "treatment" in question_lower:
            response_text = """# Home Care and Natural Remedies

Here are safe, effective home treatments to help manage your symptoms:

## General Comfort Measures:

### Rest & Recovery:
- **Get plenty of sleep** (7-9 hours per night)
- **Take time off** work/school if possible
- **Avoid strenuous activities** until feeling better

### Hydration:
- **Drink plenty of fluids**: Water, herbal teas, clear broths
- **Warm liquids** can soothe throat and nasal passages
- **Avoid alcohol and caffeine** which can dehydrate

### Nutrition:
- **Eat light, nutritious foods**: Soups, fruits, vegetables
- **Honey** can soothe cough and throat irritation
- **Ginger tea** may help with nausea and inflammation

## Symptom-Specific Home Remedies:

### For Congestion:
- **Steam inhalation**: Breathe steam from hot shower or bowl of hot water
- **Saline nasal rinse**: Neti pot or saline spray
- **Humidifier**: Add moisture to dry air
- **Elevate head** while sleeping

### For Sore Throat:
- **Salt water gargle**: 1/2 tsp salt in warm water
- **Warm tea with honey**
- **Ice chips or popsicles** for numbing relief

### For Cough:
- **Honey** (1-2 tsp before bed)
- **Warm liquids** to thin mucus
- **Avoid irritants** like smoke or strong odors

### For Body Aches:
- **Warm bath** with Epsom salts
- **Gentle stretching**
- **Heat therapy**: Heating pad or warm compress
- **Light massage**

## When Home Remedies Aren't Enough:

- Symptoms worsen instead of improving
- High fever persists
- Difficulty breathing develops
- Severe pain that doesn't respond to treatment

**Note**: These remedies complement but don't replace professional medical care when needed."""

        elif "worse" in question_lower or "getting" in question_lower or "symptoms" in question_lower:
            response_text = """# Monitoring Symptom Progression

Here's how to track if your symptoms are improving or worsening:

## Signs Your Symptoms Are **Getting Better**:

✅ **Fever is decreasing** or staying below 100°F (37.8°C)
✅ **Energy levels improving** - feeling less tired
✅ **Appetite returning**
✅ **Sleep quality improving**
✅ **Symptoms are less intense** than when they started
✅ **Able to do more daily activities**

## Signs Your Symptoms Are **Getting Worse**:

⚠️ **Fever rising** above 101°F (38.3°C) or lasting more than 3 days
⚠️ **New symptoms developing** (chest pain, difficulty breathing, severe headache)
⚠️ **Existing symptoms intensifying**
⚠️ **Feeling more exhausted** than before
⚠️ **Unable to keep fluids down**
⚠️ **Difficulty performing basic activities**

## Keep a Symptom Diary:

Track daily:
- **Temperature** (if you have fever)
- **Energy level** (1-10 scale)
- **Appetite**
- **Sleep quality**
- **Specific symptoms** and their intensity
- **Medications taken**

## Red Flag Symptoms - Seek Immediate Care:

🚨 **Difficulty breathing** or shortness of breath
🚨 **Chest pain or pressure**
🚨 **Severe headache** with neck stiffness
🚨 **High fever** (103°F/39.4°C or higher)
🚨 **Persistent vomiting**
🚨 **Signs of dehydration**
🚨 **Confusion or altered mental state**

## Timeline Expectations:

- **Days 1-3**: Symptoms may worsen before improving
- **Days 4-7**: Should see gradual improvement
- **Week 2+**: Most symptoms should be resolved

**If symptoms don't follow this pattern or you're concerned, contact your healthcare provider.**"""

        else:
            # General followup response
            response_text = f"""Thank you for your follow-up question: "{followup_req.question}"

Based on your previous symptoms and the information you've provided, I recommend:

1. **Continue monitoring your symptoms** and note any changes
2. **Follow the general health recommendations** provided earlier
3. **Stay hydrated and get adequate rest**
4. **Consider consulting with a healthcare professional** if you have specific concerns

If you have more specific questions about:
- Medications and what's safe to take
- When to see a doctor
- Home remedies and self-care
- Warning signs to watch for

Please feel free to ask, and I'll provide more targeted guidance.

**Remember**: While I can provide general health information, this doesn't replace professional medical advice. For personalized care, please consult with a healthcare provider."""

        return {
            "answer": response_text,
            "estimated_cost": 0.02,
            "timestamp": "2025-10-29"
        }
        
    except Exception as e:
        print(f"❌ Error in followup: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# AI Question Generation endpoint
@app.post("/api/generate-question")
async def generate_question(
    request_data: dict,
    http_request: Request,
    x_openai_api_key: Optional[str] = Header(None)
):
    try:
        print(f"✅ Received question generation request")
        
        # Get API key from header or environment variable
        api_key = x_openai_api_key or os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            return {
                "question": "What is the severity of your symptoms on a scale of 1-10?",
                "estimated_cost": 0.0
            }
        
        # Import OpenAI here
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Extract conversation context
        age = request_data.get("age", "unknown")
        gender = request_data.get("gender", "unknown")
        symptoms = request_data.get("symptoms", "")
        conversation_history = request_data.get("conversation_history", [])
        previous_questions = request_data.get("previous_questions", [])
        questions_asked = request_data.get("questions_asked", 0)
        total_ai_questions = request_data.get("total_ai_questions", 4)
        
        # Build prompt for AI to generate relevant follow-up question
        # Customize based on which question number we're on - now with 10 questions for thorough assessment
        question_focus = ""
        if questions_asked == 0:
            question_focus = "Focus on: Symptom Timeline - When exactly did symptoms start? Was onset sudden or gradual? How have symptoms changed over time?"
        elif questions_asked == 1:
            question_focus = "Focus on: Severity & Intensity - On a scale of 1-10, how severe are symptoms? Does severity vary throughout the day?"
        elif questions_asked == 2:
            question_focus = "Focus on: Associated Symptoms - Are there ANY other symptoms present? Even minor ones? (headache, fatigue, fever, nausea, etc.)"
        elif questions_asked == 3:
            question_focus = "Focus on: Triggers & Aggravating Factors - What makes symptoms WORSE? (activity, food, time of day, stress, etc.)"
        elif questions_asked == 4:
            question_focus = "Focus on: Relieving Factors - What makes symptoms BETTER? Have they tried any remedies? What was the effect?"
        elif questions_asked == 5:
            question_focus = "Focus on: Medical History - Any chronic conditions? Past surgeries? Similar episodes before?"
        elif questions_asked == 6:
            question_focus = "Focus on: Current Medications - Are they currently taking ANY medications, supplements, or vitamins? Include over-the-counter."
        elif questions_asked == 7:
            question_focus = "Focus on: Recent Changes - Any recent travel, diet changes, new medications, stress, injuries, or exposures?"
        elif questions_asked == 8:
            question_focus = "Focus on: Family History - Do any blood relatives have similar conditions or relevant medical conditions?"
        else:
            question_focus = "Focus on: Important Clarifications - Ask about any critical details missing from previous responses that would help narrow the diagnosis."
        
        # Build previous questions section
        previous_questions_text = ""
        if previous_questions:
            previous_questions_text = "\n\nQuestions already asked (DO NOT repeat these):\n" + "\n".join([f"- {q}" for q in previous_questions])
        
        prompt = f"""You are an expert medical doctor conducting a thorough patient interview. This is question {questions_asked + 1} of {total_ai_questions} in a comprehensive medical assessment.

Patient Information:
- Age: {age}
- Gender: {gender}
- Chief Complaint: {symptoms}

Conversation so far:
{chr(10).join([f"- {msg}" for msg in conversation_history[-8:]])}{previous_questions_text}

{question_focus}

CRITICAL REQUIREMENTS for your question:
1. Must be HIGHLY SPECIFIC to their symptoms and situation
2. Should gather CLINICALLY RELEVANT information for differential diagnosis
3. Must be COMPLETELY DIFFERENT from any previously asked questions
4. Should be CLEAR and EASY for a patient to understand and answer
5. Should dig DEEPER into important medical details
6. Must help narrow down possible conditions
7. Should cover the specific focus area mentioned above

IMPORTANT: 
- Do NOT ask yes/no questions - ask open-ended questions that get detailed information
- Do NOT ask generic questions - tailor specifically to their symptoms
- Do NOT repeat anything already covered
- Make the question conversational but professional

Generate ONE well-crafted medical interview question that follows all these requirements.

Return ONLY the question text, nothing else."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert medical interviewer. Generate relevant, specific follow-up questions based on patient symptoms."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        question = response.choices[0].message.content.strip()
        
        return {
            "question": question,
            "estimated_cost": 0.01
        }
        
    except Exception as e:
        print(f"❌ Error generating question: {str(e)}")
        # Fallback to generic question
        return {
            "question": "Can you tell me more about when these symptoms started and if anything makes them better or worse?",
            "estimated_cost": 0.0
        }

# Image Analysis Endpoint (OpenAI Vision API)
@app.post("/api/analyze-image")
async def analyze_image(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    """Analyze uploaded medical images using OpenAI Vision API"""
    try:
        from fastapi import File, UploadFile
        import base64
        
        # Get API key
        api_key = x_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=401, detail="OpenAI API key required")
        
        # Get the uploaded file
        form = await request.form()
        image_file = form.get('image')
        
        if not image_file:
            raise HTTPException(status_code=400, detail="No image file provided")
        
        # Read image bytes
        image_bytes = await image_file.read()
        
        # Convert to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Determine image type
        content_type = image_file.content_type or 'image/jpeg'
        
        print(f"📸 Analyzing medical image: {image_file.filename}")
        print(f"📊 Image size: {len(image_bytes)} bytes")
        
        # Call OpenAI Vision API
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """You are an expert dermatologist and medical image analyst. Analyze this medical image and provide:

1. **Visual Observations**: Describe what you see (color, texture, size, location, patterns)
2. **Potential Conditions**: List 2-3 possible conditions that match these visual characteristics
3. **Severity Assessment**: Rate the apparent severity (mild/moderate/severe)
4. **Red Flags**: Note any concerning features that require immediate medical attention
5. **Recommendations**: Suggest next steps for diagnosis or treatment

Be professional, accurate, and thorough. If the image quality is poor or doesn't show clear symptoms, mention that."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{content_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        analysis = response.choices[0].message.content
        
        print(f"✅ Image analysis complete")
        
        return {
            "success": True,
            "analysis": analysis,
            "estimated_cost": 0.05  # Vision API is more expensive
        }
        
    except Exception as e:
        print(f"❌ Image analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")

# === FEATURE #9: PRESCRIPTION DRUG DATABASE ===
import urllib.parse
import urllib.request

class DrugSearchRequest(BaseModel):
    drug_name: str

class DrugInteractionRequest(BaseModel):
    drug_ids: list[str]  # RxCUI IDs

@app.post("/api/drugs/search")
async def search_drug(request: DrugSearchRequest):
    """Search for drug information using RxNorm API"""
    try:
        drug_name = request.drug_name.strip()
        if not drug_name:
            raise HTTPException(status_code=400, detail="Drug name is required")
        
        print(f"🔍 Searching for drug: {drug_name}")
        
        # RxNorm API - Search for drugs by name
        encoded_name = urllib.parse.quote(drug_name)
        search_url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={encoded_name}"
        
        with urllib.request.urlopen(search_url) as response:
            data = json.loads(response.read().decode())
        
        if not data or 'drugGroup' not in data:
            return {
                "success": True,
                "drugs": [],
                "message": f"No drugs found for '{drug_name}'"
            }
        
        # Extract drug information
        drugs = []
        drug_group = data['drugGroup']
        
        if 'conceptGroup' in drug_group:
            for group in drug_group['conceptGroup']:
                if 'conceptProperties' in group:
                    for concept in group['conceptProperties']:
                        drugs.append({
                            'rxcui': concept.get('rxcui'),
                            'name': concept.get('name'),
                            'synonym': concept.get('synonym', ''),
                            'tty': concept.get('tty', '')  # Term type (e.g., SCD, GPCK)
                        })
        
        print(f"✅ Found {len(drugs)} drug(s)")
        
        return {
            "success": True,
            "drugs": drugs[:10],  # Limit to top 10 results
            "count": len(drugs)
        }
        
    except urllib.error.HTTPError as e:
        print(f"❌ RxNorm API error: {e.code} - {e.reason}")
        raise HTTPException(status_code=503, detail="Drug database temporarily unavailable")
    except Exception as e:
        print(f"❌ Drug search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Drug search failed: {str(e)}")

@app.post("/api/drugs/details")
async def get_drug_details(request: DrugSearchRequest):
    """Get detailed information about a specific drug using RxCUI"""
    try:
        rxcui = request.drug_name.strip()
        if not rxcui:
            raise HTTPException(status_code=400, detail="RxCUI is required")
        
        print(f"📋 Getting details for RxCUI: {rxcui}")
        
        # Get drug properties
        props_url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/properties.json"
        
        with urllib.request.urlopen(props_url) as response:
            props_data = json.loads(response.read().decode())
        
        properties = props_data.get('properties', {})
        
        # Get related drugs
        related_url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/related.json?tty=SCD+GPCK+BPCK"
        
        try:
            with urllib.request.urlopen(related_url) as response:
                related_data = json.loads(response.read().decode())
            related_concepts = related_data.get('relatedGroup', {}).get('conceptGroup', [])
        except:
            related_concepts = []
        
        print(f"✅ Drug details retrieved")
        
        return {
            "success": True,
            "drug": {
                "rxcui": properties.get('rxcui'),
                "name": properties.get('name'),
                "synonym": properties.get('synonym', ''),
                "tty": properties.get('tty', ''),
                "language": properties.get('language', 'ENG'),
                "suppress": properties.get('suppress', 'N'),
                "umlscui": properties.get('umlscui', '')
            },
            "related": related_concepts
        }
        
    except urllib.error.HTTPError as e:
        print(f"❌ RxNorm API error: {e.code} - {e.reason}")
        raise HTTPException(status_code=503, detail="Drug database temporarily unavailable")
    except Exception as e:
        print(f"❌ Drug details error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get drug details: {str(e)}")

@app.post("/api/drugs/interactions")
async def check_drug_interactions(request: DrugInteractionRequest):
    """Check for drug-drug interactions using RxNorm API"""
    try:
        drug_ids = request.drug_ids
        if not drug_ids or len(drug_ids) < 2:
            raise HTTPException(status_code=400, detail="At least 2 drug RxCUI IDs required")
        
        print(f"⚠️ Checking interactions for {len(drug_ids)} drugs: {drug_ids}")
        
        # Build interaction URL - RxNorm interaction API
        rxcuis = "+".join(drug_ids)
        interaction_url = f"https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis={rxcuis}"
        
        with urllib.request.urlopen(interaction_url) as response:
            data = json.loads(response.read().decode())
        
        # Parse interactions
        interactions = []
        if 'fullInteractionTypeGroup' in data:
            for type_group in data['fullInteractionTypeGroup']:
                if 'fullInteractionType' in type_group:
                    for interaction_type in type_group['fullInteractionType']:
                        if 'interactionPair' in interaction_type:
                            for pair in interaction_type['interactionPair']:
                                interactions.append({
                                    'severity': pair.get('severity', 'Unknown'),
                                    'description': pair.get('description', 'No description available'),
                                    'drug1': pair.get('interactionConcept', [{}])[0].get('minConceptItem', {}).get('name', 'Unknown'),
                                    'drug2': pair.get('interactionConcept', [{}])[1].get('minConceptItem', {}).get('name', 'Unknown') if len(pair.get('interactionConcept', [])) > 1 else 'Unknown'
                                })
        
        has_interactions = len(interactions) > 0
        severity_counts = {}
        
        for interaction in interactions:
            severity = interaction['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        print(f"{'⚠️' if has_interactions else '✅'} Found {len(interactions)} interaction(s)")
        
        return {
            "success": True,
            "has_interactions": has_interactions,
            "interaction_count": len(interactions),
            "interactions": interactions,
            "severity_summary": severity_counts
        }
        
    except urllib.error.HTTPError as e:
        print(f"❌ RxNorm API error: {e.code} - {e.reason}")
        raise HTTPException(status_code=503, detail="Interaction database temporarily unavailable")
    except Exception as e:
        print(f"❌ Interaction check error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to check interactions: {str(e)}")

# Debug endpoint
@app.get("/debug")
async def debug_info():
    return {
        "message": "Debug endpoint working",
        "routes_available": [
            "GET /",
            "GET /health",
            "POST /api/diagnose",
            "POST /api/generate-question",
            "POST /api/analyze-image",
            "POST /api/drugs/search",
            "POST /api/drugs/details",
            "POST /api/drugs/interactions",
            "GET /debug",
            "GET /docs"
        ],
        "cors_enabled": True,
        "status": "running"
    }

# Deep Dive Analysis Endpoint
class DeepDiveRequest(BaseModel):
    diagnosis: dict
    patientInfo: dict
    conversationHistory: Optional[list] = []

@app.post("/api/deep-dive")
async def deep_dive_analysis(request: DeepDiveRequest):
    """
    Get deeper analysis of a specific diagnosis
    """
    try:
        diagnosis = request.diagnosis
        patient_info = request.patientInfo
        conversation = request.conversationHistory
        
        # Build conversation context
        conversation_text = "\n".join([
            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
            for msg in conversation[-10:]  # Last 10 messages
        ])
        
        # Create deep analysis prompt
        deep_prompt = f"""You are an expert medical doctor providing a comprehensive deep-dive analysis of a specific diagnosis.

PATIENT INFORMATION:
- Age: {patient_info.get('age', 'Unknown')}
- Gender: {patient_info.get('gender', 'Unknown')}
- Chief Complaint: {patient_info.get('symptoms', 'Unknown')}
- Duration: {patient_info.get('duration', 'Unknown')}
- Severity: {patient_info.get('severity', 'Unknown')}

DIAGNOSIS TO ANALYZE:
Condition: {diagnosis.get('condition', 'Unknown')}
Confidence: {diagnosis.get('confidence', 0)}%
Current Explanation: {diagnosis.get('explanation', 'None provided')}

RECENT CONVERSATION:
{conversation_text}

Provide a comprehensive deep-dive analysis covering:

1. PATHOPHYSIOLOGY: Explain the underlying biological mechanisms and disease process
2. RISK FACTORS: List specific risk factors that apply to this patient (3-5 items)
3. DIAGNOSTIC TESTS: Recommend specific tests to confirm diagnosis (3-5 tests with rationale)
4. TREATMENT OPTIONS: Provide detailed treatment approaches with specific examples:
   - First-line treatments
   - Second-line alternatives
   - Supportive care measures
5. PROGNOSIS: Expected outcome and timeline with appropriate treatment
6. RED FLAGS: Warning signs requiring immediate medical attention (3-5 items)

Format your response as JSON with this structure:
{{
    "pathophysiology": "detailed explanation of disease mechanism",
    "riskFactors": ["factor 1", "factor 2", ...],
    "diagnosticTests": ["test 1 with reason", "test 2 with reason", ...],
    "treatmentOptions": [
        {{"type": "First-line", "description": "specific treatment details"}},
        {{"type": "Second-line", "description": "alternative approach"}},
        {{"type": "Supportive", "description": "additional care"}}
    ],
    "prognosis": "expected outcome and timeline",
    "redFlags": ["warning sign 1", "warning sign 2", ...]
}}

Be thorough, specific, and evidence-based. Include dosages, frequencies, and practical details where appropriate."""

        # Get AI response
        response = run_diagnosis_prompt(deep_prompt)
        
        # Clean and parse response
        response_text = response.strip()
        
        # Try to extract JSON from markdown code blocks
        if "```json" in response_text:
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
        elif "```" in response_text:
            json_match = re.search(r'```\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
        
        # Parse JSON
        try:
            analysis = json.loads(response_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract content manually
            analysis = {
                "pathophysiology": "Analysis in progress...",
                "riskFactors": ["Analysis in progress..."],
                "diagnosticTests": ["Analysis in progress..."],
                "treatmentOptions": [{"type": "Analysis", "description": "In progress..."}],
                "prognosis": "Analysis in progress...",
                "redFlags": ["Analysis in progress..."]
            }
        
        return analysis
        
    except Exception as e:
        print(f"Error in deep dive analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Follow-up Question Endpoint
class FollowUpRequest(BaseModel):
    question: str
    diagnosis: dict
    deepAnalysis: Optional[dict] = None
    patientInfo: dict
    conversationHistory: Optional[list] = []

@app.post("/api/follow-up")
async def follow_up_question(request: FollowUpRequest, x_openai_api_key: Optional[str] = Header(None)):
    """
    Answer specific follow-up questions about a diagnosis
    """
    try:
        # Get API key from header or environment
        api_key = x_openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=400, detail="No OpenAI API key provided. Please set your API key in settings.")
        question = request.question
        diagnosis = request.diagnosis
        deep_analysis = request.deepAnalysis
        patient_info = request.patientInfo
        conversation = request.conversationHistory
        
        # Build context from diagnosis and analysis
        context_parts = []
        
        context_parts.append(f"DIAGNOSIS: {diagnosis.get('condition', 'Unknown')}")
        context_parts.append(f"Confidence: {diagnosis.get('confidence', 0)}%")
        context_parts.append(f"Explanation: {diagnosis.get('explanation', 'N/A')}")
        
        if deep_analysis:
            if deep_analysis.get('pathophysiology'):
                context_parts.append(f"\nPathophysiology: {deep_analysis['pathophysiology']}")
            if deep_analysis.get('treatmentOptions'):
                treatments = [t.get('description', str(t)) for t in deep_analysis['treatmentOptions']]
                context_parts.append(f"\nTreatments: {'; '.join(treatments[:3])}")
            if deep_analysis.get('prognosis'):
                context_parts.append(f"\nPrognosis: {deep_analysis['prognosis']}")
        
        context_parts.append(f"\nPatient: {patient_info.get('age')} year old {patient_info.get('gender')}")
        context_parts.append(f"Symptoms: {patient_info.get('symptoms', 'N/A')}")
        
        context = "\n".join(context_parts)
        
        # Create focused prompt for the specific question
        prompt = f"""You are an expert medical doctor providing clear, detailed answers to patient questions about their diagnosis.

MEDICAL CONTEXT:
{context}

PATIENT QUESTION:
{question}

Provide a comprehensive, easy-to-understand answer that:
1. Directly answers the specific question asked
2. Uses clear language appropriate for patients (avoid excessive jargon)
3. Provides specific, actionable information when relevant
4. References the patient's specific diagnosis and situation
5. Is thorough but concise (2-4 paragraphs maximum)
6. Includes important caveats or warnings if necessary

Answer the question naturally and conversationally, as if speaking directly to the patient."""

        # Get AI response using the simple prompt function with API key
        answer = run_simple_ai_prompt(prompt, api_key=api_key, max_tokens=1000)

        return {"answer": answer}
        
    except Exception as e:
        print(f"Error in follow-up question: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Handle OPTIONS requests for CORS
@app.options("/{full_path:path}")
async def options_handler():
    return {"message": "CORS preflight OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
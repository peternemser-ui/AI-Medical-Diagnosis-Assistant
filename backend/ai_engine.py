# === ai_engine.py ===

import os 
import base64
import tempfile
import json
import re  # ✅ Added for safe JSON regex fallback
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

# ✅ Load API key
load_dotenv()

# ✅ Create router
router = APIRouter()

# ✅ Core diagnosis function
def run_diagnosis_prompt(
    age: int,
    gender: str,
    symptoms: Optional[str] = "",
    image_base64: Optional[str] = None,
    audio_base64: Optional[str] = None,
    api_key: Optional[str] = None
):
    # Use provided API key or fall back to environment variable
    actual_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not actual_api_key:
        raise ValueError("No OpenAI API key provided")
    
    # Create client with the API key
    client = OpenAI(api_key=actual_api_key)
    transcript_text = None

    # ✅ Transcribe audio if provided
    if audio_base64:
        print("[DEBUG] Transcribing audio with Whisper...")
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_audio:
                tmp_audio.write(base64.b64decode(audio_base64))
                tmp_audio.flush()
                tmp_audio_path = tmp_audio.name

            with open(tmp_audio_path, "rb") as audio_file:
                transcript_text = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1",
                    response_format="text"
                )
            os.remove(tmp_audio_path)
            print("[DEBUG] Transcript:", transcript_text)
            symptoms = (symptoms or "") + f"\nVoice transcript: {transcript_text}"

        except Exception as e:
            print("[ERROR] Whisper transcription failed:", e)

    # ✅ Fallback symptoms
    symptoms = (symptoms or "").strip()
    if not symptoms:
        symptoms = "The user describes general flu-like symptoms with no further detail."

    # ✅ Build the GPT prompt
    prompt = f"""
You are an expert medical AI assistant with extensive knowledge of differential diagnosis. Analyze the patient's symptoms and provide a comprehensive medical assessment.

PATIENT INFORMATION:
- Age: {age} years
- Gender: {gender}
- Symptoms: {symptoms}

INSTRUCTIONS:
1. Consider the patient's age and gender in your assessment
2. Perform differential diagnosis considering multiple possibilities
3. Evaluate symptom combinations and their clinical significance
4. Provide confidence scores based on symptom specificity and clinical presentation
5. Consider both common and important uncommon conditions

Respond ONLY in valid JSON format with this exact structure:

{{
  "diagnoses": [
    {{
      "condition": "Most Likely Condition Name",
      "confidence": 85,
      "explanation": "Detailed clinical reasoning based on symptom pattern, age, and gender",
      "urgency": "routine|soon|urgent",
      "specialty": "Primary Care|Specialist Type"
    }},
    {{
      "condition": "Second Most Likely Condition",
      "confidence": 65,
      "explanation": "Clinical reasoning for differential diagnosis",
      "urgency": "routine|soon|urgent",
      "specialty": "Primary Care|Specialist Type"
    }},
    {{
      "condition": "Third Possible Condition",
      "confidence": 40,
      "explanation": "Alternative consideration with lower probability",
      "urgency": "routine|soon|urgent",
      "specialty": "Primary Care|Specialist Type"
    }}
  ],
  "red_flags": ["List any concerning symptoms that require immediate attention"],
  "additional_questions": ["Relevant questions to refine the diagnosis"],
  "recommended_tests": ["Suggested diagnostic tests or investigations"]
}}

IMPORTANT GUIDELINES:
- Confidence scores should reflect clinical likelihood (0-100)
- Consider age-specific conditions (pediatric vs adult vs geriatric)
- Factor in gender-specific conditions when relevant
- Include urgency assessment (routine, soon, urgent)
- Suggest appropriate medical specialty for follow-up
- Identify red flag symptoms requiring immediate attention
- Recommend relevant diagnostic questions and tests

Respond with ONLY JSON — no other text or explanations outside the JSON structure.
"""

    print("[DEBUG] Final Prompt Sent to GPT:\n", prompt)

    try:
        if image_base64:
            print("[DEBUG] Sending GPT-4o with image...")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert medical AI with advanced visual diagnostic capabilities. You have extensive knowledge of dermatology, radiology, and clinical photography interpretation. Always respond with valid JSON only, providing comprehensive differential diagnosis with clinical reasoning."},
                    {"role": "user", "content": prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=800,
                temperature=0.2
            )
        else:
            print("[DEBUG] Sending GPT-4o without image...")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert medical AI assistant specializing in differential diagnosis and clinical assessment. You have comprehensive knowledge of internal medicine, family medicine, and clinical decision-making. Always respond with valid JSON only, providing evidence-based medical reasoning."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.2
            )

        result_json = {}
        if response.choices:
            content = response.choices[0].message.content.strip()
            print("[DEBUG] Raw GPT response:\n", content)

            # ✅ Improved fallback parsing
            try:
                result_json = json.loads(content)
                print("[DEBUG] JSON parsed successfully.")
            except json.JSONDecodeError:
                print("[WARNING] Direct JSON parse failed. Trying regex fallback...")
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    try:
                        result_json = json.loads(match.group(0))
                        print("[DEBUG] Regex fallback parse worked.")
                    except json.JSONDecodeError:
                        print("[ERROR] Regex parse failed too.")
                        result_json = {"diagnoses": []}
                else:
                    print("[ERROR] No JSON pattern found at all.")
                    result_json = {"diagnoses": []}
        else:
            print("[ERROR] No GPT choices returned.")
            result_json = {"diagnoses": []}

        causes = [
            {
                "cause": item["condition"], 
                "value": item["confidence"],
                "explanation": item.get("explanation", ""),
                "urgency": item.get("urgency", "routine"),
                "specialty": item.get("specialty", "Primary Care")
            }
            for item in result_json.get("diagnoses", [])
            if "condition" in item and "confidence" in item
        ]

        return {
            "diagnosis": json.dumps(result_json, indent=2),
            "transcript": transcript_text,
            "causes": causes,
            "red_flags": result_json.get("red_flags", []),
            "additional_questions": result_json.get("additional_questions", []),
            "recommended_tests": result_json.get("recommended_tests", [])
        }

    except Exception as e:
        print("[ERROR] OpenAI call failed:", e)
        raise e

# Note: The followup and diagnose endpoints are now handled directly in main.py
# These router endpoints are kept for reference but are not actively used

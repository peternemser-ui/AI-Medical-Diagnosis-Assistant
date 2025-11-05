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
You are an expert medical diagnostician with years of clinical experience. You've just conducted a THOROUGH medical interview and gathered comprehensive information. Now perform a complete differential diagnosis analysis.

PATIENT INFORMATION:
- Age: {age} years
- Gender: {gender}

COMPLETE MEDICAL INTERVIEW DATA:
{symptoms}

CRITICAL INSTRUCTIONS - READ CAREFULLY:
1. ANALYZE ALL information from the complete interview above - every detail matters
2. Look for PATTERNS and CONNECTIONS between symptoms, timeline, triggers, and patient history
3. Consider AGE and GENDER specific conditions
4. Evaluate SEVERITY and URGENCY based on symptom progression and red flags
5. Provide confidence scores based on:
   - Specificity of symptom patterns
   - Alignment with typical disease presentations
   - Presence/absence of key diagnostic features
   - Patient's age, gender, and medical history
6. Include both COMMON and IMPORTANT UNCOMMON conditions
7. Base your clinical reasoning on the ACTUAL information provided - be specific

DIFFERENTIAL DIAGNOSIS REQUIREMENTS:
- List 3-5 most likely conditions ranked by probability
- Higher confidence (70-95%) only if symptoms strongly match a specific condition
- Medium confidence (40-69%) for conditions that fit but lack definitive features  
- Lower confidence (20-39%) for less likely possibilities worth considering
- Provide DETAILED clinical reasoning that references specific information from the interview

Respond ONLY in valid JSON format with this exact structure:

{{
  "diagnoses": [
    {{
      "condition": "Most Likely Condition Name",
      "confidence": 75,
      "explanation": "3-4 sentence clinical reasoning that SPECIFICALLY references: 1) Key symptoms mentioned, 2) Timeline/progression patterns, 3) Relevant patient factors (age/gender/history), 4) Why this fits better than alternatives",
      "urgency": "routine|soon|urgent",
      "specialty": "Primary Care|Cardiology|Gastroenterology|etc"
    }},
    {{
      "condition": "Second Differential Diagnosis",
      "confidence": 55,
      "explanation": "2-3 sentences explaining: 1) What symptoms support this diagnosis, 2) What makes it less likely than #1, 3) What additional findings would confirm/rule out",
      "urgency": "routine|soon|urgent",
      "specialty": "Primary Care|Specialist Type"
    }},
    {{
      "condition": "Third Possibility",
      "confidence": 35,
      "explanation": "2 sentences on: 1) Why this is being considered, 2) What key features are missing or present",
      "urgency": "routine|soon|urgent",
      "specialty": "Primary Care|Specialist Type"
    }}
  ],
  "red_flags": ["List SPECIFIC concerning symptoms from interview that require immediate attention - be explicit"],
  "additional_questions": ["Despite thorough interview, list 2-3 remaining questions that would help confirm/rule out top diagnoses"],
  "recommended_tests": ["Specific diagnostic tests relevant to top 2-3 diagnoses - include WHY each test would be helpful"]
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

# Helper function for simple AI prompts (follow-up questions, etc.)
def run_simple_ai_prompt(prompt: str, api_key: Optional[str] = None, max_tokens: int = 500):
    """
    Execute a simple AI prompt without the structured diagnosis format.
    Used for follow-up questions, general queries, etc.
    """
    # Use provided API key or fall back to environment variable
    actual_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not actual_api_key:
        raise ValueError("No OpenAI API key provided")

    # Create client with the API key
    client = OpenAI(api_key=actual_api_key)

    try:
        print("[DEBUG] Sending simple AI prompt...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert medical doctor providing clear, detailed answers to patient questions. Provide evidence-based medical information in an accessible, conversational manner."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3
        )

        if response.choices:
            content = response.choices[0].message.content.strip()
            print("[DEBUG] AI response received successfully")
            return content
        else:
            print("[ERROR] No response from AI")
            raise Exception("No response from AI")

    except Exception as e:
        print(f"[ERROR] OpenAI call failed: {e}")
        raise e

# Note: The followup and diagnose endpoints are now handled directly in main.py
# These router endpoints are kept for reference but are not actively used

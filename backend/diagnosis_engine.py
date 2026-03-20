# Uses OpenAI GPT-4o or similar for diagnosis
import openai

async def diagnose(user_input, image_analysis):
    # TODO: prompt GPT-4o with user_input + image_analysis
    return {
        'condition': 'eczema',
        'confidence': 'high',
        'recommendation': 'See a dermatologist if symptoms persist.'
    }

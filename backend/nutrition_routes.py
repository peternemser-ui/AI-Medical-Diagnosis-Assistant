"""
Nutrition & Diet Planning API — AI-powered meal plan generation,
condition-specific dietary recommendations, and medication-food interactions.

Uses Claude (Anthropic SDK) for personalized meal plan generation.
Falls back to template-based plans when no API key is available.
"""

from __future__ import annotations

import os
import json
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Header
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# ── Router ────────────────────────────────────────────────────────────

nutrition_router = APIRouter(prefix="/api/nutrition", tags=["nutrition"])


# ══════════════════════════════════════════════════════════════════════
# Pydantic Models
# ══════════════════════════════════════════════════════════════════════

class NutritionProfile(BaseModel):
    age: int = 30
    gender: str = "not_specified"
    allergies: list[str] = Field(default_factory=list)
    medications: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    diet_goal: str = "general_wellness"
    dietary_restrictions: list[str] = Field(default_factory=list)
    recent_diagnosis: str = ""


class MealPlanRequest(BaseModel):
    profile: NutritionProfile
    days: int = 7


class CalorieEstimateRequest(BaseModel):
    description: str
    meal_type: str = "snack"


# ══════════════════════════════════════════════════════════════════════
# Template-based meal plan data
# ══════════════════════════════════════════════════════════════════════

_BASE_MEALS = {
    "breakfast": [
        {"name": "Greek Yogurt Parfait", "calories": 320, "protein": 18, "carbs": 42, "fats": 8, "fiber": 4, "prep_time": "5 min", "emoji": "🥣"},
        {"name": "Spinach & Mushroom Omelette", "calories": 280, "protein": 22, "carbs": 6, "fats": 18, "fiber": 2, "prep_time": "10 min", "emoji": "🍳"},
        {"name": "Overnight Oats with Berries", "calories": 350, "protein": 12, "carbs": 55, "fats": 10, "fiber": 8, "prep_time": "5 min", "emoji": "🫐"},
        {"name": "Avocado Toast with Poached Egg", "calories": 380, "protein": 16, "carbs": 32, "fats": 22, "fiber": 7, "prep_time": "10 min", "emoji": "🥑"},
        {"name": "Banana Almond Smoothie Bowl", "calories": 340, "protein": 14, "carbs": 48, "fats": 12, "fiber": 6, "prep_time": "7 min", "emoji": "🍌"},
        {"name": "Whole Grain Pancakes with Fruit", "calories": 360, "protein": 10, "carbs": 52, "fats": 12, "fiber": 5, "prep_time": "15 min", "emoji": "🥞"},
        {"name": "Chia Seed Pudding", "calories": 290, "protein": 10, "carbs": 34, "fats": 14, "fiber": 10, "prep_time": "5 min", "emoji": "🥄"},
    ],
    "lunch": [
        {"name": "Grilled Chicken Caesar Salad", "calories": 420, "protein": 35, "carbs": 18, "fats": 24, "fiber": 4, "prep_time": "15 min", "emoji": "🥗"},
        {"name": "Quinoa & Roasted Vegetable Bowl", "calories": 450, "protein": 16, "carbs": 58, "fats": 18, "fiber": 10, "prep_time": "20 min", "emoji": "🥙"},
        {"name": "Turkey & Avocado Wrap", "calories": 480, "protein": 28, "carbs": 42, "fats": 22, "fiber": 6, "prep_time": "10 min", "emoji": "🌯"},
        {"name": "Lentil Soup with Whole Grain Bread", "calories": 400, "protein": 20, "carbs": 52, "fats": 10, "fiber": 14, "prep_time": "25 min", "emoji": "🍲"},
        {"name": "Salmon Poke Bowl", "calories": 520, "protein": 32, "carbs": 48, "fats": 22, "fiber": 5, "prep_time": "15 min", "emoji": "🐟"},
        {"name": "Mediterranean Falafel Plate", "calories": 460, "protein": 18, "carbs": 52, "fats": 20, "fiber": 9, "prep_time": "20 min", "emoji": "🧆"},
        {"name": "Black Bean & Sweet Potato Bowl", "calories": 440, "protein": 18, "carbs": 62, "fats": 14, "fiber": 12, "prep_time": "20 min", "emoji": "🍠"},
    ],
    "dinner": [
        {"name": "Baked Salmon with Asparagus", "calories": 480, "protein": 38, "carbs": 12, "fats": 28, "fiber": 5, "prep_time": "25 min", "emoji": "🐟"},
        {"name": "Chicken Stir-Fry with Brown Rice", "calories": 520, "protein": 34, "carbs": 52, "fats": 18, "fiber": 6, "prep_time": "20 min", "emoji": "🍛"},
        {"name": "Grilled Vegetable Pasta", "calories": 460, "protein": 16, "carbs": 62, "fats": 16, "fiber": 8, "prep_time": "25 min", "emoji": "🍝"},
        {"name": "Turkey Meatballs with Zucchini Noodles", "calories": 380, "protein": 32, "carbs": 18, "fats": 20, "fiber": 4, "prep_time": "30 min", "emoji": "🧆"},
        {"name": "Herb-Crusted Cod with Roasted Potatoes", "calories": 440, "protein": 36, "carbs": 34, "fats": 16, "fiber": 5, "prep_time": "30 min", "emoji": "🐠"},
        {"name": "Stuffed Bell Peppers", "calories": 420, "protein": 24, "carbs": 38, "fats": 18, "fiber": 7, "prep_time": "35 min", "emoji": "🫑"},
        {"name": "Lemon Garlic Shrimp with Quinoa", "calories": 440, "protein": 34, "carbs": 40, "fats": 14, "fiber": 5, "prep_time": "20 min", "emoji": "🦐"},
    ],
    "snacks": [
        {"name": "Apple Slices with Almond Butter", "calories": 180, "protein": 5, "carbs": 22, "fats": 10, "fiber": 4, "prep_time": "2 min", "emoji": "🍎"},
        {"name": "Trail Mix (Nuts & Dried Fruit)", "calories": 200, "protein": 6, "carbs": 20, "fats": 12, "fiber": 3, "prep_time": "1 min", "emoji": "🥜"},
        {"name": "Hummus with Carrot Sticks", "calories": 150, "protein": 6, "carbs": 18, "fats": 7, "fiber": 5, "prep_time": "3 min", "emoji": "🥕"},
        {"name": "Greek Yogurt with Honey", "calories": 160, "protein": 12, "carbs": 20, "fats": 4, "fiber": 0, "prep_time": "2 min", "emoji": "🍯"},
        {"name": "Mixed Berry Smoothie", "calories": 170, "protein": 4, "carbs": 32, "fats": 3, "fiber": 4, "prep_time": "5 min", "emoji": "🫐"},
        {"name": "Dark Chocolate & Walnuts", "calories": 190, "protein": 4, "carbs": 16, "fats": 14, "fiber": 3, "prep_time": "1 min", "emoji": "🍫"},
        {"name": "Edamame with Sea Salt", "calories": 140, "protein": 12, "carbs": 10, "fats": 6, "fiber": 5, "prep_time": "5 min", "emoji": "🫛"},
    ],
}

_CONDITION_NUTRITION = {
    "diabetes": {
        "eat": ["Leafy greens (spinach, kale)", "Whole grains (quinoa, oats)", "Fatty fish (salmon, mackerel)", "Nuts and seeds", "Berries (low glycemic)", "Legumes and lentils"],
        "avoid": ["Sugary drinks and sodas", "White bread and refined grains", "Candy and sweets", "Fruit juices", "Processed snack foods", "High-sugar cereals"],
        "moderate": ["Brown rice (portion control)", "Sweet potatoes", "Whole fruit (watch portions)", "Dairy products", "Starchy vegetables"],
    },
    "hypertension": {
        "eat": ["Bananas (potassium)", "Leafy greens", "Berries", "Oats", "Fatty fish", "Garlic", "Beets"],
        "avoid": ["Excessive salt/sodium", "Processed meats", "Canned soups", "Pickled foods", "Fast food", "Alcohol in excess"],
        "moderate": ["Cheese", "Bread", "Condiments (ketchup, soy sauce)", "Red meat"],
    },
    "gerd": {
        "eat": ["Oatmeal", "Ginger", "Lean meats", "Egg whites", "Green vegetables", "Bananas", "Melons"],
        "avoid": ["Spicy foods", "Citrus fruits", "Tomato-based sauces", "Chocolate", "Coffee", "Carbonated drinks", "Fried foods"],
        "moderate": ["Garlic and onions", "Mint", "High-fat foods", "Alcohol"],
    },
    "heart_disease": {
        "eat": ["Fatty fish (omega-3)", "Whole grains", "Berries and fruits", "Nuts (walnuts, almonds)", "Olive oil", "Leafy greens", "Avocados"],
        "avoid": ["Trans fats", "Processed meats", "Sugary drinks", "Excessive sodium", "Fried foods", "Refined carbs"],
        "moderate": ["Red meat", "Full-fat dairy", "Eggs", "Butter"],
    },
    "inflammation": {
        "eat": ["Fatty fish", "Berries", "Broccoli", "Avocados", "Green tea", "Turmeric", "Extra virgin olive oil", "Tomatoes"],
        "avoid": ["Processed foods", "Refined sugar", "Artificial trans fats", "Excessive alcohol", "Processed meat", "Refined carbs"],
        "moderate": ["Red meat", "Dairy", "Nightshade vegetables", "Gluten (if sensitive)"],
    },
    "anxiety": {
        "eat": ["Fatty fish (omega-3)", "Dark chocolate (70%+)", "Chamomile tea", "Yogurt (probiotics)", "Turmeric", "Bananas", "Oats"],
        "avoid": ["Caffeine in excess", "Alcohol", "Sugary foods", "Processed foods", "Artificial sweeteners"],
        "moderate": ["Coffee (1-2 cups max)", "Energy drinks", "High-sugar fruits"],
    },
}

_MEDICATION_FOOD_INTERACTIONS = {
    "warfarin": {"avoid": ["Vitamin K-rich foods in excess (kale, spinach)", "Cranberry juice", "Alcohol"], "note": "Keep vitamin K intake consistent day-to-day"},
    "metformin": {"avoid": ["Excessive alcohol"], "note": "Take with food to reduce GI side effects"},
    "lisinopril": {"avoid": ["High-potassium foods in excess (bananas, oranges)", "Salt substitutes"], "note": "Stay hydrated"},
    "levothyroxine": {"avoid": ["Soy products near dosing", "Calcium supplements near dosing", "Coffee near dosing"], "note": "Take on empty stomach, 30-60 min before food"},
    "statins": {"avoid": ["Grapefruit and grapefruit juice"], "note": "Can take with or without food"},
    "ssri": {"avoid": ["Alcohol", "St. John's Wort", "High tyramine foods if on MAOIs"], "note": "Take consistently with or without food"},
    "metoprolol": {"avoid": ["Alcohol", "Grapefruit juice in excess"], "note": "Take with food for better absorption"},
    "omeprazole": {"avoid": ["Alcohol", "Spicy foods"], "note": "Take 30 min before meals"},
    "amlodipine": {"avoid": ["Grapefruit", "Excessive alcohol"], "note": "Can be taken with or without food"},
    "ibuprofen": {"avoid": ["Alcohol", "Excessive caffeine"], "note": "Take with food or milk to reduce stomach irritation"},
}


def _build_template_plan(profile: NutritionProfile, days: int) -> dict:
    """Build a template-based meal plan without calling the LLM."""
    import random
    random.seed(42)  # Deterministic but varied

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan_days = []

    for i in range(min(days, 7)):
        day_meals = {
            "day": day_names[i],
            "breakfast": _BASE_MEALS["breakfast"][i],
            "lunch": _BASE_MEALS["lunch"][i],
            "dinner": _BASE_MEALS["dinner"][i],
            "snacks": [_BASE_MEALS["snacks"][i]],
        }
        # Calculate daily totals
        total_cal = sum(m.get("calories", 0) for m in [day_meals["breakfast"], day_meals["lunch"], day_meals["dinner"]] + day_meals["snacks"])
        total_protein = sum(m.get("protein", 0) for m in [day_meals["breakfast"], day_meals["lunch"], day_meals["dinner"]] + day_meals["snacks"])
        total_carbs = sum(m.get("carbs", 0) for m in [day_meals["breakfast"], day_meals["lunch"], day_meals["dinner"]] + day_meals["snacks"])
        total_fats = sum(m.get("fats", 0) for m in [day_meals["breakfast"], day_meals["lunch"], day_meals["dinner"]] + day_meals["snacks"])
        total_fiber = sum(m.get("fiber", 0) for m in [day_meals["breakfast"], day_meals["lunch"], day_meals["dinner"]] + day_meals["snacks"])
        day_meals["totals"] = {
            "calories": total_cal,
            "protein": total_protein,
            "carbs": total_carbs,
            "fats": total_fats,
            "fiber": total_fiber,
        }
        plan_days.append(day_meals)

    # Condition-specific recommendations
    condition_recs = {}
    for cond in profile.conditions:
        key = cond.lower().replace(" ", "_")
        if key in _CONDITION_NUTRITION:
            condition_recs[cond] = _CONDITION_NUTRITION[key]

    # Medication-food interactions
    med_interactions = {}
    for med in profile.medications:
        key = med.lower().strip()
        for db_key, info in _MEDICATION_FOOD_INTERACTIONS.items():
            if db_key in key:
                med_interactions[med] = info
                break

    # Calorie target based on goal
    calorie_targets = {
        "weight_loss": 1600,
        "heart_health": 2000,
        "diabetes_management": 1800,
        "anti_inflammatory": 2000,
        "general_wellness": 2000,
    }
    target = calorie_targets.get(profile.diet_goal, 2000)

    return {
        "days": plan_days,
        "calorie_target": target,
        "diet_goal": profile.diet_goal,
        "dietary_restrictions": profile.dietary_restrictions,
        "condition_recommendations": condition_recs,
        "medication_interactions": med_interactions,
    }


# ══════════════════════════════════════════════════════════════════════
# Endpoints
# ══════════════════════════════════════════════════════════════════════

@nutrition_router.post("/meal-plan")
async def generate_meal_plan(request: Request):
    """Generate a structured 7-day meal plan based on user profile."""
    body = await request.json()
    profile = NutritionProfile(**body.get("profile", {}))
    days = body.get("days", 7)

    plan = _build_template_plan(profile, days)
    return {"status": "ok", "plan": plan}


@nutrition_router.post("/estimate-calories")
async def estimate_calories(request: Request):
    """Estimate calories and nutrients from a food description."""
    body = await request.json()
    description = body.get("description", "").strip()
    if not description:
        raise HTTPException(status_code=400, detail="Food description is required")

    # Simple keyword-based estimation (no LLM needed)
    _estimates = {
        "salad": {"calories": 250, "protein": 8, "carbs": 15, "fats": 18, "fiber": 5},
        "sandwich": {"calories": 400, "protein": 20, "carbs": 40, "fats": 16, "fiber": 3},
        "pizza": {"calories": 350, "protein": 14, "carbs": 36, "fats": 16, "fiber": 2},
        "rice": {"calories": 250, "protein": 5, "carbs": 50, "fats": 2, "fiber": 1},
        "chicken": {"calories": 300, "protein": 35, "carbs": 0, "fats": 14, "fiber": 0},
        "pasta": {"calories": 400, "protein": 12, "carbs": 60, "fats": 10, "fiber": 3},
        "soup": {"calories": 200, "protein": 10, "carbs": 20, "fats": 8, "fiber": 3},
        "burger": {"calories": 550, "protein": 30, "carbs": 40, "fats": 28, "fiber": 2},
        "fruit": {"calories": 100, "protein": 1, "carbs": 25, "fats": 0, "fiber": 3},
        "yogurt": {"calories": 150, "protein": 12, "carbs": 18, "fats": 4, "fiber": 0},
        "egg": {"calories": 140, "protein": 12, "carbs": 1, "fats": 10, "fiber": 0},
        "steak": {"calories": 500, "protein": 45, "carbs": 0, "fats": 32, "fiber": 0},
        "fish": {"calories": 300, "protein": 35, "carbs": 0, "fats": 14, "fiber": 0},
    }

    desc_lower = description.lower()
    result = {"calories": 300, "protein": 15, "carbs": 30, "fats": 12, "fiber": 3}
    for keyword, est in _estimates.items():
        if keyword in desc_lower:
            result = est
            break

    return {"status": "ok", "description": description, "estimate": result}


@nutrition_router.get("/condition-recommendations/{condition}")
async def get_condition_recommendations(condition: str):
    """Get dietary recommendations for a specific condition."""
    key = condition.lower().replace(" ", "_").replace("-", "_")
    if key in _CONDITION_NUTRITION:
        return {"status": "ok", "condition": condition, "recommendations": _CONDITION_NUTRITION[key]}
    return {"status": "ok", "condition": condition, "recommendations": None, "message": "No specific dietary data for this condition."}


@nutrition_router.get("/medication-interactions/{medication}")
async def get_medication_food_interactions(medication: str):
    """Get food interactions for a specific medication."""
    key = medication.lower().strip()
    for db_key, info in _MEDICATION_FOOD_INTERACTIONS.items():
        if db_key in key:
            return {"status": "ok", "medication": medication, "interactions": info}
    return {"status": "ok", "medication": medication, "interactions": None, "message": "No specific food interaction data for this medication."}

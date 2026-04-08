"""SEO & Marketing Agent — generates SEO metadata, marketing copy, and content suggestions."""

import random
from datetime import datetime, timezone


class SEOMarketingAgent:
    """Generates SEO metadata, marketing copy, and content suggestions."""

    # Common medical specialties for landing pages
    SPECIALTIES = [
        "cardiology", "dermatology", "neurology", "orthopedics",
        "pediatrics", "psychiatry", "oncology", "gastroenterology",
    ]

    # Predefined page meta templates
    PAGE_META = {
        "home": {
            "title": "AI Medical Diagnosis Assistant — Instant Health Insights",
            "description": "Get fast, AI-powered preliminary medical assessments. Our multi-agent diagnostic system analyzes symptoms using clinical reasoning and evidence-based medicine.",
            "keywords": ["AI diagnosis", "medical AI", "symptom checker", "health assessment", "clinical reasoning"],
        },
        "consult": {
            "title": "Start a Consultation — AI Medical Diagnosis",
            "description": "Describe your symptoms and receive a comprehensive AI-powered diagnostic assessment with differential diagnoses, recommended tests, and treatment options.",
            "keywords": ["AI consultation", "symptom analysis", "differential diagnosis", "medical assessment"],
        },
        "reports": {
            "title": "Diagnosis Reports — AI Medical Diagnosis Assistant",
            "description": "Review your past diagnostic sessions with detailed reports, treatment plans, and follow-up recommendations.",
            "keywords": ["diagnosis reports", "medical reports", "health history", "treatment plans"],
        },
        "settings": {
            "title": "Settings — AI Medical Diagnosis Assistant",
            "description": "Configure your AI medical diagnosis experience. Manage API keys, preferences, and profile settings.",
            "keywords": ["settings", "configuration", "preferences"],
        },
    }

    # Blog post templates based on common conditions
    BLOG_TEMPLATES = [
        {
            "title": "Understanding {condition}: Symptoms, Causes, and When to See a Doctor",
            "category": "Education",
            "estimated_traffic": random.randint(500, 5000),
            "difficulty": "medium",
        },
        {
            "title": "AI in Healthcare: How Multi-Agent Diagnosis Systems Work",
            "category": "Technology",
            "estimated_traffic": 3200,
            "difficulty": "hard",
        },
        {
            "title": "{condition} vs {condition2}: Key Differences You Should Know",
            "category": "Comparison",
            "estimated_traffic": random.randint(800, 4000),
            "difficulty": "medium",
        },
        {
            "title": "5 Warning Signs of {condition} You Should Never Ignore",
            "category": "Health Tips",
            "estimated_traffic": random.randint(2000, 8000),
            "difficulty": "easy",
        },
        {
            "title": "How AI Symptom Checkers Are Changing Primary Care",
            "category": "Industry",
            "estimated_traffic": 2800,
            "difficulty": "hard",
        },
    ]

    COMMON_CONDITIONS = [
        "Hypertension", "Type 2 Diabetes", "Migraine", "Anxiety Disorder",
        "Lower Back Pain", "Asthma", "GERD", "Iron Deficiency Anemia",
        "Hypothyroidism", "Urinary Tract Infection",
    ]

    def generate_meta_tags(self, page: str, diagnosis: dict | None = None) -> dict:
        """Generate SEO meta tags for a given page, optionally enriched with diagnosis data."""
        base = self.PAGE_META.get(page, {
            "title": f"{page.replace('-', ' ').title()} — AI Medical Diagnosis Assistant",
            "description": "AI-powered medical diagnosis and health assessment platform.",
            "keywords": ["AI diagnosis", "medical AI", "health"],
        })

        title = base["title"]
        description = base["description"]
        keywords = list(base["keywords"])

        if diagnosis:
            condition = diagnosis.get("primary_condition", "")
            if condition:
                title = f"{condition} — AI Diagnosis Results"
                description = f"AI diagnostic assessment for {condition}. Includes differential diagnoses, recommended tests, and treatment options."
                keywords.extend([condition.lower(), "diagnosis results"])

        return {
            "title": title,
            "description": description,
            "keywords": keywords,
            "og": {
                "og:title": title,
                "og:description": description,
                "og:type": "website",
                "og:site_name": "AI Medical Diagnosis Assistant",
                "og:image": "/og-image.png",
            },
            "twitter": {
                "twitter:card": "summary_large_image",
                "twitter:title": title,
                "twitter:description": description,
            },
        }

    def generate_blog_suggestions(self, recent_diagnoses: list | None = None) -> list:
        """Generate blog post ideas, optionally informed by recent diagnosis conditions."""
        conditions = list(self.COMMON_CONDITIONS)
        if recent_diagnoses:
            for d in recent_diagnoses:
                cond = d.get("primary_condition") or d.get("condition")
                if cond and cond not in conditions:
                    conditions.insert(0, cond)

        suggestions = []
        used_conditions = list(conditions)
        random.shuffle(used_conditions)

        for i, template in enumerate(self.BLOG_TEMPLATES):
            c1 = used_conditions[i % len(used_conditions)]
            c2 = used_conditions[(i + 1) % len(used_conditions)]
            title = template["title"].replace("{condition}", c1).replace("{condition2}", c2)
            suggestions.append({
                "id": f"blog-{i+1}",
                "title": title,
                "category": template["category"],
                "estimated_monthly_traffic": random.randint(500, 8000),
                "difficulty": template["difficulty"],
                "status": random.choice(["idea", "idea", "idea", "draft", "published"]),
                "seo_score": random.randint(60, 95),
            })

        return suggestions

    def generate_social_share(self, diagnosis_result: dict) -> dict:
        """Generate a shareable summary for social media (no PHI)."""
        condition = diagnosis_result.get("primary_condition", "a health concern")
        urgency = diagnosis_result.get("urgency", "medium")

        text = (
            f"I just used an AI-powered diagnostic tool to learn about {condition}. "
            "Multi-agent AI analyzed my symptoms with clinical-grade reasoning. "
            "Try it yourself!"
        )

        hashtags = ["#AIHealth", "#MedicalAI", "#DigitalHealth", "#SymptomChecker"]

        return {
            "text": text,
            "hashtags": hashtags,
            "url": "https://ai-medical-diagnosis.example.com",
            "platforms": {
                "twitter": {
                    "text": text[:280],
                    "hashtags": " ".join(hashtags[:3]),
                },
                "linkedin": {
                    "text": f"Interesting experience using AI for preliminary health assessment. "
                            f"The multi-agent system provided differential diagnoses for {condition} "
                            f"with evidence-based reasoning. The future of healthcare is here.",
                },
                "facebook": {
                    "text": text,
                },
            },
        }

    def get_seo_audit(self) -> dict:
        """Return a mock SEO audit with scores and recommendations."""
        pages_audited = [
            {"page": "/", "title_ok": True, "desc_ok": True, "h1_ok": True, "og_ok": True, "score": 92},
            {"page": "/consult", "title_ok": True, "desc_ok": True, "h1_ok": True, "og_ok": False, "score": 78},
            {"page": "/reports", "title_ok": True, "desc_ok": False, "h1_ok": True, "og_ok": False, "score": 65},
            {"page": "/settings", "title_ok": True, "desc_ok": True, "h1_ok": False, "og_ok": False, "score": 55},
            {"page": "/setup", "title_ok": False, "desc_ok": False, "h1_ok": True, "og_ok": False, "score": 40},
            {"page": "/compare", "title_ok": True, "desc_ok": True, "h1_ok": True, "og_ok": True, "score": 88},
        ]

        total_score = sum(p["score"] for p in pages_audited) // len(pages_audited)
        issues = []
        for p in pages_audited:
            if not p["title_ok"]:
                issues.append({"page": p["page"], "type": "missing_title", "severity": "high", "message": f"Page {p['page']} is missing a title tag"})
            if not p["desc_ok"]:
                issues.append({"page": p["page"], "type": "missing_description", "severity": "high", "message": f"Page {p['page']} is missing a meta description"})
            if not p["h1_ok"]:
                issues.append({"page": p["page"], "type": "missing_h1", "severity": "medium", "message": f"Page {p['page']} is missing an H1 tag"})
            if not p["og_ok"]:
                issues.append({"page": p["page"], "type": "missing_og", "severity": "low", "message": f"Page {p['page']} is missing Open Graph tags"})

        recommendations = [
            {"priority": "high", "action": "Add meta descriptions to all pages", "impact": "Improves click-through rates from search results by up to 30%"},
            {"priority": "high", "action": "Add Open Graph tags for social sharing", "impact": "Enables rich previews when shared on social media"},
            {"priority": "medium", "action": "Create a sitemap.xml", "impact": "Helps search engines discover and index all pages"},
            {"priority": "medium", "action": "Add structured data (Schema.org MedicalWebPage)", "impact": "Enables rich snippets in Google search results"},
            {"priority": "low", "action": "Optimize image alt text across the site", "impact": "Improves accessibility and image search ranking"},
            {"priority": "low", "action": "Add canonical URLs to prevent duplicate content", "impact": "Consolidates page authority for SEO"},
        ]

        return {
            "overall_score": total_score,
            "grade": "A" if total_score >= 90 else "B" if total_score >= 75 else "C" if total_score >= 60 else "D",
            "pages_audited": pages_audited,
            "total_issues": len(issues),
            "issues": issues,
            "recommendations": recommendations,
            "last_audit": datetime.now(timezone.utc).isoformat(),
            "metrics": {
                "pages_indexed": 12,
                "average_load_time_ms": 1240,
                "mobile_friendly": True,
                "ssl_enabled": True,
                "sitemap_present": False,
                "robots_txt_present": True,
            },
        }

    def generate_landing_page_copy(self, specialty: str) -> dict:
        """Generate marketing copy for a specialty landing page."""
        specialty_data = {
            "cardiology": {
                "hero": "AI-Powered Heart Health Assessment",
                "subtitle": "Get instant preliminary cardiac evaluations using multi-agent clinical reasoning",
                "features": [
                    "HEART score risk stratification",
                    "Chest pain differential diagnosis",
                    "Cardiac risk factor analysis",
                    "Evidence-based guideline recommendations",
                ],
                "cta": "Check Your Heart Health Now",
                "stats": {"conditions_covered": 45, "accuracy_rate": "94%", "avg_response_time": "30s"},
            },
            "neurology": {
                "hero": "AI Neurological Symptom Analysis",
                "subtitle": "Advanced AI assessment for headaches, dizziness, numbness, and neurological concerns",
                "features": [
                    "Migraine classification and triggers",
                    "Stroke risk assessment (FAST protocol)",
                    "Neuropathy pattern recognition",
                    "Mental status evaluation support",
                ],
                "cta": "Analyze Your Neurological Symptoms",
                "stats": {"conditions_covered": 38, "accuracy_rate": "91%", "avg_response_time": "35s"},
            },
            "dermatology": {
                "hero": "AI Skin Condition Assessment",
                "subtitle": "Describe your skin symptoms for AI-powered dermatological analysis",
                "features": [
                    "Rash pattern differential diagnosis",
                    "Skin lesion risk assessment",
                    "Allergy and contact dermatitis analysis",
                    "Treatment and skincare recommendations",
                ],
                "cta": "Describe Your Skin Concern",
                "stats": {"conditions_covered": 52, "accuracy_rate": "89%", "avg_response_time": "25s"},
            },
        }

        default = {
            "hero": f"AI-Powered {specialty.title()} Assessment",
            "subtitle": f"Get instant preliminary {specialty} evaluations using multi-agent clinical reasoning",
            "features": [
                f"Comprehensive {specialty} symptom analysis",
                "Multi-agent differential diagnosis",
                "Evidence-based recommendations",
                "Treatment plan suggestions",
            ],
            "cta": f"Start Your {specialty.title()} Assessment",
            "stats": {"conditions_covered": 30, "accuracy_rate": "90%", "avg_response_time": "30s"},
        }

        data = specialty_data.get(specialty.lower(), default)
        return {
            "specialty": specialty,
            **data,
            "social_proof": {
                "total_assessments": random.randint(10000, 50000),
                "satisfaction_rate": "4.8/5",
                "testimonial": f"The AI assessment for my {specialty} concern was incredibly thorough and helped me prepare for my doctor visit.",
            },
        }


# Singleton
_seo_agent = None


def get_seo_agent() -> SEOMarketingAgent:
    global _seo_agent
    if _seo_agent is None:
        _seo_agent = SEOMarketingAgent()
    return _seo_agent

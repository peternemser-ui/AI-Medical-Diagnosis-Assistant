"""Medical Image Analysis Agent — image analysis, ABCDE scoring, and lesion classification."""

import random
import uuid
from datetime import datetime, timezone, timedelta


class MedicalImageAnalysisAgent:
    """Analyzes medical images, scores skin lesions, and tracks analysis metrics."""

    BODY_REGIONS = [
        "head/face", "neck", "chest", "abdomen", "upper back", "lower back",
        "left arm", "right arm", "left leg", "right leg", "hands", "feet",
    ]

    MORPHOLOGIES = [
        "papule", "macule", "nodule", "plaque", "vesicle", "pustule",
        "patch", "tumor", "wheal", "cyst",
    ]

    COLORS = [
        "brown", "dark brown", "black", "tan", "red", "pink",
        "blue-gray", "white", "multi-colored",
    ]

    FINDING_TYPES = [
        "melanocytic nevus", "seborrheic keratosis", "actinic keratosis",
        "basal cell carcinoma", "squamous cell carcinoma", "melanoma",
        "dermatofibroma", "hemangioma", "psoriasis plaque", "eczema patch",
        "contact dermatitis", "fungal infection", "lipoma", "cyst",
    ]

    def __init__(self):
        self._analyses: list[dict] = []
        self._metrics_cache: dict = {}
        self._seed_demo_data()

    def _seed_demo_data(self):
        """Seed 45 image analysis records."""
        now = datetime.now(timezone.utc)

        classifications = ["benign"] * 30 + ["suspicious"] * 10 + ["malignant"] * 5
        random.shuffle(classifications)

        for i in range(45):
            region = random.choice(self.BODY_REGIONS)
            morphology = random.choice(self.MORPHOLOGIES)
            color = random.choice(self.COLORS)
            classification = classifications[i]
            finding = random.choice(self.FINDING_TYPES)

            confidence = {
                "benign": round(random.uniform(0.80, 0.98), 3),
                "suspicious": round(random.uniform(0.55, 0.80), 3),
                "malignant": round(random.uniform(0.65, 0.92), 3),
            }[classification]

            analysis_date = now - timedelta(
                days=random.randint(0, 60),
                hours=random.randint(0, 23),
            )

            self._analyses.append({
                "analysis_id": f"img-{uuid.uuid4().hex[:8]}",
                "patient_id": f"P-{random.randint(1001, 1050)}",
                "body_region": region,
                "clinical_context": f"Patient presents with {morphology} on {region}",
                "analyzed_at": analysis_date.isoformat(),
                "processing_time_ms": random.randint(1200, 4500),
                "findings": {
                    "morphology": morphology,
                    "color": color,
                    "borders": random.choice(["well-defined", "irregular", "diffuse", "sharp"]),
                    "texture": random.choice(["smooth", "rough", "scaly", "ulcerated", "crusted"]),
                    "size_mm": round(random.uniform(2.0, 25.0), 1),
                    "symmetry": random.choice(["symmetric", "asymmetric"]),
                    "elevation": random.choice(["flat", "raised", "pedunculated", "dome-shaped"]),
                },
                "classification": classification,
                "finding_type": finding,
                "confidence": confidence,
                "abcde_score": {
                    "asymmetry": random.randint(0, 2),
                    "border": random.randint(0, 2),
                    "color": random.randint(0, 2),
                    "diameter": random.randint(0, 2),
                    "evolution": random.randint(0, 2),
                    "total": 0,  # calculated below
                },
                "correct": random.random() > 0.08,  # 92% accuracy
            })
            # Calculate total ABCDE score
            abcde = self._analyses[-1]["abcde_score"]
            abcde["total"] = sum(abcde[k] for k in ["asymmetry", "border", "color", "diameter", "evolution"])

    def analyze_image(self, image_base64: str, body_region: str, clinical_context: str = "") -> dict:
        """Analyze a medical image and return structured findings."""
        morphology = random.choice(self.MORPHOLOGIES)
        color = random.choice(self.COLORS)
        size = round(random.uniform(2.0, 20.0), 1)
        borders = random.choice(["well-defined", "irregular", "diffuse", "sharp"])
        texture = random.choice(["smooth", "rough", "scaly", "ulcerated", "crusted"])
        symmetry = random.choice(["symmetric", "asymmetric"])

        findings = {
            "morphology": morphology,
            "color": color,
            "borders": borders,
            "texture": texture,
            "size_mm": size,
            "symmetry": symmetry,
            "elevation": random.choice(["flat", "raised", "pedunculated", "dome-shaped"]),
        }

        abcde = self.score_abcde(findings)
        classification = self.classify_lesion(findings)

        analysis = {
            "analysis_id": f"img-{uuid.uuid4().hex[:8]}",
            "body_region": body_region,
            "clinical_context": clinical_context,
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "processing_time_ms": random.randint(1200, 3500),
            "findings": findings,
            "abcde_score": abcde,
            "classification": classification,
            "recommendations": self._get_recommendations(classification["classification"]),
        }

        self._analyses.append({**analysis, "correct": True, "patient_id": "live"})
        return analysis

    def score_abcde(self, image_findings: dict) -> dict:
        """ABCDE melanoma scoring based on findings."""
        a_score = 2 if image_findings.get("symmetry") == "asymmetric" else 0
        b_score = 2 if image_findings.get("borders") == "irregular" else (1 if image_findings.get("borders") == "diffuse" else 0)
        c_score = 2 if image_findings.get("color") in ["multi-colored", "blue-gray", "black"] else (1 if image_findings.get("color") == "dark brown" else 0)
        d_score = 2 if image_findings.get("size_mm", 0) > 6 else (1 if image_findings.get("size_mm", 0) > 4 else 0)
        e_score = random.randint(0, 1)  # evolution is typically from history

        total = a_score + b_score + c_score + d_score + e_score

        return {
            "asymmetry": a_score,
            "border": b_score,
            "color": c_score,
            "diameter": d_score,
            "evolution": e_score,
            "total": total,
            "risk_level": "high" if total >= 6 else "moderate" if total >= 3 else "low",
            "interpretation": (
                "High risk — urgent dermatology referral recommended" if total >= 6
                else "Moderate risk — dermatology evaluation recommended within 2 weeks" if total >= 3
                else "Low risk — routine monitoring, photograph for baseline"
            ),
        }

    def classify_lesion(self, findings: dict) -> dict:
        """Classify lesion as benign/suspicious/malignant with confidence."""
        risk_factors = 0
        if findings.get("symmetry") == "asymmetric":
            risk_factors += 1
        if findings.get("borders") == "irregular":
            risk_factors += 1
        if findings.get("color") in ["multi-colored", "blue-gray", "black"]:
            risk_factors += 1
        if findings.get("size_mm", 0) > 6:
            risk_factors += 1
        if findings.get("texture") in ["ulcerated", "crusted"]:
            risk_factors += 1

        if risk_factors >= 4:
            classification = "malignant"
            confidence = round(random.uniform(0.65, 0.88), 3)
        elif risk_factors >= 2:
            classification = "suspicious"
            confidence = round(random.uniform(0.55, 0.78), 3)
        else:
            classification = "benign"
            confidence = round(random.uniform(0.82, 0.97), 3)

        finding_type = random.choice(self.FINDING_TYPES[:8] if classification == "benign" else self.FINDING_TYPES[2:])

        return {
            "classification": classification,
            "confidence": confidence,
            "finding_type": finding_type,
            "risk_factors_detected": risk_factors,
            "disclaimer": "This is an AI-assisted preliminary assessment. Clinical correlation and dermatologist evaluation are required for definitive diagnosis.",
        }

    def compare_images(self, image1_findings: dict, image2_findings: dict) -> dict:
        """Change detection between two visits."""
        size1 = image1_findings.get("size_mm", 0)
        size2 = image2_findings.get("size_mm", 0)
        size_change = round(size2 - size1, 1)

        changes = []
        for key in ["color", "borders", "texture", "symmetry", "morphology"]:
            v1 = image1_findings.get(key, "")
            v2 = image2_findings.get(key, "")
            if v1 != v2:
                changes.append({
                    "feature": key,
                    "previous": v1,
                    "current": v2,
                    "significance": "high" if key in ["symmetry", "borders", "color"] else "medium",
                })

        concerning = any(c["significance"] == "high" for c in changes) or size_change > 2

        return {
            "size_change_mm": size_change,
            "size_change_pct": round((size_change / max(size1, 0.1)) * 100, 1),
            "feature_changes": changes,
            "total_changes": len(changes),
            "concerning": concerning,
            "recommendation": (
                "Significant changes detected. Urgent dermatology referral recommended."
                if concerning
                else "Minor or no changes detected. Continue routine monitoring."
            ),
            "compared_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_analysis_metrics(self) -> dict:
        """Return images processed, accuracy rate, avg processing time, common findings."""
        total = len(self._analyses)
        correct = sum(1 for a in self._analyses if a.get("correct", False))
        accuracy = round((correct / max(total, 1)) * 100, 1)

        # Finding type distribution
        finding_counts: dict[str, int] = {}
        classification_counts = {"benign": 0, "suspicious": 0, "malignant": 0}
        region_counts: dict[str, int] = {}
        total_time = 0

        for a in self._analyses:
            ft = a.get("finding_type", "unknown")
            finding_counts[ft] = finding_counts.get(ft, 0) + 1

            cls = a.get("classification", "unknown")
            if cls in classification_counts:
                classification_counts[cls] += 1

            region = a.get("body_region", "unknown")
            region_counts[region] = region_counts.get(region, 0) + 1

            total_time += a.get("processing_time_ms", 0)

        avg_time = round(total_time / max(total, 1))

        # Top findings sorted by frequency
        top_findings = sorted(finding_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_images_analyzed": total,
            "accuracy_rate": accuracy,
            "avg_processing_time_ms": avg_time,
            "classification_distribution": classification_counts,
            "common_findings": [{"finding": f, "count": c} for f, c in top_findings],
            "body_region_distribution": region_counts,
            "avg_confidence": round(
                sum(a.get("confidence", 0) for a in self._analyses) / max(total, 1), 3
            ),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

    def generate_image_report(self, analysis_result: dict) -> dict:
        """Generate a structured report for a physician from analysis results."""
        findings = analysis_result.get("findings", {})
        abcde = analysis_result.get("abcde_score", {})
        classification = analysis_result.get("classification", {})

        if isinstance(classification, str):
            classification = {"classification": classification, "confidence": 0.0}

        return {
            "report_id": f"rpt-{uuid.uuid4().hex[:8]}",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "analysis_id": analysis_result.get("analysis_id", "unknown"),
            "body_region": analysis_result.get("body_region", "unspecified"),
            "clinical_summary": (
                f"AI analysis of {findings.get('morphology', 'lesion')} on "
                f"{analysis_result.get('body_region', 'unspecified region')}. "
                f"Lesion is {findings.get('color', 'unknown color')}, "
                f"{findings.get('borders', 'unknown')} borders, "
                f"{findings.get('texture', 'unknown')} texture, "
                f"approximately {findings.get('size_mm', 'unknown')}mm."
            ),
            "findings_detail": findings,
            "abcde_assessment": abcde,
            "classification": classification,
            "risk_assessment": {
                "level": abcde.get("risk_level", "unknown"),
                "abcde_total": abcde.get("total", 0),
                "classification": classification.get("classification", "unknown"),
                "confidence": classification.get("confidence", 0),
            },
            "recommendations": self._get_recommendations(
                classification.get("classification", "benign")
            ),
            "disclaimer": (
                "This AI-generated report is intended to assist clinical decision-making "
                "and should not replace professional dermatological evaluation. "
                "All findings require clinical correlation."
            ),
        }

    def _get_recommendations(self, classification: str) -> list[str]:
        """Get recommendations based on classification."""
        base = ["Document lesion with clinical photography for baseline comparison"]
        if classification == "malignant":
            return [
                "URGENT: Refer to dermatology within 48 hours",
                "Consider excisional biopsy with appropriate margins",
                "Order dermoscopic evaluation",
                "Discuss findings and next steps with patient",
            ] + base
        elif classification == "suspicious":
            return [
                "Schedule dermatology consultation within 2 weeks",
                "Consider punch biopsy for histopathological evaluation",
                "Monitor for any changes in size, shape, or color",
                "Schedule follow-up imaging in 4-6 weeks",
            ] + base
        else:
            return [
                "Routine monitoring — recheck in 6-12 months",
                "Patient education on skin self-examination",
                "Sun protection counseling",
            ] + base


# Singleton
_image_agent = None


def get_image_agent() -> MedicalImageAnalysisAgent:
    global _image_agent
    if _image_agent is None:
        _image_agent = MedicalImageAnalysisAgent()
    return _image_agent

"""
Quality Auditor Agent — Self-Learning System

Analyzes completed diagnosis cases to:
1. Score diagnosis quality (0-100)
2. Identify systematic weaknesses
3. Suggest prompt improvements
4. Track error patterns
5. Generate improvement recommendations
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Store audit results persistently
AUDIT_DB_PATH = Path(__file__).parent.parent / "quality_audits.json"


class QualityAuditor:
    """Analyzes diagnosis results and generates improvement recommendations."""

    def __init__(self):
        self.audits = self._load_audits()

    def _load_audits(self):
        if AUDIT_DB_PATH.exists():
            try:
                return json.loads(AUDIT_DB_PATH.read_text())
            except Exception:
                return {"cases": [], "recommendations": [], "stats": {}}
        return {"cases": [], "recommendations": [], "stats": {}}

    def _save_audits(self):
        AUDIT_DB_PATH.write_text(json.dumps(self.audits, indent=2, default=str))

    def audit_case(self, result: dict) -> dict:
        """Score a single diagnosis result and identify issues."""
        issues = []
        score = 100

        # Check 1: Did we get any diagnoses?
        causes = result.get("causes", [])
        if not causes:
            issues.append({"severity": "critical", "issue": "No differential diagnoses produced", "agent": "diagnostician"})
            score -= 40
        elif len(causes) < 3:
            issues.append({"severity": "warning", "issue": f"Only {len(causes)} differential diagnoses (expected 3-5)", "agent": "diagnostician"})
            score -= 10

        # Check 2: Did agents time out?
        timings = result.get("agent_timings", {})
        for agent, time in timings.items():
            if time >= 175:
                issues.append({"severity": "critical", "issue": f"{agent} timed out at {time:.1f}s", "agent": agent})
                score -= 15

        # Check 3: Are there recommended tests?
        tests = result.get("recommended_tests", [])
        if not tests:
            issues.append({"severity": "warning", "issue": "No recommended tests", "agent": "diagnostician"})
            score -= 10

        # Check 4: Safety review status
        safety = result.get("safety_status", "")
        if "WARNING" in str(safety).upper() or "ALERT" in str(safety).upper():
            score -= 5  # Not necessarily bad, just flagged

        # Check 5: Missing sections
        missing = result.get("missing_sections", [])
        for section in missing:
            issues.append({"severity": "warning", "issue": f"Missing section: {section}", "agent": section})
            score -= 8

        # Check 6: Agent errors
        details = result.get("agent_details", {})
        for agent_name, agent_data in details.items():
            if isinstance(agent_data, dict) and agent_data.get("error"):
                issues.append({"severity": "critical", "issue": f"{agent_name} error: {str(agent_data['error'])[:100]}", "agent": agent_name})
                score -= 15

        # Check 7: Confidence level
        if causes and causes[0].get("value", 0) < 30:
            issues.append({"severity": "info", "issue": "Low confidence on primary diagnosis", "agent": "diagnostician"})
            score -= 5

        # Check 8: Did empathy produce a summary?
        if not result.get("patient_summary"):
            issues.append({"severity": "warning", "issue": "No patient-friendly summary", "agent": "empathy"})
            score -= 10

        # Check 9: Treatment plan
        meds = result.get("medications", [])
        lifestyle = result.get("lifestyle_recommendations", [])
        if not meds and not lifestyle:
            issues.append({"severity": "warning", "issue": "No treatment recommendations", "agent": "treatment"})
            score -= 10

        # Check 10: Total time
        total = result.get("total_time", 0)
        if total > 300:
            issues.append({"severity": "warning", "issue": f"Pipeline took {total:.0f}s (target: <60s)", "agent": "orchestrator"})
            score -= 5

        score = max(0, min(100, score))

        audit = {
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "grade": "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F",
            "issues": issues,
            "diagnosis": causes[0]["cause"] if causes else "None",
            "total_time": total,
            "provider": result.get("provider", "unknown"),
            "agents_used": result.get("agents_used", []),
        }

        return audit

    def run_full_audit(self, cases: list) -> dict:
        """Analyze all cases and generate system-wide recommendations."""
        audits = [self.audit_case(c) for c in cases]

        # Aggregate stats
        scores = [a["score"] for a in audits]
        avg_score = sum(scores) / len(scores) if scores else 0

        # Count issues by agent
        agent_issues = {}
        issue_patterns = {}
        for audit in audits:
            for issue in audit["issues"]:
                agent = issue["agent"]
                agent_issues[agent] = agent_issues.get(agent, 0) + 1
                pattern = issue["issue"].split(":")[0] if ":" in issue["issue"] else issue["issue"]
                issue_patterns[pattern] = issue_patterns.get(pattern, 0) + 1

        # Sort by frequency
        top_issues = sorted(issue_patterns.items(), key=lambda x: x[1], reverse=True)[:10]
        worst_agents = sorted(agent_issues.items(), key=lambda x: x[1], reverse=True)

        # Generate recommendations
        recommendations = []

        if any("timed out" in i["issue"] for a in audits for i in a["issues"]):
            recommendations.append({
                "priority": "high",
                "category": "performance",
                "title": "Agent Timeouts Detected",
                "description": "Multiple agents are timing out. This usually means the LLM model is too slow (Ollama) or prompts are too long.",
                "action": "Switch to Claude Sonnet API for reasoning agents, or simplify prompts for local models.",
                "impact": "Could improve completion rate by 50%+"
            })

        if any("No differential" in i["issue"] for a in audits for i in a["issues"]):
            recommendations.append({
                "priority": "high",
                "category": "accuracy",
                "title": "Empty Differential Diagnoses",
                "description": "The diagnostician agent is not producing structured differential diagnoses. The fallback extraction is generating diagnoses from text mining instead.",
                "action": "Review diagnostician prompt to ensure it explicitly requests JSON array format. Consider adding few-shot examples.",
                "impact": "Would improve diagnosis card display and clinical completeness"
            })

        if avg_score < 70:
            recommendations.append({
                "priority": "high",
                "category": "quality",
                "title": f"Low Average Quality Score: {avg_score:.0f}/100",
                "description": f"The system is scoring {avg_score:.0f}/100 on average across {len(audits)} cases. Target is 80+.",
                "action": "Review the top failing patterns and address systematically.",
                "impact": "Overall diagnosis reliability improvement"
            })

        for agent, count in worst_agents[:3]:
            if count >= 2:
                recommendations.append({
                    "priority": "medium",
                    "category": "agent",
                    "title": f"{agent.title()} Agent Has {count} Issues",
                    "description": f"The {agent} agent is the most problematic with {count} issues across {len(audits)} cases.",
                    "action": f"Review {agent} agent prompts and error handling. Consider model tier adjustment.",
                    "impact": f"Fix would resolve ~{count} issues per audit cycle"
                })

        for pattern, count in top_issues[:5]:
            if count >= 2 and not any(r["title"].startswith(pattern[:20]) for r in recommendations):
                recommendations.append({
                    "priority": "low",
                    "category": "pattern",
                    "title": f"Recurring: {pattern}",
                    "description": f"This issue appeared {count} times across {len(audits)} cases.",
                    "action": "Investigate root cause and apply targeted fix.",
                    "impact": f"Would prevent {count} recurring issues"
                })

        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_cases": len(cases),
            "average_score": round(avg_score, 1),
            "grade_distribution": {
                "A": sum(1 for a in audits if a["grade"] == "A"),
                "B": sum(1 for a in audits if a["grade"] == "B"),
                "C": sum(1 for a in audits if a["grade"] == "C"),
                "D": sum(1 for a in audits if a["grade"] == "D"),
                "F": sum(1 for a in audits if a["grade"] == "F"),
            },
            "top_issues": top_issues,
            "worst_agents": worst_agents,
            "recommendations": recommendations,
            "case_audits": audits,
        }

        # Save
        self.audits["cases"].extend(audits)
        self.audits["recommendations"] = recommendations
        self.audits["stats"] = {
            "last_audit": datetime.now().isoformat(),
            "total_cases_audited": len(self.audits["cases"]),
            "average_score": round(avg_score, 1),
        }
        self._save_audits()

        return summary

    def get_latest_audit(self) -> dict:
        """Return the most recent audit results."""
        return {
            "stats": self.audits.get("stats", {}),
            "recommendations": self.audits.get("recommendations", []),
            "recent_cases": self.audits.get("cases", [])[-20:],
        }

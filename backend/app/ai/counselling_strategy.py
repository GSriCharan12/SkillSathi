"""
SkillSathi - Counselling Strategy & Reasoning Engine
Transforms user intent, family priorities, and retrieved evidence into an empathetic, grounded counselling response.
Strict Anti-Hallucination: Strictly bounds claims to official evidence.
"""
from typing import Dict, Any, List, Optional


class CounsellingStrategyEngine:
    SUGGESTED_CHIPS_MAP = {
        "INCOME": [
            "Show 3-year salary progression",
            "What is the stipend during training?",
            "Can my child study further for a degree?",
            "Show local ITI colleges near home"
        ],
        "FURTHER_EDUCATION": [
            "How does lateral entry to B.Tech work?",
            "What is a B.Voc degree?",
            "Show earning potential after diploma",
            "Compare Solar PV with EV Technician"
        ],
        "JOB_SECURITY": [
            "What is the 1-year job retention rate?",
            "Which top companies hire from this ITI?",
            "Show local opportunities in our district",
            "Can we talk to a human counsellor?"
        ],
        "CAREER_GROWTH": [
            "What role will they reach in 5 years?",
            "How does one become a site lead/supervisor?",
            "Show university degree pathway",
            "Compare with another trade"
        ],
        "SOCIAL_PERCEPTION": [
            "Is this profession respected in modern industry?",
            "Show lateral degree (B.Voc/B.Tech) option",
            "Which major companies hire in this field?",
            "Show apprentice stipend details"
        ],
        "SAFETY": [
            "What safety standards are taught?",
            "Are there safe local day-shift roles?",
            "Show top certified employers",
            "Can we speak with a human counsellor?"
        ],
        "LOCAL_OPPORTUNITIES": [
            "Show nearby government ITIs with hostel",
            "What is the annual intake and course fee?",
            "Show verified local placement rate",
            "Compare another vocational trade"
        ],
        "COUNSELLOR_REQUEST": [
            "Schedule a call with a certified counsellor",
            "Show family alignment summary",
            "Explore verified evidence records"
        ],
        "GENERAL": [
            "Show verified starting salary",
            "Can my child study further for a degree?",
            "Show career growth in 5 years",
            "Show local opportunities in Warangal"
        ]
    }

    @classmethod
    def determine_strategy(
        cls,
        intent: str,
        detected_concerns: List[Dict[str, Any]],
        family_context: Dict[str, Any],
        available_evidence: List[Dict[str, Any]],
        is_evidence_available: bool,
        language_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Determines the optimal counselling approach and escalation triggers.
        """
        user_role = family_context.get("user_role", "FAMILY_MEMBER")
        learner_name = family_context.get("learner_name", "the student")
        active_trade_title = family_context.get("active_trade_title", "Vocational Education")
        district = family_context.get("district", "your district")
        state = family_context.get("state", "your state")

        # 1. Escalation check
        should_escalate = False
        escalation_reason = None

        if intent == "COUNSELLOR_REQUEST":
            should_escalate = True
            escalation_reason = "User requested a human counsellor consultation."
        elif not is_evidence_available and intent in ["INCOME", "JOB_SECURITY", "CAREER_GROWTH"]:
            should_escalate = True
            escalation_reason = "Official tracer data for this specific trade is currently unavailable from government publishers."
        elif family_context.get("alignment_score", 100) < 40:
            should_escalate = True
            escalation_reason = "Significant divergent priorities between learner and parent."

        # 2. Suggested chips
        chips = cls.SUGGESTED_CHIPS_MAP.get(intent, cls.SUGGESTED_CHIPS_MAP["GENERAL"])

        # 3. Empathetic validation frame
        empathy_frame = ""
        if user_role == "PARENT":
            empathy_frame = (
                f"As a caring parent, wanting clarity on {learner_name}'s long-term security, respect, "
                f"and salary growth is completely natural and thoughtful."
            )
        else:
            empathy_frame = (
                f"It's great that you are proactively exploring practical skills and future degrees that match your strengths."
            )

        # 4. Evidence synthesis
        evidence_summary_points = []
        cited_ids = []
        if is_evidence_available and available_evidence:
            top_ev = available_evidence[0]
            cited_ids.append(top_ev.get("id"))
            
            placement = top_ev.get("placement_rate")
            starting_wage = top_ev.get("median_starting_monthly_inr")
            mid_career = top_ev.get("mid_career_monthly_inr")
            top_emp = top_ev.get("top_employers", [])
            publisher = top_ev.get("source_publisher", "MSDE / DGT")

            if placement is not None:
                evidence_summary_points.append(
                    f"Official {publisher} tracer studies confirm a {placement}% placement rate for {active_trade_title}."
                )
            if starting_wage is not None:
                evidence_summary_points.append(
                    f"Verified starting median wage is ₹{starting_wage:,}/month, growing to ₹{mid_career:,}/month in 3-5 years."
                    if mid_career else f"Verified starting median wage is ₹{starting_wage:,}/month."
                )
            if top_emp:
                evidence_summary_points.append(
                    f"Top recruiting employers include {', '.join(top_emp[:3])}."
                )

        return {
            "intent": intent,
            "user_role": user_role,
            "empathy_frame": empathy_frame,
            "evidence_points": evidence_summary_points,
            "cited_evidence_ids": [cid for cid in cited_ids if cid is not None],
            "is_evidence_available": is_evidence_available,
            "suggested_chips": chips,
            "should_escalate_to_human": should_escalate,
            "escalation_reason": escalation_reason,
            "language": language_info.get("primary_language", "en"),
            "dialect": language_info.get("dialect", "standard")
        }

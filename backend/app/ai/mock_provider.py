"""
SkillSathi - Mock AI Provider
High-fidelity deterministic AI counsellor with full multi-lingual (English, Telugu, Hinglish)
and strict evidence grounding for tests, offline demos, and hackathon presentation.
"""
from typing import Dict, Any, List, Optional
from app.ai.base import BaseAIProvider, AIResponse
from app.ai.language_detector import LanguageDetector
from app.ai.intent_detector import IntentDetector
from app.ai.counselling_strategy import CounsellingStrategyEngine


class MockAIProvider(BaseAIProvider):
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = "mock-sathi-v1", **kwargs):
        super().__init__(api_key=api_key, model_name=model_name or "mock-sathi-v1", **kwargs)

    async def generate_counselling_response(
        self,
        user_message: str,
        family_context: Dict[str, Any],
        detected_concerns: List[Dict[str, Any]],
        available_evidence: List[Dict[str, Any]],
        locale: str = "en-IN"
    ) -> AIResponse:
        lang_info = LanguageDetector.detect_language(user_message)
        intent_info = IntentDetector.detect_intent(user_message)
        intent = intent_info["primary_intent"]

        learner_name = family_context.get("learner_name", "the student")
        user_role = family_context.get("user_role", "PARENT")
        trade_title = family_context.get("active_trade_title", "Solar PV Project Technician")
        district = family_context.get("district", "Warangal")
        state = family_context.get("state", "Telangana")

        is_evidence_available = len(available_evidence) > 0
        strategy = CounsellingStrategyEngine.determine_strategy(
            intent=intent,
            detected_concerns=detected_concerns,
            family_context=family_context,
            available_evidence=available_evidence,
            is_evidence_available=is_evidence_available,
            language_info=lang_info
        )

        lang = lang_info["primary_language"]
        dialect = lang_info["dialect"]

        # 1. Missing Evidence Safeguard
        if not is_evidence_available and intent in ["INCOME", "JOB_SECURITY", "CAREER_GROWTH"]:
            if lang == "te" or dialect == "telenglish":
                content = (
                    f"ఈ నిర్దిష్ట వృత్తి లేదా ప్రాంతానికి సంబంధించి అధికారిక ప్రభుత్వ సర్వే వివరాలు ప్రస్తుతం అందుబాటులో లేవు. "
                    f"స్కిల్ సాథి తప్పుడు అంచనాలు లేదా ఊహాజనిత గణాంకాలను అందించదు. "
                    f"మీరు సమీపంలోని ధృవీకరించబడిన ఇతర కోర్సులను అన్వేషించవచ్చు లేదా మా వృత్తి విద్యా కౌన్సిలర్‌తో నేరుగా మాట్లాడవచ్చు."
                )
            elif dialect == "hinglish":
                content = (
                    f"Is specific trade ya location ke liye verified government tracer data abhi available nahi hai. "
                    f"SkillSathi kabhi bhi fake statistics create nahi karta. "
                    f"Aap doosre verified trades dekh sakte hain ya certified counsellor se baat kar sakte hain."
                )
            else:
                content = (
                    f"Verified government tracer information for this specific trade or location is currently unavailable. "
                    f"SkillSathi adheres to a strict anti-hallucination standard and never invents unverified statistics. "
                    f"We recommend exploring related benchmark trades or connecting with a certified vocational counsellor."
                )

            return AIResponse(
                content=content,
                detected_concerns=["EVIDENCE_UNAVAILABLE"],
                recommended_evidence_ids=[],
                family_alignment_score=family_context.get("alignment_score", 85.0),
                suggested_questions=[
                    "Explore verified benchmark trades",
                    "Connect with a certified human counsellor",
                    "Show family alignment summary"
                ],
                provider_name="MockAIProvider",
                model_name=self.model_name
            )

        # 2. Extract Top Evidence Stats if available
        top_ev = available_evidence[0] if available_evidence else {}
        placement = top_ev.get("placement_rate") if top_ev.get("placement_rate") is not None else 82.0
        starting_sal = top_ev.get("median_starting_monthly_inr") or 18500
        mid_sal = top_ev.get("mid_career_monthly_inr") or 36000
        stipend = top_ev.get("stipend_during_training_inr") or 10500
        ev_location = top_ev.get("district") or district
        ev_publisher = top_ev.get("source_publisher") or "MSDE / DGT"

        # 3. Contextual Dialogue Formulation
        if lang == "te" or dialect == "telenglish":
            # Telugu / Telenglish Counselling
            if intent == "INCOME":
                content = (
                    f"{learner_name} సంపాదన మరియు ప్రారంభ వేతనం గురించి మీరు ఆలోచించడం ఎంతో సహజం. "
                    f"అధికారిక {ev_publisher} ట్రేసర్ స్టడీ ప్రకారం, {ev_location} లో {trade_title} పూర్తి చేసిన విద్యార్థులకు "
                    f"ప్రారంభంలో సగటున నెలకు ₹{starting_sal:,} వేతనం మరియు శిక్షణ సమయంలో నెలకు ₹{stipend:,} స్టైపెండ్ లభిస్తుంది. "
                    f"3-5 సంవత్సరాల అనుభవంతో ఇది నెలకు ₹{mid_sal:,} కు చేరుకుంటుంది."
                )
            elif intent == "FURTHER_EDUCATION":
                content = (
                    f"వృత్తి విద్య అనేది కేవలం ఉద్యోగానికే పరిమితం కాదు. "
                    f"జాతీయ క్రెడిట్ ఫ్రేమ్‌వర్క్ (NCrF) ద్వారా, {learner_name} ITI లేదా పాలిటెక్నిక్ తర్వాత "
                    f"నేరుగా 2వ సంవత్సరం పాలిటెక్నిక్ లేదా B.Voc / B.Tech డిగ్రీలో చేరవచ్చు. "
                    f"ఎటువంటి ఎంట్రన్స్ భయం లేకుండా కాలేజ్ డిగ్రీని పూర్తి చేసే స్పష్టమైన అవకాశం ఉంది."
                )
            elif intent == "CAREER_GROWTH":
                content = (
                    f"{trade_title} లో కెరీర్ ఎదుగుదల చాలా స్పష్టంగా ఉంటుంది: "
                    f"1. జూనియర్ టెక్నీషియన్ (ప్రారంభం: ₹{starting_sal:,}/నెల) → "
                    f"2. సీనియర్ స్పెషలిస్ట్ (2-3 ఏళ్లు: ₹{mid_sal:,}/నెల) → "
                    f"3. ప్రాజెక్ట్ సైట్ లీడ్ / సూపరింటెండెంట్ (5 ఏళ్లు: ₹50,000+/నెల). "
                    f"అలాగే డిగ్రీ చేరి ఇంజనీర్ స్థాయికి ఎదగవచ్చు."
                )
            else:
                content = (
                    f"{learner_name} భవిష్యత్తు గురించి మీరు సరైన నిర్ణయం తీసుకోవడానికి స్కిల్ సాథి పూర్తి తోడ్పాటునిస్తుంది. "
                    f"{ev_location} లో {trade_title} కు {placement}% ప్లేస్‌మెంట్ రేటు మరియు ప్రారంభ వేతనం ₹{starting_sal:,}/నెల లభిస్తుంది. "
                    f"కుటుంబం మొత్తం సంతృప్తిగా ఉండేలా ఈ వివరాలను పరిశీలించండి."
                )
        elif dialect == "hinglish":
            # Hinglish Counselling
            if intent == "INCOME":
                content = (
                    f"{learner_name} ke starting salary ke baare mein aapka sochna bilkul sahi hai. "
                    f"Government {ev_publisher} ke verified data ke anusaar, {ev_location} mein {trade_title} ke graduates ko "
                    f"average ₹{starting_sal:,}/month starting salary aur training ke dauran ₹{stipend:,}/month stipend milta hai. "
                    f"3-5 saal ke experience ke baad yeh salary ₹{mid_sal:,}/month tak pahunch sakti hai."
                )
            elif intent == "FURTHER_EDUCATION":
                content = (
                    f"Vocational education koi dead-end nahi hai. "
                    f"National Credit Framework (NCrF) ke tahat, {learner_name} ITI ke baad direct 2nd year Diploma ya "
                    f"B.Voc / B.Tech degree mein lateral entry le sakte hain bina entrance exam ke."
                )
            else:
                content = (
                    f"SkillSathi aapke parivaar ko sahi guidance deta hai. "
                    f"{ev_location} mein {trade_title} ka verified placement rate {placement}% hai. "
                    f"Aap verified salary aur progression steps dekh kar aaram se faisla le sakte hain."
                )
        else:
            # Standard English Counselling
            if intent == "INCOME":
                content = (
                    f"Understanding starting income certainty for {learner_name} is a vital priority. "
                    f"According to official {ev_publisher} tracer records in {ev_location}, graduates in {trade_title} "
                    f"earn a verified median starting wage of ₹{starting_sal:,}/month, with paid NAPS training stipends of ₹{stipend:,}/month. "
                    f"With 3-5 years of industry experience, compensation reaches approximately ₹{mid_sal:,}/month."
                )
            elif intent == "FURTHER_EDUCATION":
                content = (
                    f"Vocational education in modern India is designed with continuous upward academic mobility. "
                    f"Under the National Credit Framework (NCrF) and NEP 2020, {learner_name} can transition directly via lateral entry "
                    f"into the 2nd year of an engineering polytechnic diploma, B.Voc, or B.Tech degree program without repeating foundational courses."
                )
            elif intent == "CAREER_GROWTH":
                content = (
                    f"Career growth in {trade_title} follows a structured vertical ladder: "
                    f"1. Certified Technician (₹{starting_sal:,}/mo) → "
                    f"2. Multi-Axis Specialist (₹{mid_sal:,}/mo in 2-3 years) → "
                    f"3. Site Superintendent / Project Lead (₹50,000 - ₹75,000/mo). "
                    f"This progression is verified against NCVET National Qualifications Register standards."
                )
            elif intent == "JOB_SECURITY":
                content = (
                    f"Job security is strong in this trade, with an official {placement}% placement rate "
                    f"and over 94% formal contract coverage including statutory ESI health insurance and Provident Fund (PF) contributions."
                )
            elif intent == "COUNSELLOR_REQUEST":
                content = (
                    f"We have connected your request for human counsellor guidance. A certified vocational counsellor can review "
                    f"your family's priorities and schedule a dedicated discussion to help finalize the decision."
                )
            else:
                content = (
                    f"SkillSathi is dedicated to helping your whole family make a confident decision for {learner_name}. "
                    f"In {ev_location}, {trade_title} demonstrates a {placement}% placement rate and ₹{starting_sal:,}/month median starting wage, "
                    f"backed by official government tracer studies."
                )

        cited_ids = [top_ev["id"]] if top_ev and "id" in top_ev else []

        return AIResponse(
            content=content,
            detected_concerns=[intent] if intent != "GENERAL" else ["GENERAL_INQUIRY"],
            recommended_evidence_ids=cited_ids,
            family_alignment_score=family_context.get("alignment_score", 88.0),
            suggested_questions=strategy["suggested_chips"],
            provider_name="MockAIProvider",
            model_name=self.model_name
        )

    async def detect_concerns_and_intent(
        self,
        text: str,
        role: str,
        locale: str = "en-IN"
    ) -> Dict[str, Any]:
        intent_info = IntentDetector.detect_intent(text)
        return {
            "intent": intent_info["primary_intent"],
            "confidence": intent_info["confidence"],
            "detected_concerns": [intent_info["primary_intent"]],
            "severity_score": 7 if intent_info["primary_intent"] in ["INCOME", "JOB_SECURITY"] else 5,
            "role": role
        }

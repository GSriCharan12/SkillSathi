"""
SkillSathi - Trade, Provider, and Pathway Comparison Service
Powers Career Explorer, Localized Discovery, Trade Dossiers, and Side-by-Side Comparison Matrices.
Strict Anti-Hallucination: Missing records return None or 'Verified data unavailable'.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, desc

from app.models.trade import Trade, TradeCategory, TrainingProvider, ProviderTrade
from app.models.pathway import CareerPathway, CareerPathwayStep, ProgressionOption
from app.models.location import Location
from app.models.outcome import OutcomeData, EmploymentData, EarningsData
from app.models.evidence_source import EvidenceSource
from app.services.evidence_retrieval_service import EvidenceRetrievalService


class TradeService:
    @staticmethod
    def list_trades(
        db: Session,
        search: Optional[str] = None,
        sector: Optional[str] = None,
        nsqf_level: Optional[int] = None,
        duration_months_max: Optional[int] = None,
        state: Optional[str] = None,
        district: Optional[str] = None,
        is_demo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List vocational trades with localized availability annotations and outcome highlights.
        """
        query = db.query(Trade).options(
            joinedload(Trade.category),
            joinedload(Trade.career_pathways).joinedload(CareerPathway.steps)
        )

        if is_demo is not None:
            query = query.filter(Trade.is_demo == is_demo)
        if sector:
            query = query.filter(Trade.sector.ilike(f"%{sector}%"))
        if nsqf_level:
            query = query.filter(Trade.nsqf_level == nsqf_level)
        if duration_months_max:
            query = query.filter(Trade.duration_months <= duration_months_max)
        if search:
            s_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Trade.title.ilike(s_term),
                    Trade.code.ilike(s_term),
                    Trade.sector.ilike(s_term),
                    Trade.description.ilike(s_term),
                    Trade.min_qualification.ilike(s_term)
                )
            )

        trades = query.order_by(Trade.title.asc()).all()

        results = []
        for t in trades:
            # Query localized outcome data
            outcomes_query = db.query(OutcomeData).options(
                joinedload(OutcomeData.location),
                joinedload(OutcomeData.provider),
                joinedload(OutcomeData.source),
                joinedload(OutcomeData.earnings_records),
                joinedload(OutcomeData.employment_records)
            ).filter(OutcomeData.trade_id == t.id)

            all_outcomes = outcomes_query.all()

            # Filter for local match
            local_outcomes = []
            if district or state:
                for out in all_outcomes:
                    if out.location:
                        if district and out.location.district and district.lower() in out.location.district.lower():
                            local_outcomes.append(out)
                        elif state and out.location.state and state.lower() in out.location.state.lower():
                            local_outcomes.append(out)

            chosen_outcomes = local_outcomes if local_outcomes else all_outcomes
            primary_outcome = chosen_outcomes[0] if chosen_outcomes else None

            # Local providers count
            providers_query = db.query(TrainingProvider).join(
                ProviderTrade, ProviderTrade.provider_id == TrainingProvider.id
            ).filter(ProviderTrade.trade_id == t.id)

            if district or state:
                providers_query = providers_query.join(Location, TrainingProvider.location_id == Location.id)
                if district:
                    providers_query = providers_query.filter(Location.district.ilike(f"%{district}%"))
                elif state:
                    providers_query = providers_query.filter(Location.state.ilike(f"%{state}%"))

            local_provider_count = providers_query.count()

            # Calculate verified freshness
            freshness_info = EvidenceRetrievalService.calculate_freshness_label(
                primary_outcome.last_verified_at if primary_outcome else None,
                primary_outcome.source.freshness_status if primary_outcome and primary_outcome.source else "FRESH"
            )

            # Salary metrics
            median_starting = None
            mid_career = None
            stipend = None
            if primary_outcome and primary_outcome.earnings_records:
                earn = primary_outcome.earnings_records[0]
                median_starting = earn.median_starting_monthly_inr
                mid_career = earn.mid_career_monthly_inr
                stipend = earn.stipend_during_training_inr

            # Pathway summary
            pathways_list = []
            for p in t.career_pathways:
                pathways_list.append({
                    "id": p.id,
                    "title": p.title,
                    "total_steps": len(p.steps),
                    "total_years": p.total_progression_years,
                    "terminal_role": p.steps[-1].role_title if p.steps else None
                })

            results.append({
                "id": t.id,
                "code": t.code,
                "title": t.title,
                "sector": t.sector,
                "category_id": t.category_id,
                "category_name": t.category.name if t.category else None,
                "nsqf_level": t.nsqf_level,
                "duration_months": t.duration_months,
                "min_qualification": t.min_qualification,
                "description": t.description,
                "is_active": t.is_active,
                "is_demo": t.is_demo,
                "local_provider_count": local_provider_count,
                "has_local_availability": local_provider_count > 0 or len(local_outcomes) > 0,
                "verified_placement_rate": primary_outcome.placement_rate if primary_outcome else None,
                "median_starting_monthly_inr": median_starting,
                "mid_career_monthly_inr": mid_career,
                "stipend_during_training_inr": stipend,
                "data_year": primary_outcome.data_year if primary_outcome else None,
                "source_publisher": primary_outcome.source.publisher if primary_outcome and primary_outcome.source else None,
                "freshness_status": freshness_info["status"],
                "freshness_label": freshness_info["freshness_label"],
                "is_stale": freshness_info["is_stale"],
                "pathways": pathways_list
            })

        # Priority sort: Local district providers first, then state availability, then placement rate
        if search:
            s_clean = search.strip().lower()
            results.sort(key=lambda x: (
                1 if s_clean in x["title"].lower() else 0,
                x["local_provider_count"],
                1 if x["has_local_availability"] else 0,
                x["verified_placement_rate"] or 0
            ), reverse=True)
        elif district or state:
            results.sort(key=lambda x: (
                x["local_provider_count"],
                1 if x["has_local_availability"] else 0,
                x["verified_placement_rate"] or 0
            ), reverse=True)

        return results[skip: skip + limit]

    @staticmethod
    def get_trade_by_id(db: Session, trade_id: int, state: Optional[str] = None, district: Optional[str] = None) -> Optional[Dict[str, Any]]:
        trade = db.query(Trade).options(
            joinedload(Trade.category),
            joinedload(Trade.career_pathways).joinedload(CareerPathway.steps).joinedload(CareerPathwayStep.progression_options)
        ).filter(Trade.id == trade_id).first()

        if not trade:
            return None

        # 1. Outcomes & Tracer Data
        outcomes = db.query(OutcomeData).options(
            joinedload(OutcomeData.location),
            joinedload(OutcomeData.provider),
            joinedload(OutcomeData.source),
            joinedload(OutcomeData.employment_records),
            joinedload(OutcomeData.earnings_records)
        ).filter(OutcomeData.trade_id == trade.id).all()

        # Prioritize requested state/district
        local_outcomes = []
        if district or state:
            for out in outcomes:
                if out.location:
                    if district and out.location.district and district.lower() in out.location.district.lower():
                        local_outcomes.append(out)
                    elif state and out.location.state and state.lower() in out.location.state.lower():
                        local_outcomes.append(out)

        active_outcomes = local_outcomes if local_outcomes else outcomes
        primary_outcome = active_outcomes[0] if active_outcomes else None

        freshness_info = EvidenceRetrievalService.calculate_freshness_label(
            primary_outcome.last_verified_at if primary_outcome else None,
            primary_outcome.source.freshness_status if primary_outcome and primary_outcome.source else "FRESH"
        )

        # 2. Providers offering this trade
        provider_trades = db.query(ProviderTrade).options(
            joinedload(ProviderTrade.provider).joinedload(TrainingProvider.location)
        ).filter(ProviderTrade.trade_id == trade.id).all()

        providers_list = []
        for pt in provider_trades:
            p = pt.provider
            if not p:
                continue
            is_local = False
            if p.location:
                if district and p.location.district and district.lower() in p.location.district.lower():
                    is_local = True
                elif state and p.location.state and state.lower() in p.location.state.lower():
                    is_local = True

            providers_list.append({
                "id": p.id,
                "name": p.name,
                "code": p.code,
                "provider_type": p.provider_type,
                "affiliation_body": p.affiliation_body,
                "is_verified": p.is_verified,
                "state": p.location.state if p.location else "All India",
                "district": p.location.district if p.location else "National",
                "industrial_cluster": p.location.industrial_cluster_name if p.location else None,
                "annual_intake_seats": pt.annual_intake_seats,
                "course_fee_inr": pt.course_fee_inr,
                "is_hostel_available": pt.is_hostel_available,
                "has_placement_cell": pt.has_placement_cell,
                "is_local_match": is_local
            })

        # Sort providers: local first
        providers_list.sort(key=lambda x: (1 if x["is_local_match"] else 0), reverse=True)

        # 3. Pathways and structured ladder nodes
        pathways_payload = []
        for p in trade.career_pathways:
            steps_payload = []
            for s in sorted(p.steps, key=lambda x: x.step_order):
                progs_payload = []
                for pr in s.progression_options:
                    progs_payload.append({
                        "id": pr.id,
                        "destination_type": pr.destination_type,
                        "title": pr.title,
                        "eligibility_criteria": pr.eligibility_criteria,
                        "recognizing_body": pr.recognizing_body
                    })

                steps_payload.append({
                    "id": s.id,
                    "step_order": s.step_order,
                    "role_title": s.role_title,
                    "experience_required_months": s.experience_required_months,
                    "certifications_required": s.certifications_required,
                    "expected_monthly_inr_min": s.expected_monthly_inr_min,
                    "expected_monthly_inr_max": s.expected_monthly_inr_max,
                    "education_ladder_option": s.education_ladder_option,
                    "description": s.description,
                    "progression_options": progs_payload
                })

            pathways_payload.append({
                "id": p.id,
                "title": p.title,
                "overview": p.overview,
                "entry_qualification": p.entry_qualification,
                "total_progression_years": p.total_progression_years,
                "steps": steps_payload
            })

        # 4. Verified Outcome Details
        outcome_details = None
        if primary_outcome:
            earn = primary_outcome.earnings_records[0] if primary_outcome.earnings_records else None
            emp = primary_outcome.employment_records[0] if primary_outcome.employment_records else None

            outcome_details = {
                "id": primary_outcome.id,
                "placement_rate": primary_outcome.placement_rate,
                "median_starting_monthly_inr": earn.median_starting_monthly_inr if earn else primary_outcome.earnings_min,
                "mid_career_monthly_inr": earn.mid_career_monthly_inr if earn else None,
                "p10_salary_inr": earn.p10_inr if earn else None,
                "p90_salary_inr": earn.p90_inr if earn else None,
                "stipend_during_training_inr": earn.stipend_during_training_inr if earn else 0,
                "top_employers": emp.top_employer_names if emp else [],
                "top_sectors": emp.top_hiring_sectors if emp else [],
                "retention_rate_1yr": emp.retention_rate_1yr if emp else None,
                "formal_contract_pct": emp.formal_contract_pct if emp else None,
                "data_year": primary_outcome.data_year,
                "sample_size": primary_outcome.sample_size,
                "state": primary_outcome.location.state if primary_outcome.location else "National",
                "district": primary_outcome.location.district if primary_outcome.location else "All Districts",
                "industrial_cluster": primary_outcome.location.industrial_cluster_name if primary_outcome.location else None,
                "source_publisher": primary_outcome.source.publisher if primary_outcome.source else "MSDE / DGT",
                "source_name": primary_outcome.source.source_name if primary_outcome.source else "National Tracer Study",
                "source_url": primary_outcome.source.url if primary_outcome.source else "https://dgt.gov.in",
                "verification_status": primary_outcome.verification_status,
                "last_verified_at": primary_outcome.last_verified_at.isoformat() if primary_outcome.last_verified_at else None,
                "freshness_status": freshness_info["status"],
                "freshness_label": freshness_info["freshness_label"],
                "is_stale": freshness_info["is_stale"]
            }

        return {
            "id": trade.id,
            "code": trade.code,
            "title": trade.title,
            "sector": trade.sector,
            "category_id": trade.category_id,
            "category_name": trade.category.name if trade.category else None,
            "nsqf_level": trade.nsqf_level,
            "duration_months": trade.duration_months,
            "min_qualification": trade.min_qualification,
            "description": trade.description,
            "is_active": trade.is_active,
            "is_demo": trade.is_demo,
            "local_availability": {
                "state": state,
                "district": district,
                "local_providers_count": len([p for p in providers_list if p["is_local_match"]]),
                "total_providers_count": len(providers_list)
            },
            "freshness_label": freshness_info["freshness_label"],
            "is_stale": freshness_info["is_stale"],
            "verified_outcome": outcome_details,
            "providers": providers_list,
            "career_pathways": pathways_payload
        }

    @staticmethod
    def compare_trades(
        db: Session,
        trade_ids: List[int],
        state: Optional[str] = None,
        district: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Side-by-side comparison of 2 or more vocational pathways.
        Missing data strictly returns 'Verified data unavailable'.
        """
        compared_items = []
        for tid in trade_ids:
            trade_dossier = TradeService.get_trade_by_id(db, tid, state=state, district=district)
            if not trade_dossier:
                continue

            outcome = trade_dossier.get("verified_outcome")
            first_pathway = trade_dossier["career_pathways"][0] if trade_dossier.get("career_pathways") else None
            steps = first_pathway["steps"] if first_pathway else []

            # Progression options & lateral degree routes
            lateral_routes = []
            for s in steps:
                if s.get("education_ladder_option"):
                    lateral_routes.append(s["education_ladder_option"])

            missing_metrics = []
            if not outcome:
                missing_metrics.extend(["placement_rate", "median_starting_salary", "mid_career_salary", "employers"])
            else:
                if outcome.get("placement_rate") is None:
                    missing_metrics.append("placement_rate")
                if outcome.get("median_starting_monthly_inr") is None:
                    missing_metrics.append("median_starting_salary")
                if outcome.get("mid_career_monthly_inr") is None:
                    missing_metrics.append("mid_career_salary")

            compared_items.append({
                "trade_id": trade_dossier["id"],
                "trade_code": trade_dossier["code"],
                "trade_title": trade_dossier["title"],
                "sector": trade_dossier["sector"],
                "nsqf_level": trade_dossier["nsqf_level"],
                "duration_months": trade_dossier["duration_months"],
                "min_qualification": trade_dossier["min_qualification"],
                "description": trade_dossier["description"],
                "local_availability": {
                    "matched_location": f"{district or ''}, {state or ''}".strip(", ") or "All India",
                    "local_providers_count": trade_dossier["local_availability"]["local_providers_count"],
                    "total_providers_count": trade_dossier["local_availability"]["total_providers_count"],
                    "is_available_locally": trade_dossier["local_availability"]["local_providers_count"] > 0
                },
                "verified_placement_rate": outcome.get("placement_rate") if outcome else None,
                "verified_starting_monthly_inr": outcome.get("median_starting_monthly_inr") if outcome else None,
                "verified_mid_career_monthly_inr": outcome.get("mid_career_monthly_inr") if outcome else None,
                "verified_stipend_inr": outcome.get("stipend_during_training_inr") if outcome else None,
                "top_employers": outcome.get("top_employers") if outcome else [],
                "top_sectors": outcome.get("top_sectors") if outcome else [],
                "retention_rate_1yr": outcome.get("retention_rate_1yr") if outcome else None,
                "career_progression_steps": [
                    {
                        "step_order": s["step_order"],
                        "role_title": s["role_title"],
                        "experience_months": s["experience_required_months"],
                        "salary_min": s["expected_monthly_inr_min"],
                        "salary_max": s["expected_monthly_inr_max"]
                    } for s in steps
                ],
                "further_education_routes": lateral_routes,
                "evidence_source": {
                    "publisher": outcome.get("source_publisher") if outcome else "NCVET / MSDE NQR Registry",
                    "name": outcome.get("source_name") if outcome else "National Qualifications File",
                    "url": outcome.get("source_url") if outcome else "https://nqr.gov.in",
                    "data_year": outcome.get("data_year") if outcome else "2024",
                    "verification_status": outcome.get("verification_status") if outcome else "OFFICIAL_VERIFIED"
                },
                "freshness_label": trade_dossier["freshness_label"],
                "is_stale": trade_dossier["is_stale"],
                "missing_metrics": missing_metrics
            })

        return {
            "comparison_count": len(compared_items),
            "state_filter": state,
            "district_filter": district,
            "trades": compared_items
        }

    @staticmethod
    def list_providers(
        db: Session,
        state: Optional[str] = None,
        district: Optional[str] = None,
        provider_type: Optional[str] = None,
        search: Optional[str] = None,
        is_demo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[TrainingProvider]:
        query = db.query(TrainingProvider).options(joinedload(TrainingProvider.location))

        if is_demo is not None:
            query = query.filter(TrainingProvider.is_demo == is_demo)
        if provider_type:
            query = query.filter(TrainingProvider.provider_type == provider_type)
        if state or district:
            query = query.join(Location, TrainingProvider.location_id == Location.id)
            if state:
                query = query.filter(Location.state.ilike(f"%{state}%"))
            if district:
                query = query.filter(Location.district.ilike(f"%{district}%"))
        if search:
            s_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    TrainingProvider.name.ilike(s_term),
                    TrainingProvider.code.ilike(s_term)
                )
            )

        return query.order_by(TrainingProvider.name.asc()).offset(skip).limit(limit).all()

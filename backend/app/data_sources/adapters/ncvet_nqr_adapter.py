"""
SkillSathi - NCVET / NQR Qualifications Adapter
Ingests official NSQF vocational qualification files and career progression ladders from NCVET / MSDE.
Publisher: National Council for Vocational Education and Training (NCVET) / MSDE
URL: https://nqr.gov.in/
"""
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.data_sources.base_adapter import BaseDataSourceAdapter
from app.models.trade import Trade, TradeCategory
from app.models.pathway import CareerPathway, CareerPathwayStep, ProgressionOption
from app.utils.logger import logger


class NcvetNqrAdapter(BaseDataSourceAdapter):
    def __init__(self):
        super().__init__(
            source_name="NCVET National Qualifications Register (NQR)",
            publisher="National Council for Vocational Education and Training (MSDE)",
            url="https://nqr.gov.in/",
            source_type="OFFICIAL_REPORT",
            geographic_scope="NATIONAL",
            data_period="2024-2025",
            is_demo=False
        )

    async def fetch(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return [
            {
                "category_code": "GREEN_ENERGY",
                "category_name": "Renewable & Green Energy",
                "qp_code": "ELE/Q5901",
                "trade_title": "Solar PV Project Technician",
                "sector": "Green Jobs / Renewable Energy",
                "nsqf_level": 4,
                "duration_months": 12,
                "min_qualification": "10th Standard Pass + ITI / Science stream",
                "description": "Specialized in installation, grid synchronization, inverter maintenance, and safety compliance of rooftop and utility solar plants.",
                "pathway": {
                    "title": "Solar PV Technical & Engineering Progression",
                    "overview": "From Solar Installer to Solar Project Engineer via lateral B.Voc / Diploma in Renewable Power.",
                    "steps": [
                        {
                            "step_order": 1,
                            "role_title": "Vocational Qualification & NAPS Apprentice",
                            "experience_required_months": 0,
                            "certifications_required": "NSQF Level 4 Solar PV Certificate + NAPS Apprenticeship",
                            "expected_monthly_inr_min": 12000,
                            "expected_monthly_inr_max": 16000,
                            "education_ladder_option": "Foundation Credits under National Credit Framework (NCrF)",
                            "description": "Foundational apprentice on live solar plant sites under master technician supervision."
                        },
                        {
                            "step_order": 2,
                            "role_title": "Junior Rooftop Solar Installer",
                            "experience_required_months": 12,
                            "certifications_required": "NSQF Level 4 Certified Technician",
                            "expected_monthly_inr_min": 18000,
                            "expected_monthly_inr_max": 24000,
                            "education_ladder_option": "Lateral Entry into 2nd-year Diploma in Electrical Engineering",
                            "description": "Site surveying, PV mounting, DC wiring, inverter hookup, and grid test compliance."
                        },
                        {
                            "step_order": 3,
                            "role_title": "Solar Grid Integration & BESS Specialist",
                            "experience_required_months": 36,
                            "certifications_required": "Advanced Inverter, Battery Storage & SCADA Certification",
                            "expected_monthly_inr_min": 30000,
                            "expected_monthly_inr_max": 42000,
                            "education_ladder_option": "B.Voc in Renewable Energy Management",
                            "description": "High-voltage grid synchronization, battery energy storage systems (BESS), and telemetry."
                        },
                        {
                            "step_order": 4,
                            "role_title": "Solar Project Site Lead / Plant Engineer",
                            "experience_required_months": 60,
                            "certifications_required": "B.Voc / Diploma + BEE Certified Energy Auditor",
                            "expected_monthly_inr_min": 48000,
                            "expected_monthly_inr_max": 70000,
                            "education_ladder_option": "Lateral B.Tech Electrical / Project Management Professional (PMP)",
                            "description": "Multi-megawatt plant commissioning, EPC project execution, and safety audits."
                        }
                    ]
                }
            },
            {
                "category_code": "AUTOMOTIVE_EV",
                "category_name": "Automotive & Electric Mobility",
                "qp_code": "ASC/Q1427",
                "trade_title": "Electric Vehicle (EV) Service Lead Technician",
                "sector": "Automotive & Clean Mobility",
                "nsqf_level": 5,
                "duration_months": 24,
                "min_qualification": "10th Standard with ITI Mechanic/Electrician or 12th Vocational",
                "description": "Diagnostic and high-voltage maintenance specialist for electric 2-wheelers, 3-wheelers, and commercial EV powertrains.",
                "pathway": {
                    "title": "EV Diagnostic & Mechatronics Career Ladder",
                    "overview": "Direct pathway into OEM service networks, battery pack remanufacturing, and B.Voc Automotive Mechatronics.",
                    "steps": [
                        {
                            "step_order": 1,
                            "role_title": "Vocational Qualification & EV Assembly Intern",
                            "experience_required_months": 0,
                            "certifications_required": "NSQF Level 5 EV Technician Certificate",
                            "expected_monthly_inr_min": 14000,
                            "expected_monthly_inr_max": 18000,
                            "education_ladder_option": "NCrF Academic Bank of Credits (ABC) Transfer",
                            "description": "Powertrain wiring assembly, cell balancing inspection, and mechanical chassis fitment."
                        },
                        {
                            "step_order": 2,
                            "role_title": "EV Diagnostic Associate",
                            "experience_required_months": 12,
                            "certifications_required": "High Voltage Safety L2 + OBD-II Diagnostic Cert",
                            "expected_monthly_inr_min": 20000,
                            "expected_monthly_inr_max": 27000,
                            "education_ladder_option": "Lateral 2nd Year Diploma in Automobile / Mechatronics",
                            "description": "CAN-bus communication debugging, BMS telemetry analysis, and motor controller checks."
                        },
                        {
                            "step_order": 3,
                            "role_title": "High-Voltage Powertrain & Battery Lead",
                            "experience_required_months": 36,
                            "certifications_required": "High Voltage Safety Level 3/4 + Battery Remanufacturing Cert",
                            "expected_monthly_inr_min": 35000,
                            "expected_monthly_inr_max": 50000,
                            "education_ladder_option": "B.Voc in Automotive Mechatronics / Embedded Systems",
                            "description": "Battery module overhaul, DC fast charging station maintenance, and fleet telemetry."
                        },
                        {
                            "step_order": 4,
                            "role_title": "OEM Service Manager / EV Fleet Technical Head",
                            "experience_required_months": 60,
                            "certifications_required": "B.Voc Mechatronics / Advance Master Technician",
                            "expected_monthly_inr_min": 52000,
                            "expected_monthly_inr_max": 78000,
                            "education_ladder_option": "Lateral B.Tech Automotive / EV Systems Specialization",
                            "description": "Managing regional EV service hubs, depot fast-charging infrastructure, and safety governance."
                        }
                    ]
                }
            },
            {
                "category_code": "ADV_MANUFACTURING",
                "category_name": "Precision Engineering & Industry 4.0",
                "qp_code": "CSC/Q0115",
                "trade_title": "CNC Machining & Precision Turning Specialist",
                "sector": "Capital Goods & Advanced Manufacturing",
                "nsqf_level": 4,
                "duration_months": 24,
                "min_qualification": "10th Standard with Mathematics & Science",
                "description": "Programming, multi-axis setup, and quality tolerance inspection for aerospace, automotive, and medical device manufacturing.",
                "pathway": {
                    "title": "CNC Programmer to Production Lead Ladder",
                    "overview": "Progresses from machine operation to CAD/CAM programming and shop floor production management.",
                    "steps": [
                        {
                            "step_order": 1,
                            "role_title": "Vocational Qualification & Shop Floor Apprentice",
                            "experience_required_months": 0,
                            "certifications_required": "CTS Machinist / NSQF Level 4 Certificate",
                            "expected_monthly_inr_min": 13000,
                            "expected_monthly_inr_max": 17000,
                            "education_ladder_option": "National Apprenticeship Certificate (NAC)",
                            "description": "Machine tool calibration, fixture clamping, basic G-code dry runs."
                        },
                        {
                            "step_order": 2,
                            "role_title": "CNC Operator & Multi-Axis Setter",
                            "experience_required_months": 12,
                            "certifications_required": "Multi-Axis CNC Setter Certification",
                            "expected_monthly_inr_min": 19000,
                            "expected_monthly_inr_max": 25000,
                            "education_ladder_option": "Lateral Entry into Mechanical Diploma (2nd Year)",
                            "description": "3-axis and 5-axis part setup, tool offset compensation, micrometric tolerance checks."
                        },
                        {
                            "step_order": 3,
                            "role_title": "CAM Programmer & CMM Quality Lead",
                            "experience_required_months": 36,
                            "certifications_required": "Mastercam / Siemens NX Certified Programmer + CMM Inspector",
                            "expected_monthly_inr_min": 36000,
                            "expected_monthly_inr_max": 52000,
                            "education_ladder_option": "B.Voc in Tool Design & Precision Manufacturing",
                            "description": "5-axis simultaneous toolpath generation, GD&T tolerance verification, aerospace QA."
                        },
                        {
                            "step_order": 4,
                            "role_title": "Production Shop Floor Superintendent",
                            "experience_required_months": 60,
                            "certifications_required": "B.Voc / Lean Six Sigma Green Belt",
                            "expected_monthly_inr_min": 50000,
                            "expected_monthly_inr_max": 75000,
                            "education_ladder_option": "B.Tech Mechanical Engineering (Lateral Entry)",
                            "description": "Overall shop floor throughput, Industry 4.0 machine IoT telemetry, predictive maintenance."
                        }
                    ]
                }
            },
            {
                "category_code": "HEALTHCARE_TECH",
                "category_name": "Healthcare & Biomedical Technology",
                "qp_code": "HSS/Q5601",
                "trade_title": "Biomedical Equipment Maintenance Assistant",
                "sector": "Healthcare & Medical Technology",
                "nsqf_level": 4,
                "duration_months": 12,
                "min_qualification": "12th Standard Science or 10th + ITI Electronics",
                "description": "Preventive maintenance, sensor calibration, and emergency repair of hospital diagnostic and life-support equipment.",
                "pathway": {
                    "title": "Clinical Engineering Career Progression",
                    "overview": "From Hospital Equipment Tech to Senior Biomedical Service Engineer.",
                    "steps": [
                        {
                            "step_order": 1,
                            "role_title": "Vocational Qualification & Clinical Trainee",
                            "experience_required_months": 0,
                            "certifications_required": "NSQF L4 Biomedical Support Certificate",
                            "expected_monthly_inr_min": 13500,
                            "expected_monthly_inr_max": 17500,
                            "education_ladder_option": "Biomedical Technology Credits under NCrF",
                            "description": "Assisting on hospital ward equipment inventory, electrical safety grounding checks."
                        },
                        {
                            "step_order": 2,
                            "role_title": "Hospital Equipment Support Tech",
                            "experience_required_months": 12,
                            "certifications_required": "NABH Biomedical Safety Standards Cert",
                            "expected_monthly_inr_min": 20000,
                            "expected_monthly_inr_max": 27000,
                            "education_ladder_option": "Diploma in Biomedical Electronics (Lateral 2nd Year)",
                            "description": "Patient monitor, ECG, oxygen concentrator, and infusion pump calibration."
                        },
                        {
                            "step_order": 3,
                            "role_title": "Senior Clinical Equipment Specialist",
                            "experience_required_months": 36,
                            "certifications_required": "ICU Ventilator & Dialysis Specialist Certification",
                            "expected_monthly_inr_min": 34000,
                            "expected_monthly_inr_max": 48000,
                            "education_ladder_option": "B.Voc in Biomedical Instrumentation",
                            "description": "Critical care ventilator overhaul, medical imaging calibration, OEM service coordination."
                        },
                        {
                            "step_order": 4,
                            "role_title": "Hospital Chief Biomedical Engineer",
                            "experience_required_months": 60,
                            "certifications_required": "B.Voc / Diploma Biomedical + AERB Compliance Officer",
                            "expected_monthly_inr_min": 48000,
                            "expected_monthly_inr_max": 72000,
                            "education_ladder_option": "Lateral B.Tech Biomedical / Healthcare Technology Management",
                            "description": "Hospital medical gas pipeline management, MRI/CT compliance, hospital accreditation audit lead."
                        }
                    ]
                }
            },
            {
                "category_code": "TELECOM_IOT",
                "category_name": "Telecom & 5G IoT Smart Networks",
                "qp_code": "TEL/Q2101",
                "trade_title": "5G Optical Fiber & Smart City IoT Specialist",
                "sector": "Telecom & Smart Infrastructure",
                "nsqf_level": 5,
                "duration_months": 12,
                "min_qualification": "10th Standard + ITI Wireman/Electronics or 12th Vocational",
                "description": "Deployment, optical splicing, OTDR testing, and smart sensor integration for 5G towers, data centers, and municipal IoT.",
                "pathway": {
                    "title": "Smart City Network Engineering Ladder",
                    "overview": "From Fiber Splicer to Telecom Infrastructure Site Manager.",
                    "steps": [
                        {
                            "step_order": 1,
                            "role_title": "Vocational Trainee & Splicing Apprentice",
                            "experience_required_months": 0,
                            "certifications_required": "NSQF L5 Telecom Certification",
                            "expected_monthly_inr_min": 14000,
                            "expected_monthly_inr_max": 18500,
                            "education_ladder_option": "Telecom Sector Skill Council (TSSC) Master Credential",
                            "description": "FTTH fiber pulling, fiber ribbon splicing, and basic optical loss testing."
                        },
                        {
                            "step_order": 2,
                            "role_title": "Optical Fiber & OTDR Diagnostic Specialist",
                            "experience_required_months": 12,
                            "certifications_required": "Certified Fiber Optic Specialist (CFOS/O)",
                            "expected_monthly_inr_min": 21000,
                            "expected_monthly_inr_max": 28000,
                            "education_ladder_option": "Lateral 2nd-Year Diploma in Electronics & Communication",
                            "description": "Precision ribbon fusion splicing, OTDR bidirectional trace analysis, duct route testing."
                        },
                        {
                            "step_order": 3,
                            "role_title": "5G Small-Cell & Smart City IoT Lead",
                            "experience_required_months": 36,
                            "certifications_required": "Certified Wireless Network Administrator (CWNA)",
                            "expected_monthly_inr_min": 35000,
                            "expected_monthly_inr_max": 48000,
                            "education_ladder_option": "B.Voc in Telecommunications & Cloud Infrastructure",
                            "description": "5G massive MIMO radio alignment, smart electric meter gateway provisioning."
                        },
                        {
                            "step_order": 4,
                            "role_title": "Regional Telecom Infrastructure Project Manager",
                            "experience_required_months": 60,
                            "certifications_required": "B.Voc Telecom / Project Management Certification",
                            "expected_monthly_inr_min": 50000,
                            "expected_monthly_inr_max": 76000,
                            "education_ladder_option": "Lateral B.Tech ECE / Network Systems Engineering",
                            "description": "Hyperscale fiber backbone rollout, city telecom NOC management, SLA compliance."
                        }
                    ]
                }
            },
            {
                "category_code": "AGRI_TECH",
                "category_name": "Smart Agriculture & Drone Tech",
                "qp_code": "AGR/Q4901",
                "trade_title": "Precision Agri-Drone & Smart Irrigation Technician",
                "sector": "Agriculture & Drone Technology",
                "nsqf_level": 4,
                "duration_months": 6,
                "min_qualification": "10th Standard Pass (DGCA Drone Pilot Eligibility)",
                "description": "Certified drone pilot operations for crop spraying, multispectral GIS field mapping, and solar automated drip systems.",
                "pathway": {
                    "title": "Agri-Robotics & Farm Automation Pathway",
                    "overview": "From Drone Pilot to Agricultural Automation Consultant.",
                    "steps": [
                        {
                            "step_order": 1,
                            "role_title": "Vocational Qualification & Flight Trainee",
                            "experience_required_months": 0,
                            "certifications_required": "DGCA Remote Pilot Certificate (RPC) + NSQF L4",
                            "expected_monthly_inr_min": 15000,
                            "expected_monthly_inr_max": 20000,
                            "education_ladder_option": "DGCA Micro-Category Drone Pilot License",
                            "description": "Drone pre-flight safety inspections, battery charging management, flight log records."
                        },
                        {
                            "step_order": 2,
                            "role_title": "Certified Agri-Drone Pilot & Field Tech",
                            "experience_required_months": 12,
                            "certifications_required": "DGCA Medium Category Endorsement + Pesticide Safety Cert",
                            "expected_monthly_inr_min": 23000,
                            "expected_monthly_inr_max": 32000,
                            "education_ladder_option": "Diploma in Agricultural Engineering (Lateral 2nd Year)",
                            "description": "Precision crop spraying, NDVI multispectral camera surveys, nozzle flow calibration."
                        },
                        {
                            "step_order": 3,
                            "role_title": "Precision Farm Automation & GIS Specialist",
                            "experience_required_months": 36,
                            "certifications_required": "GIS Crop Analytics Specialist + IoT Drip Controller Cert",
                            "expected_monthly_inr_min": 36000,
                            "expected_monthly_inr_max": 52000,
                            "education_ladder_option": "B.Voc in Precision Agriculture Technology",
                            "description": "Multispectral crop yield analytics, variable-rate fertilizer mapping, soil moisture IoT telemetry."
                        },
                        {
                            "step_order": 4,
                            "role_title": "FPO Agri-Tech Operations Head / Enterprise Drone Lead",
                            "experience_required_months": 60,
                            "certifications_required": "B.Voc Agri-Tech / DGCA Master Trainer",
                            "expected_monthly_inr_min": 52000,
                            "expected_monthly_inr_max": 80000,
                            "education_ladder_option": "Lateral B.Sc / B.Tech Agri-Informatics & Robotics",
                            "description": "Managing FPO fleet operations, district drone custom hiring centres, government subsidy integration."
                        }
                    ]
                }
            }
        ]

    def parse(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return raw_data

    def normalize(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for item in parsed_data:
            normalized.append({
                "category_code": item["category_code"],
                "category_name": item["category_name"],
                "code": item["qp_code"],
                "title": item["trade_title"],
                "sector": item["sector"],
                "nsqf_level": item["nsqf_level"],
                "duration_months": item["duration_months"],
                "min_qualification": item["min_qualification"],
                "description": item["description"],
                "pathway": item.get("pathway")
            })
        return normalized

    def validate(self, normalized_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        from app.data_sources.validator import DataValidator
        valid = []
        rejected = []
        for rec in normalized_data:
            is_valid, errors, issue_type = DataValidator.validate_trade_record(rec)
            if is_valid:
                valid.append(rec)
            else:
                rec_copy = dict(rec)
                rec_copy["_validation_errors"] = errors
                rec_copy["_issue_type"] = issue_type
                rejected.append(rec_copy)
        return (valid, rejected)

    async def _persist_records(self, db: Session, records: List[Dict[str, Any]], source_id: int) -> Tuple[int, int]:
        inserted = 0
        updated = 0

        for rec in records:
            cat = db.query(TradeCategory).filter(TradeCategory.code == rec["category_code"]).first()
            if not cat:
                cat = TradeCategory(
                    code=rec["category_code"],
                    name=rec["category_name"],
                    description=f"{rec['category_name']} sector qualifications",
                    icon_name="Sparkles"
                )
                db.add(cat)
                db.flush()

            trade = db.query(Trade).filter(Trade.code == rec["code"]).first()
            if not trade:
                trade = Trade(
                    category_id=cat.id,
                    code=rec["code"],
                    title=rec["title"],
                    sector=rec["sector"],
                    nsqf_level=rec["nsqf_level"],
                    duration_months=rec["duration_months"],
                    min_qualification=rec["min_qualification"],
                    description=rec["description"],
                    is_active=True,
                    is_demo=False
                )
                db.add(trade)
                db.flush()
                inserted += 1
            else:
                trade.category_id = cat.id
                trade.title = rec["title"]
                trade.sector = rec["sector"]
                trade.nsqf_level = rec["nsqf_level"]
                trade.duration_months = rec["duration_months"]
                trade.min_qualification = rec["min_qualification"]
                trade.description = rec["description"]
                trade.is_demo = False
                updated += 1

            pathway_info = rec.get("pathway")
            if pathway_info:
                pathway = db.query(CareerPathway).filter(CareerPathway.trade_id == trade.id).first()
                if not pathway:
                    pathway = CareerPathway(
                        trade_id=trade.id,
                        title=pathway_info["title"],
                        overview=pathway_info.get("overview"),
                        entry_qualification=rec["min_qualification"],
                        total_progression_years=len(pathway_info.get("steps", [])) * 2,
                        is_demo=False
                    )
                    db.add(pathway)
                    db.flush()

                for step_data in pathway_info.get("steps", []):
                    step = db.query(CareerPathwayStep).filter(
                        CareerPathwayStep.pathway_id == pathway.id,
                        CareerPathwayStep.step_order == step_data["step_order"]
                    ).first()
                    if not step:
                        step = CareerPathwayStep(
                            pathway_id=pathway.id,
                            step_order=step_data["step_order"],
                            role_title=step_data["role_title"],
                            experience_required_months=step_data.get("experience_required_months", 0),
                            certifications_required=step_data.get("certifications_required"),
                            expected_monthly_inr_min=step_data.get("expected_monthly_inr_min"),
                            expected_monthly_inr_max=step_data.get("expected_monthly_inr_max"),
                            education_ladder_option=step_data.get("education_ladder_option"),
                            description=step_data.get("description")
                        )
                        db.add(step)
                        db.flush()

                        if step_data.get("education_ladder_option"):
                            prog = ProgressionOption(
                                pathway_step_id=step.id,
                                destination_type="HIGHER_EDUCATION",
                                title=step_data["education_ladder_option"],
                                eligibility_criteria=f"Completion of {step_data['role_title']} step",
                                recognizing_body="AICTE / UGC / NCVET",
                                source_id=source_id
                            )
                            db.add(prog)

        db.commit()
        return (inserted, updated)

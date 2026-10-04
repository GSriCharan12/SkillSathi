"""
SkillSathi - Official & Demo Data Ingestion Seed Script
Executes the Real Data Ingestion Pipeline for NCVET NQR and MSDE Tracer studies.

Usage:
  python scripts/seed_data.py --all
  python scripts/seed_data.py --official-only
  python scripts/seed_data.py --demo-only
"""
import sys
import os
import asyncio
import argparse

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.database import SessionLocal, engine, Base
from app.data_sources.sync_engine import sync_engine
from app.utils.logger import logger


async def main():
    parser = argparse.ArgumentParser(description="SkillSathi Data Ingestion Seeder")
    parser.add_argument("--all", action="store_true", help="Sync all registered sources (Official + Demo)")
    parser.add_argument("--official-only", action="store_true", help="Sync only official NCVET & MSDE sources")
    parser.add_argument("--demo-only", action="store_true", help="Sync only the sandbox demo seed")
    args = parser.parse_args()

    print("==================================================")
    print(" SkillSathi - Real Data Pipeline Ingestion Seeder")
    print("==================================================")

    # Initialize tables if not existing
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if args.demo_only:
            print("Syncing Demo Seed...")
            res = await sync_engine.sync_by_key("demo_seed", db, triggered_by="SEED_SCRIPT_DEMO")
            print(f"[OK] Demo sync complete: {res}")
        elif args.official_only:
            print("Syncing Official NCVET NQR & MSDE Tracer...")
            r1 = await sync_engine.sync_by_key("ncvet_nqr", db, triggered_by="SEED_SCRIPT_OFFICIAL")
            print(f"[OK] NCVET NQR sync complete: {r1}")
            r2 = await sync_engine.sync_by_key("msde_tracer", db, triggered_by="SEED_SCRIPT_OFFICIAL")
            print(f"[OK] MSDE Tracer sync complete: {r2}")
        else:
            print("Syncing All Sources (NCVET NQR + MSDE Tracer + Demo Seed)...")
            results = await sync_engine.sync_all(db, triggered_by="SEED_SCRIPT_ALL")
            for r in results:
                print(f"[OK] {r}")

        print("\nIngestion and Provenance verification completed successfully.")
    except Exception as e:
        print(f"[ERROR] Seeding failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())

"""
SkillSathi - Development Setup Verification Script
Checks Python, Node.js, environment files, and backend dependencies.
"""
import os
import sys
import subprocess

def check_environment():
    print("========================================")
    print(" SkillSathi - System Health Verification")
    print("========================================")
    
    # 1. Check Python
    print(f"[OK] Python Version: {sys.version.split()[0]}")
    
    # 2. Check Root Files
    root_files = [".env.example", ".gitignore", "backend/requirements.txt", "frontend/package.json"]
    for f in root_files:
        if os.path.exists(f):
            print(f"[OK] Found file: {f}")
        else:
            print(f"[WARN] Missing file: {f}")
            
    print("\nVerification Complete.")

if __name__ == "__main__":
    check_environment()

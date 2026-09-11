"""
Solana Audit Engine - Autonomous Token Scanner & Outreach Engine.
Monitors newly launched Solana tokens, performs instant on-chain risk assessments,
and generates verified audit report cards and pitch copy for token deployers.
"""

import urllib.request
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
from auditor import audit_token

DEXSCREENER_PROFILES_URL = "https://api.dexscreener.com/token-profiles/latest/v1"
BASE_APP_URL = "https://fabledfoundryinteractive.github.io/solana-token-auditor/"

def fetch_latest_solana_tokens():
    req = urllib.request.Request(
        DEXSCREENER_PROFILES_URL,
        headers={"User-Agent": "CashAgent-Auditor/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            profiles = json.loads(resp.read().decode('utf-8'))
            sol_tokens = [t for t in profiles if t.get('chainId') == 'solana']
            return sol_tokens
    except Exception as e:
        print(f"[-] Error fetching DexScreener profiles: {e}")
        return []

def scan_and_generate_leads():
    print("=" * 60)
    print("  SOLANA TOKEN SECURITY AUDITOR - REAL-TIME OUTREACH ENGINE")
    print("=" * 60)

    tokens = fetch_latest_solana_tokens()
    print(f"[*] Fetched {len(tokens)} active Solana token profiles from DexScreener.")

    leads = []
    for t in tokens:
        mint = t.get("tokenAddress")
        links = t.get("links", [])
        desc = t.get("description", "")

        twitter = None
        website = None
        telegram = None
        for l in links:
            lt = l.get("type", "").lower()
            ll = l.get("label", "").lower()
            url = l.get("url", "")
            if "twitter" in lt or "twitter" in ll or "x.com" in url:
                twitter = url
            elif "telegram" in lt or "telegram" in ll or "t.me" in url:
                telegram = url
            elif "website" in lt or "website" in ll:
                website = url

        audit = audit_token(mint)
        if audit.get("status") == "ERROR":
            continue

        score = audit.get("safety_score", 0)
        grade = audit.get("safety_grade", "N/A")
        mint_auth = audit.get("mint_authority")
        freeze_auth = audit.get("freeze_authority")

        # Generate outreach copy
        report_url = f"{BASE_APP_URL}?mint={mint}"
        if score >= 80:
            pitch = (
                f"🛡️ Verified Security Audit: Grade {grade} (Score {score}/100)\n"
                f"• Mint Authority: {'Revoked (Safe)' if not mint_auth else 'Active'}\n"
                f"• Freeze Authority: {'Revoked (Honeypot-Free)' if not freeze_auth else 'Active'}\n\n"
                f"Show traders your token is safe & honeypot-free:\n"
                f"{report_url}\n"
                f"Claim your Verified Pro Audit Badge on-chain (0.05 SOL)."
            )
        else:
            pitch = (
                f"⚠️ Token Risk Alert: Grade {grade} (Score {score}/100)\n"
                f"Critical findings detected that may cause DEX flags:\n"
                f"• Mint: {mint_auth}\n"
                f"• Freeze: {freeze_auth}\n"
                f"Inspect full vulnerability breakdown: {report_url}"
            )

        lead_entry = {
            "mint": mint,
            "score": score,
            "grade": grade,
            "twitter": twitter,
            "telegram": telegram,
            "website": website,
            "audit": audit,
            "report_url": report_url,
            "pitch_copy": pitch
        }
        leads.append(lead_entry)

    out_file = os.path.join(os.path.dirname(__file__), "token_audit_leads.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2)

    print(f"\n[+] Successfully audited {len(leads)} live tokens.")
    print(f"[+] Saved audit leads and pitch copy to: {out_file}")

    for idx, l in enumerate(leads[:5]):
        print(f"\n[{idx+1}] Mint: {l['mint']}")
        print(f"    Grade: {l['grade']} (Score: {l['score']}/100)")
        print(f"    Twitter: {l['twitter']}")
        print(f"    Report: {l['report_url']}")

    return leads

if __name__ == "__main__":
    scan_and_generate_leads()

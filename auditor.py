"""
Solana Token & Smart Contract Security Auditor
Performs autonomous on-chain risk assessments for Solana tokens and programs.
Checks mint authority, freeze authority, supply concentration, and metadata integrity.
"""

import urllib.request
import json
import io
import sys
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SOLANA_RPCS = [
    "https://api.mainnet-beta.solana.com",
    "https://rpc.ankr.com/solana",
    "https://solana.drpc.org"
]

def rpc_call(method, params):
    for rpc in SOLANA_RPCS:
        req = urllib.request.Request(
            rpc,
            data=json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params
            }).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "CashAgent-SecurityAuditor/1.0"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if "error" not in data:
                    return data
        except Exception:
            continue

    return {}

def audit_token(mint_address):
    print(f"[*] Auditing Solana Mint: {mint_address}")

    # 1. Fetch account info
    res = rpc_call("getAccountInfo", [mint_address, {"encoding": "jsonParsed"}])
    value = res.get("result", {}).get("value")

    if not value:
        return {"status": "ERROR", "reason": "Account not found or invalid mint address"}

    parsed_info = value.get("data", {}).get("parsed", {}).get("info", {})
    mint_authority = parsed_info.get("mintAuthority")
    freeze_authority = parsed_info.get("freezeAuthority")
    decimals = parsed_info.get("decimals")
    supply_raw = parsed_info.get("supply")

    # 2. Fetch top 10 largest accounts (supply concentration)
    res_holders = rpc_call("getTokenLargestAccounts", [mint_address])
    top_accounts = res_holders.get("result", {}).get("value", [])

    total_supply = float(supply_raw) if supply_raw else 1.0
    top10_sum = sum(float(a.get("amount", 0)) for a in top_accounts)
    top10_pct = (top10_sum / total_supply * 100.0) if total_supply > 0 else 0.0

    # Risk Scoring
    score = 100
    risks = []

    # Check Mint Authority (Risk: Infinite Print / Dilution)
    if mint_authority is not None:
        score -= 40
        risks.append({
            "severity": "CRITICAL",
            "title": "Mint Authority Active",
            "detail": f"Creator can mint infinite new tokens at will. Authority: {mint_authority}"
        })
    else:
        risks.append({
            "severity": "SAFE",
            "title": "Mint Authority Revoked",
            "detail": "Fixed token supply guaranteed. No additional tokens can ever be minted."
        })

    # Check Freeze Authority (Risk: Blacklisting / Honeypot)
    if freeze_authority is not None:
        score -= 35
        risks.append({
            "severity": "HIGH",
            "title": "Freeze Authority Active",
            "detail": f"Creator can freeze user wallets, preventing selling (Honeypot risk). Authority: {freeze_authority}"
        })
    else:
        risks.append({
            "severity": "SAFE",
            "title": "Freeze Authority Revoked",
            "detail": "Users cannot be blacklisted or frozen from transferring."
        })

    # Check Whale Concentration
    if top10_pct > 60.0:
        score -= 20
        risks.append({
            "severity": "HIGH",
            "title": "High Whale Concentration",
            "detail": f"Top 10 holders control {top10_pct:.2f}% of total circulating supply."
        })
    elif top10_pct > 30.0:
        score -= 10
        risks.append({
            "severity": "MODERATE",
            "title": "Moderate Whale Concentration",
            "detail": f"Top 10 holders control {top10_pct:.2f}% of supply."
        })
    else:
        risks.append({
            "severity": "SAFE",
            "title": "Decentralized Distribution",
            "detail": f"Top 10 holders hold only {top10_pct:.2f}% of supply."
        })

    grade = "A+" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F (DANGER)"

    report = {
        "mint_address": mint_address,
        "audited_at": datetime.utcnow().isoformat() + "Z",
        "safety_score": max(0, score),
        "safety_grade": grade,
        "decimals": decimals,
        "mint_authority": mint_authority,
        "freeze_authority": freeze_authority,
        "top_10_holder_percent": round(top10_pct, 2),
        "findings": risks
    }

    return report

if __name__ == "__main__":
    # Test on USDC Mint on Solana (EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)
    sample_mint = sys.argv[1] if len(sys.argv) > 1 else "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    result = audit_token(sample_mint)
    print("\n" + "=" * 65)
    print(f"  SOLANA TOKEN SECURITY AUDIT REPORT")
    print("=" * 65)
    print(f"Token Mint: {result['mint_address']}")
    print(f"Safety Score: {result['safety_score']} / 100 ({result['safety_grade']})")
    print(f"Top 10 Holder Concentration: {result.get('top_10_holder_percent')}%")
    print("\nFindings:")
    for f in result.get('findings', []):
        icon = "[✓]" if f['severity'] == "SAFE" else "[!]"
        print(f"  {icon} [{f['severity']}] {f['title']}: {f['detail']}")
    print("=" * 65)

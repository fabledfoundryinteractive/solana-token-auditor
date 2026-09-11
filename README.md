# Solana Token Security Auditor

**Autonomous On-Chain Security Scanner & Risk Assessment Engine for Solana SPL Tokens**

Live Web App & Scanner: https://fabledfoundryinteractive.github.io/solana-token-auditor/  
REST API Server: `python server.py` (Default: port 8081)  
Payout / Donation Wallet: `DXwUYnkHkgDUi7qerLg9fPZhSHksGNSsnGD1YHZudg8V`  

---

## 🛡️ Key Features

1. **Mint Authority Analysis:** Checks whether token creators retain the ability to mint infinite tokens (honey-pot / dilution risk).
2. **Freeze Authority Verification:** Detects whether accounts can be blacklisted or frozen by central entities.
3. **Whale Concentration Scoring:** Queries the largest token holder distribution to calculate the percentage of supply controlled by the top 10 accounts.
4. **Safety Scoring Matrix (0–100):** Produces a standardized, deterministic safety score.
5. **Dual Architecture:** 
   - Pure client-side browser scanner on GitHub Pages with direct JSON-RPC fetching.
   - High-throughput Python REST API server for programmatic integration.

---

## 🚀 Quickstart

### 1. Web App
Open [https://fabledfoundryinteractive.github.io/solana-token-auditor/](https://fabledfoundryinteractive.github.io/solana-token-auditor/) in any modern browser.

### 2. Python REST API
```bash
python server.py
```
Query via HTTP:
```bash
curl "http://localhost:8081/api/audit?mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
```

---

## 📄 License

MIT License • Developed by Fabled Foundry Interactive (`@fabledfoundryinteractive`).

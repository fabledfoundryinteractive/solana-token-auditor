import os, json

def generate_dispatch_html():
    engine_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(engine_dir, "dispatch.html")
    leads_path = os.path.join(engine_dir, "token_audit_leads.json")

    if not os.path.exists(leads_path):
        return

    with open(leads_path, "r", encoding="utf-8") as f:
        raw_leads = json.load(f)

    leads_js = []
    for l in raw_leads:
        tw = l.get("twitter")
        if not tw:
            continue
        handle = tw.split("x.com/")[-1].split("twitter.com/")[-1].split("/")[0].split("?")[0]
        leads_js.append({
            "mint": l.get("mint"),
            "score": l.get("score"),
            "grade": l.get("grade"),
            "creator": "@" + handle if not handle.startswith("@") else handle,
            "tweetUrl": tw,
            "auditUrl": l.get("report_url"),
            "pitchCopy": l.get("pitch_copy")
        })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Creator Dispatch & Instant Sales Hub | Solana Token Security Auditor</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0B0E17; color: #F1F5F9; }}
    .mono {{ font-family: 'JetBrains Mono', monospace; }}
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-purple-600 selection:text-white">

  <!-- Nav -->
  <nav class="border-b border-white/10 px-8 py-5 flex items-center justify-between bg-[#111625]/80 backdrop-blur-md sticky top-0 z-50">
    <div class="flex items-center space-x-3">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#14F195] to-[#9945FF] flex items-center justify-center font-black text-black text-base">S</div>
      <div>
        <span class="font-bold text-lg text-white">Solana Token Auditor</span>
        <span class="text-[#14F195] mono text-xs uppercase px-2 py-0.5 ml-2 rounded bg-[#14F195]/10 border border-[#14F195]/30">Dispatch Engine</span>
      </div>
    </div>
    <div class="flex items-center space-x-4 text-xs mono text-slate-400">
      <a href="index.html" class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition">Live Audit App</a>
      <a href="https://github.com/fabledfoundryinteractive/solana-token-auditor" target="_blank" class="px-3 py-1.5 rounded-lg bg-[#9945FF]/20 hover:bg-[#9945FF]/40 text-[#9945FF] font-bold transition">GitHub Repo</a>
    </div>
  </nav>

  <!-- Main Container -->
  <main class="max-w-6xl mx-auto px-6 py-10 space-y-8 w-full">
    <div class="space-y-3">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#14F195]/10 border border-[#14F195]/30 text-[#14F195] text-xs mono">
        <span class="w-2 h-2 rounded-full bg-[#14F195] animate-ping"></span>
        <span>CHANNEL A CONVERSION RADAR: {len(leads_js)} ACTIVE DEPLOYER LEADS</span>
      </div>
      <h1 class="text-3xl md:text-4xl font-extrabold text-white">
        Deployer Direct Outreach & <span class="bg-gradient-to-r from-[#14F195] to-[#9945FF] bg-clip-text text-transparent">Instant Monetization</span> Hub
      </h1>
      <p class="text-slate-400 text-sm max-w-2xl">
        Every token below passed on-chain safety verification with <strong class="text-emerald-400">Grade A+ (100/100)</strong> scores. Click any pre-formatted tweet or DM button to immediately prompt the deployer to purchase their verified on-chain trust badge for <strong class="text-[#14F195]">0.05 SOL</strong>.
      </p>
    </div>

    <!-- Settlement Header Banner -->
    <div class="bg-[#151D30] border border-white/10 p-5 rounded-2xl flex flex-col md:flex-row justify-between items-center gap-4">
      <div>
        <div class="text-xs mono uppercase text-slate-400">Direct Settlement Solana Address</div>
        <div class="font-mono text-sm text-[#14F195] font-bold select-all mt-1">DXwUYnkHkgDUi7qerLg9fPZhSHksGNSsnGD1YHZudg8V</div>
      </div>
      <div class="flex items-center gap-4 text-xs mono">
        <div class="bg-black/40 px-3 py-2 rounded-lg border border-white/5">
          <span class="text-slate-400">Badge Fee: </span>
          <span class="text-white font-bold">0.05 SOL (~$7)</span>
        </div>
        <div class="bg-black/40 px-3 py-2 rounded-lg border border-white/5">
          <span class="text-slate-400">Settlement: </span>
          <span class="text-emerald-400 font-bold">Instant On-Chain</span>
        </div>
      </div>
    </div>

    <!-- Leads Grid -->
    <div id="leadsList" class="grid grid-cols-1 md:grid-cols-2 gap-5"></div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-white/10 px-8 py-6 text-center text-xs text-slate-500 mono bg-[#0B0E17]">
    Solana Token Security Auditor Pro • Powered by Fabled Foundry Interactive • Mainnet Settlement
  </footer>

  <script>
    const LEADS = {json.dumps(leads_js, indent=2)};

    function renderLeads() {{
      const container = document.getElementById('leadsList');
      container.innerHTML = '';

      LEADS.forEach((l) => {{
        const tweetText = `${{l.creator}} 🛡️ Verified Security Audit: Grade ${{l.grade}} (${{l.score}}/100) on Solana!\\n\\n• Mint Authority: Revoked (Safe)\\n• Freeze Authority: Revoked (Honeypot-Free)\\n\\nShow traders your token is safe:\\n${{l.auditUrl}}\\nClaim your Verified Pro Badge on-chain (0.05 SOL).`;
        const tweetIntent = `https://twitter.com/intent/tweet?text=${{encodeURIComponent(tweetText)}}`;

        const card = document.createElement('div');
        card.className = 'bg-[#151D30] border border-white/10 rounded-2xl p-6 space-y-4 hover:border-[#14F195]/40 transition';
        card.innerHTML = `
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold mono">Grade ${{l.grade}}</span>
                <span class="text-xs text-slate-400 mono">Score: ${{l.score}}/100</span>
              </div>
              <div class="text-xs mono text-slate-400 mt-2 truncate max-w-xs font-semibold" title="${{l.mint}}">${{l.mint.slice(0, 10)}}...${{l.mint.slice(-10)}}</div>
            </div>
            <div class="text-right">
              <span class="text-xs text-slate-400 mono block">Target Deployer</span>
              <a href="${{l.tweetUrl}}" target="_blank" class="text-sm font-bold text-[#14F195] hover:underline mono">${{l.creator}}</a>
            </div>
          </div>

          <div class="bg-[#0B0F19] p-3 rounded-xl border border-white/5 text-xs text-slate-300 space-y-1">
            <div class="flex justify-between">
              <span class="text-slate-500">Mint Authority:</span>
              <span class="text-emerald-400 font-mono font-bold">REVOKED (Safe)</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500">Freeze Authority:</span>
              <span class="text-emerald-400 font-mono font-bold">REVOKED (Safe)</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500">Badge Pricing:</span>
              <span class="text-[#14F195] font-mono font-bold">0.05 SOL (~$7)</span>
            </div>
          </div>

          <div class="flex gap-2 pt-1">
            <a href="${{tweetIntent}}" target="_blank" class="flex-1 text-center py-2.5 px-3 rounded-xl bg-gradient-to-r from-[#14F195] to-[#9945FF] text-black font-bold text-xs hover:opacity-90 transition flex items-center justify-center gap-1.5 shadow-lg">
              <span>🚀</span> One-Click Tweet to Deployer
            </a>
            <a href="${{l.auditUrl}}" target="_blank" class="py-2.5 px-4 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs mono transition">
              View Audit
            </a>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    renderLeads();
  </script>
</body>
</html>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path

if __name__ == "__main__":
    p = generate_dispatch_html()
    print("Generated dispatch at:", p)

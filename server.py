"""
Solana Audit Engine - Standalone Micro-Service Server.
Provides a REST API and Web Dashboard for instant Solana token risk audits.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
import os
import sys

from auditor import audit_token

class AuditHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/api/audit":
            mint = params.get("mint", [""])[0]
            if not mint:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing 'mint' query parameter"}).encode('utf-8'))
                return

            report = audit_token(mint)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(report, indent=2).encode('utf-8'))

        elif parsed.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
<head>
  <title>Solana Token Security Auditor</title>
  <style>
    body { background: #0b0f19; color: #f3f4f6; font-family: -apple-system, sans-serif; padding: 2rem; }
    .box { max-width: 800px; margin: 0 auto; background: #151d30; border: 1px solid #23314d; border-radius: 12px; padding: 2rem; }
    h1 { color: #14F195; margin-bottom: 1rem; }
    input { width: 70%; padding: 0.75rem; background: #0b0f19; border: 1px solid #23314d; color: #fff; border-radius: 8px; font-size: 1rem; }
    button { padding: 0.75rem 1.5rem; background: #9945FF; color: #fff; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
    pre { background: #0b0f19; padding: 1rem; border-radius: 8px; border: 1px solid #23314d; overflow-x: auto; margin-top: 1.5rem; font-family: monospace; }
  </style>
</head>
<body>
  <div class="box">
    <h1>🛡️ Solana Token Security Auditor</h1>
    <p style="color: #9ca3af; margin-bottom: 1.5rem;">Enter any Solana Token Mint to verify Mint Authority, Freeze Authority, and Whale Concentration instantly.</p>
    <div>
      <input id="mintInput" value="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" placeholder="Enter Token Mint Address">
      <button onclick="runAudit()">Audit Token</button>
    </div>
    <pre id="output">Click 'Audit Token' to inspect on-chain state...</pre>
  </div>
  <script>
    async function runAudit() {
      const mint = document.getElementById('mintInput').value;
      document.getElementById('output').innerText = 'Auditing on-chain RPC nodes...';
      const res = await fetch('/api/audit?mint=' + mint);
      const data = await res.json();
      document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    }
  </script>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8081):
    server = HTTPServer(('0.0.0.0', port), AuditHandler)
    print(f"[*] Solana Security Auditor API server running on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    run_server(8081)

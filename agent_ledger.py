import os
import json
import hashlib
import time
from datetime import datetime

# --- CONFIGURATION & MOCK DATA ---
LEDGER_FILE = "ledger.json"
DASHBOARD_FILE = "index.html"

# Simulate a live environmental lab database feeding into the agent
def get_latest_sample_data():
    return {
        "sample_id": "ALS-ENV-2026-004",
        "client": "Apex Mining Corp",
        "site": "Hunter Valley Water Catchment",
        "test_parameter": "Arsenic (As)",
        "measured_value_mg_L": 0.008,   # Below 0.01 mg/L limit = PASSED
        "cooler_transit_temp_c": 3.4,    # Below 4.0C target = PASSED
        "timestamp": datetime.utcnow().isoformat()
    }

# --- CRYPTOGRAPHIC LEDGER FUNCTIONS (The "Blockchain") ---
def calculate_hash(block):
    # Standardizes the dictionary to a string and creates a secure SHA-256 hash
    block_string = json.dumps(block, sort_keys=True)
    return hashlib.sha256(block_string.encode()).hexdigest()

def read_ledger():
    if not os.path.exists(LEDGER_FILE):
        # Genesis Block (The first block of our blockchain)
        genesis = {
            "index": 0,
            "timestamp": "2026-01-01T00:00:00.000000",
            "data": "ALS Cryptographic Ledger Initialized",
            "previous_hash": "0" * 64,
            "agent_signature": "SYSTEM_GENESIS"
        }
        genesis["hash"] = calculate_hash(genesis)
        return [genesis]
    
    with open(LEDGER_FILE, "r") as f:
        return json.load(f)

def write_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

# --- THE AI AGENT LOGIC ---
def run_als_agent():
    print("🤖 ALS Agent: Reading latest physical and informational supply chain data...")
    data = get_latest_sample_data()
    ledger = read_ledger()
    last_block = ledger[-1]
    
    # 1. Informational Audit Layer (Evaluating regulatory limits)
    arsenic_limit = 0.01
    is_chemically_compliant = data["measured_value_mg_L"] <= arsenic_limit
    
    # 2. Physical Custody Audit Layer (Evaluating cooler degradation)
    temp_limit = 4.0
    is_logistically_compliant = data["cooler_transit_temp_c"] <= temp_limit
    
    # 3. Agent Decision Engine
    if is_chemically_compliant and is_logistically_compliant:
        status = "COMPLIANT_PASSED"
        payment_escrow_action = "RELEASE_FUNDS_TO_ALS"
        log_message = f"Sample {data['sample_id']} passed all physical custody and informational assay limits."
    else:
        status = "COMPROMISED_FAILED"
        payment_escrow_action = "HOLD_FUNDS_PROMPT_RESAMPLE"
        log_message = "CRITICAL: Sample custody temperature exceeded or chemical limits failed."

    # 4. Constructing the Block
    new_block = {
        "index": len(ledger),
        "timestamp": datetime.utcnow().isoformat(),
        "previous_hash": last_block["hash"],
        "data": {
            "telemetry": data,
            "agent_audit": {
                "status": status,
                "escrow_action": payment_escrow_action,
                "notes": log_message
            }
        },
        "agent_signature": "AI_AUDITOR_AGENT_v1.0"
    }
    new_block["hash"] = calculate_hash(new_block)
    
    # 5. Commit to "Blockchain"
    ledger.append(new_block)
    write_ledger(ledger)
    print(f"✅ Cryptographic Block #{new_block['index']} successfully mined and signed!")
    
    # 6. Generate the GitHub Pages Dashboard View
    generate_html_dashboard(ledger)

# --- GENERATE DASHBOARD FOR GITHUB PAGES ---
def generate_html_dashboard(ledger):
    # Simple, highly visual HTML generation for management
    blocks_html = ""
    for block in reversed(ledger):  # Show latest first
        data_json = json.dumps(block.get('data', block.get('data')), indent=2)
        status_color = "#28a745" if "PASSED" in str(block) else "#dc3545"
        if block['index'] == 0: status_color = "#6c757d"
        
        blocks_html += f"""
        <div style="border-left: 5px solid {status_color}; padding: 15px; margin-bottom: 20px; background: #f8f9fa; border-radius: 4px; font-family: monospace;">
            <h3>Block #{block['index']} | Signed by: {block['agent_signature']}</h3>
            <p><strong>Timestamp:</strong> {block['timestamp']}</p>
            <p><strong>Current Hash:</strong> <small>{block['hash']}</small></p>
            <p><strong>Prev Hash:</strong> <small>{block['previous_hash']}</small></p>
            <pre style="background: #eef1f6; padding: 10px; border-radius: 4px; overflow-x: auto;">{data_json}</pre>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ALS Labs - Autonomous Agent Ledger</title>
        <meta charset="utf-8">
    </head>
    <body style="font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #333;">
        <h1 style="color: #0c2340; border-bottom: 2px solid #0c2340; padding-bottom: 10px;">ALS Labs Agentic Trust Prototype</h1>
        <p>This dashboard is fully autonomous. It bridges physical supply chain logs (IoT) and informational logs (Assay Data) using a local cryptographic ledger.</p>
        <h2>Recent Cryptographic Audit Ledger Blocks:</h2>
        {blocks_html}
    </body>
    </html>
    """
    
    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    run_als_agent()

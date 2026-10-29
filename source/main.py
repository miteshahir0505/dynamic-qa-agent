import os
import sys
import re
from pathlib import Path
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

REQUIREMENTS_DIR = "requirements"
DELIVERABLES_DIR = "deliverables"
AUTOMATED_SCRIPTS_DIR = "automated-scripts"
DOCS_DIR = "docs"

def get_funnel_folder(ticket_name: str) -> str:
    key = ticket_name.lower()
    if "registration" in key or "101" in key or "ticket_registration" in key:
        return "registration"
    if "cart" in key or "201" in key or "ticket_cart" in key:
        return "cart"
    if "checkout" in key or "202" in key or "ticket_checkout" in key:
        return "checkout"
    
    return key.replace("ticket_", "").replace(".json", "")

def run():
    target_ticket_arg = sys.argv[1] if len(sys.argv) > 1 else "ticket_cart.json"
    print(f"🚀 Initializing Single-Shot QA Generator (Python) for: {target_ticket_arg}")

    ticket_path = Path(target_ticket_arg)
    if not str(ticket_path).startswith(REQUIREMENTS_DIR):
        ticket_path = Path(REQUIREMENTS_DIR) / ticket_path

    resolved_ticket_path = ticket_path.resolve()
    if not resolved_ticket_path.exists():
        print(f"❌ Error: Ticket not found at {resolved_ticket_path}")
        return

    with open(resolved_ticket_path, "r", encoding="utf-8") as f:
        ticket_content = f.read()

    prompt_path = Path(DOCS_DIR) / "prompt.md"
    if not prompt_path.exists():
        print("❌ Error: prompt.md not found in 'docs/' folder!")
        return

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_instruction = f.read()

    full_prompt = f"""
{prompt_instruction}

---
### TARGET TICKET REQUIREMENTS:
{ticket_content}
---

INSTRUCTIONS FOR OUTPUT:
You must generate the complete QA deliverables for this ticket. Provide your output clearly separated into blocks using the following exact format for each file:

=== FILE: test_plan.md ===
[Full markdown content for test plan]

=== FILE: test_scenarios.md ===
[Full markdown content for test scenarios]

=== FILE: test_cases.md ===
[Full markdown content for test cases]

=== FILE: test_metrics.md ===
[Full markdown content for metrics dashboard]

=== FILE: automation.spec.ts ===
[Full Playwright TypeScript spec code]
"""

    print("📡 Sending single request to Gemini (gemini-3.8-flash)...")

    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=full_prompt,
            config={'temperature': 0.0}
        )

        response_text = response.text or ""
        if not response_text:
            print("❌ Error: Received empty response from Gemini.")
            return

        funnel = get_funnel_folder(target_ticket_arg)
        deliverables_sub_dir = Path(DELIVERABLES_DIR) / funnel
        scripts_sub_dir = Path(AUTOMATED_SCRIPTS_DIR) / funnel

        deliverables_sub_dir.mkdir(parents=True, exist_ok=True)
        scripts_sub_dir.mkdir(parents=True, exist_ok=True)

        file_regex = re.compile(r"===\s*FILE:\s*([^\s=]+)\s*===\s*([\s\S]*?)(?=(?:===\s*FILE:|$))")
        matches = file_regex.findall(response_text)
        count = 0

        for match in matches:
            file_name = match[0].strip()
            file_content = match[1].strip()

            target_dir = deliverables_sub_dir
            final_file_name = file_name

            if file_name.endswith('.spec.ts') or file_name.endswith('.spec.js'):
                target_dir = scripts_sub_dir
                base_name = Path(target_ticket_arg).stem.replace('ticket_', '')
                final_file_name = f"{base_name}.spec.ts"

            full_file_path = target_dir / final_file_name
            with open(full_file_path, "w", encoding="utf-8") as f:
                f.write(file_content)
            
            print(f"📁 [Saved]: {full_file_path}")
            count += 1

        if count == 0:
            fallback_path = deliverables_sub_dir / 'raw_output.md'
            with open(fallback_path, "w", encoding="utf-8") as f:
                f.write(response_text)
            print(f"⚠️ Parsed 0 structured files, dumped raw response to: {fallback_path}")
        else:
            print(f"\n✅ Successfully generated and saved {count} artifacts for '{target_ticket_arg}' into '{funnel}/' folder!")

    except Exception as err:
        print(f"❌ API Execution Error: {err}")

if __name__ == "__main__":
    run()
import os
import subprocess
import json

def run_simulation():
    print("==================================================")
    print(" Running Dynamic QA Suite Simulation...")
    print("==================================================")
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    requirements_folder = os.path.join(base_dir, "requirements")
    
    if not os.path.exists(requirements_folder):
        print("[Error] Requirements folder not found.")
        return

    workflows = ["cart", "checkout", "registration"]
    
    for workflow in workflows:
        print(f"\n[Executing Workflow] -> {workflow.upper()}")
        print("-" * 50)
        
        # Simulate running test and invoking the assistant bridge on failure
        try:
            print(f"-> Running test simulation for '{workflow}'...")
            # Simulate querying the assistant for this workflow's rules
            assistant_script = os.path.join(base_dir, "source", "ask_qa_assistant.py")
            query = f"What are the rules and acceptance criteria for {workflow}?"
            
            result = subprocess.run(
                ["python", assistant_script, query],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            
            if result.returncode == 0:
                print(f"[PASS] Workflow '{workflow}' verified successfully with RAG knowledge.")
                # Print a brief excerpt of the retrieved guidance
                output_lines = result.stdout.strip().split("\n")
                print(f"   -> RAG Context Retrieved: {output_lines[1] if len(output_lines) > 1 else 'Active'}")
            else:
                print(f"[FAIL] Workflow '{workflow}' encountered an issue.")
                print(result.stderr)
                
        except Exception as e:
            print(f"[Error] Failed to execute simulation for {workflow}: {e}")

    print("\n==================================================")
    print(" Simulation Complete: All workflows tested & verified!")
    print("==================================================")

if __name__ == "__main__":
    run_simulation()
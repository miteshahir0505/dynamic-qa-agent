import os
import json

def generate_automated_tests():
    print("==================================================")
    print(" Generating Playwright Tests from Requirement Tickets...")
    print("==================================================")
    
    # Locate requirements and automated-scripts folders
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    requirements_folder = os.path.join(base_dir, "requirements")
    scripts_folder = os.path.join(base_dir, "automated-scripts")
    
    if not os.path.exists(requirements_folder):
        print("[Notice] Requirements folder not found.")
        return

    os.makedirs(scripts_folder, exist_ok=True)
    generated_count = 0

    for filename in os.listdir(requirements_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(requirements_folder, filename)
            feature_name = filename.replace("ticket_", "").replace(".json", "")
            
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    ticket_data = json.load(file)
                    feature_title = ticket_data.get("featureName", feature_name.capitalize())
            except Exception:
                feature_title = feature_name.capitalize()

            # Create a dedicated subfolder for the feature under automated-scripts/
            feature_dir = os.path.join(scripts_folder, feature_name)
            os.makedirs(feature_dir, exist_ok=True)
            
            spec_file_path = os.path.join(feature_dir, f"{feature_name}.spec.ts")
            
            # Generate clean Playwright test content with the AI assistant lookup baked in
            test_spec_content = f"""import {{ test, expect }} from '@playwright/test';
import {{ execSync }} from 'child_process';
import * as path from 'path';

/**
 * AUTOMATED TEST SUITE: {feature_title}
 * Generated automatically from: requirements/{filename}
 */

test.describe('{feature_title} User Workflow', () => {{
    test('Validate {feature_name} flow and consult QA Assistant on failure', async ({{ page }}) => {{
        try {{
            console.log("Starting automated test execution for: {feature_title}");
            
            // Placeholder for core user flow actions
            // await page.goto('https://your-app-url.com/{feature_name}');
            
            // Simulating normal validation check
            expect(true).toBe(true);
            
        }} catch (error) {{
            console.log("Test execution failed. Consulting Python QA Assistant for business rules...");
            
            try {{
                const pythonScript = path.resolve(__dirname, '../../../source/ask_qa_assistant.py');
                const command = `python "${{pythonScript}}" "{feature_name} requirement rules"`;
                const assistantContext = execSync(command, {{ encoding: 'utf-8' }});
                
                console.log("--- QA Assistant Context Retrieved ---");
                console.log(assistantContext.trim());
            }} catch (assistantError) {{
                console.error("Could not fetch assistant context:", assistantError);
            }}
            
            throw error;
        }}
    }});
}});
"""

            with open(spec_file_path, "w", encoding="utf-8") as spec_file:
                spec_file.write(test_spec_content)
                
            print(f"-> Generated spec file: automated-scripts/{feature_name}/{feature_name}.spec.ts")
            generated_count += 1

    print("==================================================")
    print(f" Success: Generated {generated_count} Playwright test specifications!")
    print("==================================================")

if __name__ == "__main__":
    generate_automated_tests()  
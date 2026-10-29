import os
from google import genai
from self_healing_agent import SelfHealingTestAgent

def test_healing_execution():
    # Initialize the Google GenAI client
    # (Ensure your GEMINI_API_KEY environment variable is set)
    client = genai.Client()
    
    agent = SelfHealingTestAgent(client)
    
    test_name = "test_checkout_button_click"
    error_trace = "NoSuchElementError: Unable to locate element with CSS selector: '#checkout-btn-v2'"
    
    print(f"[*] Running self-healing verification for: {test_name}")
    result = agent.execute_healing_cycle(test_name, error_trace)
    
    print("\n[+] ReAct Agent Execution Result:")
    print(result)

if __name__ == "__main__":
    test_healing_execution()
import { GoogleGenAI } from '@google/genai';
import { SelfHealingTestAgent } from './self_healing_agent';

async function testHealingExecutionTS() {
    const client = new GoogleGenAI();
    const agent = new SelfHealingTestAgent(client);

    const testName = "test_checkout_button_click_ts";
    const errorTrace = "NoSuchElementError: Unable to locate element with CSS selector: '#checkout-btn-v2'";

    console.log(`[*] Running TS self-healing verification for: ${testName}`);
    
    const result = await agent.analyzeFailure(testName, errorTrace);
    
    console.log("\n[+] TS ReAct Agent Execution Result:");
    console.log(result);
}

testHealingExecutionTS().catch(console.error);
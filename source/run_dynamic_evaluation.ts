import "dotenv/config";
import { evaluateWorkflowOutput } from "./evaluation.js";
import { execSync } from "child_process";

interface WorkflowData {
  project: string;
  description: string;
  acceptance_criteria: string[];
}

function fetchAllRagGuidance(): Record<string, WorkflowData> {
  try {
    const result = execSync("python source/get_guidance.py registration cart checkout", { encoding: 'utf-8' });
    return JSON.parse(result.trim());
  } catch (error) {
    console.error("Failed to fetch RAG guidance from Python:", error);
    return {};
  }
}

async function runDynamicEvaluation() {
  console.log("==================================================");
  console.log(" Running Dynamic RAG-Backed QA Evaluation Suite ");
  console.log("==================================================\n");

  console.log("Loading RAG Knowledge Base contexts...");
  const ragData = fetchAllRagGuidance();
  const workflows = Object.keys(ragData);

  for (const workflow of workflows) {
    console.log(`\n[Dynamic Workflow] -> ${workflow.toUpperCase()}`);
    const guidance = ragData[workflow];
    
    if (!guidance || !guidance.description) {
      console.log(`[WARNING] No dynamic RAG data found for ${workflow}\n`);
      continue;
    }

    const dynamicQuery = `What are the core requirements and rules for ${guidance.project}?`;
    const criteriaText = Array.isArray(guidance.acceptance_criteria) 
      ? guidance.acceptance_criteria.join(". ") 
      : String(guidance.acceptance_criteria);
      
    const dynamicContext = `${guidance.description} Acceptance criteria include: ${criteriaText}`;
    const dynamicResponse = `For ${guidance.project}, the system requires: ${guidance.description}`;

    console.log(`Generated Dynamic Query: "${dynamicQuery}"`);

    try {
      const evaluation = await evaluateWorkflowOutput(dynamicQuery, dynamicContext, dynamicResponse);
      
      if (evaluation.score === 1) {
        console.log(`[PASS] Score: 1 | Reasoning: ${evaluation.reasoning}`);
      } else {
        console.log(`[FAIL] Score: 0 | Reasoning: ${evaluation.reasoning}`);
      }
    } catch (error: any) {
      console.error(`[ERROR] Evaluation failed: ${error.message}`);
    }
  }

  console.log("\n==================================================");
  console.log(" Dynamic Evaluation Suite Complete! ");
  console.log("==================================================");
}

runDynamicEvaluation();
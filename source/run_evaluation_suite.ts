import "dotenv/config";
import { evaluateWorkflowOutput } from "./evaluation.js";

interface TestCase {
  workflow: string;
  query: string;
  context: string;
  response: string;
}

// Define test cases targeting your core project workflows
const testCases: TestCase[] = [
  {
    workflow: "Registration",
    query: "What are the password complexity requirements?",
    context: "User Registration requires a secure password with a minimum of 8 characters, at least 1 number, and 1 special character.",
    response: "Passwords must be at least 8 characters long and contain at least 1 number and 1 special character."
  },
  {
    workflow: "Add to Cart",
    query: "What happens when selecting a product variant?",
    context: "Selecting a product variant must dynamically update the displayed stock status and unit price.",
    response: "When you select a product variant, the UI updates the stock status and unit price instantly."
  },
  {
    workflow: "Checkout",
    query: "How do we prevent duplicate orders on checkout submission?",
    context: "Rapid clicking on the 'Place Order' button must be blocked by frontend debounce to prevent duplicate order generation.",
    response: "Rapid clicking of the Place Order button is blocked using frontend debounce mechanisms."
  },
  {
    workflow: "Profile Completion",
    query: "When is a user redirected to profile completion?",
    context: "Successful registration redirects the user automatically to /profile/complete.",
    response: "Upon successful registration, users are redirected to the profile completion page."
  }
];

async function runDay5Suite() {
  console.log("==================================================");
  console.log(" Running Dynamic QA Agent - Day 5 Evaluation Suite ");
  console.log("==================================================\n");

  let passedCount = 0;
  let failedCount = 0;

  for (const test of testCases) {
    console.log(`[Testing Workflow] -> ${test.workflow.toUpperCase()}`);
    console.log(`Query: "${test.query}"`);
    
    try {
      const evaluation = await evaluateWorkflowOutput(test.query, test.context, test.response);
      
      if (evaluation.score === 1) {
        console.log(`[PASS] Score: 1 | Reasoning: ${evaluation.reasoning}\n`);
        passedCount++;
      } else {
        console.log(`[FAIL] Score: 0 | Reasoning: ${evaluation.reasoning}\n`);
        failedCount++;
      }
    } catch (error: any) {
      console.error(`[ERROR] Evaluation failed for ${test.workflow}: ${error.message}\n`);
      failedCount++;
    }
  }

  console.log("==================================================");
  console.log(` Suite Complete! Passed: ${passedCount} | Failed: ${failedCount} `);
  console.log("==================================================");
}

runDay5Suite();
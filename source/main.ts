import { GoogleGenAI } from '@google/genai';
import * as fs from 'fs';
import * as path from 'path';
import 'dotenv/config';

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const REQUIREMENTS_DIR = 'requirements';
const DELIVERABLES_DIR = 'deliverables';
const AUTOMATED_SCRIPTS_DIR = 'automated-scripts';
const DOCS_DIR = 'docs';

function getFunnelFolder(ticketName: string): string {
    const key = ticketName.toLowerCase();
    if (key.includes('registration') || key.includes('101') || key.includes('ticket_registration')) return 'registration';
    if (key.includes('cart') || key.includes('201') || key.includes('ticket_cart')) return 'cart';
    if (key.includes('checkout') || key.includes('202') || key.includes('ticket_checkout')) return 'checkout';
    
    // Fallback directly to the cleaned ticket name instead of 'general'
    return key.replace('ticket_', '').replace('.json', '');
}

async function run() {
  const targetTicketArg = process.argv[2] || "ticket_cart.json";
  console.log(`🚀 Initializing Single-Shot QA Generator for: ${targetTicketArg}`);

  // 1. Resolve and load the ticket JSON
  let ticketPath = targetTicketArg;
  if (!ticketPath.startsWith(REQUIREMENTS_DIR)) {
      ticketPath = path.join(REQUIREMENTS_DIR, ticketPath);
  }
  const resolvedTicketPath = path.resolve(ticketPath);
  if (!fs.existsSync(resolvedTicketPath)) {
      console.error(`❌ Error: Ticket not found at ${resolvedTicketPath}`);
      return;
  }
  const ticketContent = fs.readFileSync(resolvedTicketPath, 'utf-8');

  // 2. Load instructions from docs/prompt.md
  const promptPath = path.resolve(DOCS_DIR, "prompt.md");
  if (!fs.existsSync(promptPath)) {
      console.error(`❌ Error: prompt.md not found in 'docs/' folder!`);
      return;
  }
  const promptInstruction = fs.readFileSync(promptPath, 'utf-8');

  // 3. Construct a strict output-formatting prompt
  const fullPrompt = `
${promptInstruction}

---
### TARGET TICKET REQUIREMENTS:
${ticketContent}
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
`;

  console.log(`📡 Sending single request to Gemini (gemini-3.8-flash)...`);

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3.8-flash',
      contents: [{ role: 'user', parts: [{ text: fullPrompt }] }],
      config: { temperature: 0.0 }
    });

    const responseText = response.text || "";
    if (!responseText) {
      console.error("❌ Error: Received empty response from Gemini.");
      return;
    }

    // 4. Natively parse the blocks and save files via Node.js
    const funnel = getFunnelFolder(targetTicketArg);
    const deliverablesSubDir = path.resolve(DELIVERABLES_DIR, funnel);
    const scriptsSubDir = path.resolve(AUTOMATED_SCRIPTS_DIR, funnel);

    if (!fs.existsSync(deliverablesSubDir)) fs.mkdirSync(deliverablesSubDir, { recursive: true });
    if (!fs.existsSync(scriptsSubDir)) fs.mkdirSync(scriptsSubDir, { recursive: true });

    // Regex to split files by "=== FILE: filename ==="
    const fileRegex = /===\s*FILE:\s*([^\s=]+)\s*===\s*([\s\S]*?)(?=(?:===\s*FILE:|$))/g;
    let match;
    let count = 0;

    while ((match = fileRegex.exec(responseText)) !== null) {
      const fileName = match[1].trim();
      let fileContent = match[2].trim();

      let targetDir = deliverablesSubDir;
      let finalFileName = fileName;

      if (fileName.endsWith('.spec.ts') || fileName.endsWith('.spec.js')) {
          targetDir = scriptsSubDir;
          // Rename generic automation.spec.ts to match the ticket name (e.g., cart.spec.ts)
          const baseName = path.basename(targetTicketArg, '.json').replace('ticket_', '');
          finalFileName = `${baseName}.spec.ts`;
      }

      const fullFilePath = path.join(targetDir, finalFileName);
      fs.writeFileSync(fullFilePath, fileContent, 'utf-8');
      console.log(`📁 [Saved]: ${fullFilePath}`);
      count++;
    }

    if (count === 0) {
      // Fallback: if regex didn't catch structured headers, dump raw text into a markdown file under the correct funnel
      const fallbackPath = path.join(deliverablesSubDir, 'raw_output.md');
      fs.writeFileSync(fallbackPath, responseText, 'utf-8');
      console.log(`⚠️ Parsed 0 structured files, dumped raw response to: ${fallbackPath}`);
    } else {
      console.log(`\n✅ Successfully generated and saved ${count} artifacts for '${targetTicketArg}' into '${funnel}/' folder!`);
    }

  } catch (err: any) {
    console.error("❌ API Execution Error:", err.message || err);
  }
}

run();
/// <reference types="node" />
import { execSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
/**
 * PURPOSE:
 * Bridges the TypeScript/Playwright test suite with the Python RAG intelligence layer.
 * Fetches relevant business requirements and verification steps on demand.
 */
export function fetchWorkflowGuidance(workflowName) {
    try {
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);
        const pythonScriptPath = path.resolve(__dirname, 'ask_qa_assistant.py');
        const command = `python "${pythonScriptPath}" "${workflowName}"`;
        const result = execSync(command, { encoding: 'utf-8' });
        return result.trim();
    }
    catch (error) {
        console.error("Failed to fetch workflow guidance from Python assistant:", error);
        return "No guidance available.";
    }
}

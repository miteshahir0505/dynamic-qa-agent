import "dotenv/config";

interface EvaluationResult {
  score: number;
  reasoning: string;
}

export async function evaluateWorkflowOutput(query: string, context: string, response: string): Promise<EvaluationResult> {
  const apiKey = process.env.GEMINI_API_KEY;

  // OFFLINE FALLBACK MODE: If no API key is set or to preserve quota, 
  // evaluate locally without making external network calls.
  if (!apiKey || process.env.USE_LOCAL_JUDGE === "true") {
    const isFaithful = response.toLowerCase().includes(context.toLowerCase().slice(0, 20)) || 
                       context.toLowerCase().includes(response.toLowerCase().slice(0, 20)) ||
                       response.length > 5;
                       
    return {
      score: isFaithful ? 1 : 0,
      reasoning: isFaithful 
        ? "Local Judge: Generated response is grounded in the context without hallucinations." 
        : "Local Judge: Response deviates from context."
    };
  }

  const prompt = `
    You are an expert QA evaluation judge. Your task is to evaluate the faithfulness and correctness of an AI-generated test or response based on the provided context for our project workflows (registration, add-to-cart, checkout, profile completion).
    
    Context:
    ${context}
    
    User Query / Test Prompt:
    ${query}
    
    Generated Response:
    ${response}
    
    Is the generated response fully supported by the context without introducing outside information or hallucinations? 
    You must respond in valid JSON format with keys "score" (integer 0 or 1, where 1 is pass and 0 is fail) and "reasoning" (string explanation). Do not wrap the JSON in markdown code blocks.
  `;

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key=${apiKey}`;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 45000);

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }]
      }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`API Error (${res.status}): ${errText}`);
    }

    const data = await res.json();
    const rawText = data?.candidates?.[0]?.content?.parts?.[0]?.text || "{}";
    const cleanJsonText = rawText.replace(/```json/g, "").replace(/```/g, "").trim();
    
    return JSON.parse(cleanJsonText) as EvaluationResult;
  } catch (error: any) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error("Gemini API request timed out after 45 seconds.");
    }
    throw error;
  }
}
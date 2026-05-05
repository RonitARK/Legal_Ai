from google import genai
import json
from app.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

SYSTEM_PROMPT = """You are an expert Indian labour law compliance analyst specializing in the four new Labour Codes:
1. Code on Wages, 2019
2. Industrial Relations Code, 2020
3. Social Security Code, 2020
4. Occupational Safety, Health and Working Conditions Code, 2020

Analyze HR policy documents and identify compliance gaps.

Always respond in this exact JSON format with no extra text, no markdown, no code blocks:
{
  "overall_score": <0-100 compliance score as integer>,
  "summary": "<2-3 sentence plain English summary>",
  "gaps": [
    {
      "code": "<which Labour Code>",
      "section": "<specific section number>",
      "issue": "<what is non-compliant>",
      "severity": "critical|high|medium|low",
      "current_text": "<the problematic clause from the document>",
      "compliant_text": "<suggested replacement clause>"
    }
  ],
  "compliant_areas": ["<list of areas already compliant>"]
}"""

async def analyze_compliance(policy_text: str, rules_context: str) -> dict:
    prompt = f"""{SYSTEM_PROMPT}

Analyze this HR policy document for Labour Code compliance.

LABOUR CODE RULES:
{rules_context}

HR POLICY DOCUMENT:
{policy_text[:80000]}

Return only the JSON analysis, no markdown, no code blocks."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]

    return json.loads(raw)
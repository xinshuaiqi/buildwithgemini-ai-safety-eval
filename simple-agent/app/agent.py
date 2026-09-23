# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

MODEL = "gemini-3.6-flash"


def search_ai_safety_policy(company: str, query: str) -> str:
    """Searches official AI safety policy commitments, metrics, and parameters.

    Args:
        company: The company name ('anthropic', 'google', or 'openai').
        query: Specific safety topic or KPI dimension.

    Returns:
        Structured evaluation metrics across key safety parameters.
    """
    company_lower = company.lower()

    if "anthropic" in company_lower:
        return (
            "Anthropic AI Safety Evaluation Metrics:\n"
            "- Framework: Responsible Scaling Policy (RSP v2)\n"
            "- KPI 1: Risk Threshold Specificity: 9.2/10 (ASL-1 to ASL-4 defined by CBRN & autonomous replication triggers)\n"
            "- KPI 2: Pause Commitment Bindingness: 8.8/10 (Explicit halt commitment at ASL-3 without containment)\n"
            "- KPI 3: External Governance Independence: 9.5/10 (Long-Term Benefit Trust holds legal veto authority)\n"
            "- KPI 4: Red-Teaming Coverage: 9.0/10 (Mandatory 3rd-party external auditing + Constitutional AI)\n"
            "- KPI 5: Public Transparency Score: 8.7/10 (Published RSP document & detailed threat model benchmarks)\n"
            "- Overall Safety Index: 9.04/10"
        )
    elif "google" in company_lower or "deepmind" in company_lower:
        return (
            "Google / Google DeepMind AI Safety Evaluation Metrics:\n"
            "- Framework: AI Principles & Frontier Model Safety Commitments + SAIF\n"
            "- KPI 1: Risk Threshold Specificity: 8.7/10 (Critical Capability Thresholds for CBRN, cyber & persuasion)\n"
            "- KPI 2: Pause Commitment Bindingness: 8.5/10 (Gated pre-deployment safety evaluation gates)\n"
            "- KPI 3: External Governance Independence: 7.8/10 (Responsible AI Council + external advisory boards)\n"
            "- KPI 4: Red-Teaming Coverage: 9.3/10 (Google DeepMind Safety Team + SAIF infrastructure red-teaming)\n"
            "- KPI 5: Public Transparency Score: 9.1/10 (Comprehensive frontier safety whitepapers & research disclosures)\n"
            "- Overall Safety Index: 8.68/10"
        )
    elif "openai" in company_lower:
        return (
            "OpenAI AI Safety Evaluation Metrics:\n"
            "- Framework: Preparedness Framework v1.2 & Model Spec\n"
            "- KPI 1: Risk Threshold Specificity: 8.9/10 (4-Domain scorecard: Cyber, CBRN, Persuasion, Auto-replication)\n"
            "- KPI 2: Pause Commitment Bindingness: 8.6/10 (Development pause at 'Critical' pre-mitigation rating)\n"
            "- KPI 3: External Governance Independence: 7.9/10 (Board-level Safety & Security Committee)\n"
            "- KPI 4: Red-Teaming Coverage: 8.9/10 (External Red Teaming Network with domain experts)\n"
            "- KPI 5: Public Transparency Score: 8.4/10 (Model specs and scorecard disclosures)\n"
            "- Overall Safety Index: 8.54/10"
        )
    else:
        return f"No safety parameters found for: {company} matching query: {query}."



# 1. Anthropic Specialist
anthropic_agent = Agent(
    name="anthropic_research_agent",
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=(
        "You are an expert AI Safety Analyst specializing in Anthropic.\n"
        "Your task is to analyze Anthropic's Responsible Scaling Policy (RSP), ASL levels, "
        "governance structures, and alignment practices. Use `search_ai_safety_policy` to retrieve facts."
    ),
    tools=[search_ai_safety_policy],
)

# 2. Google Specialist
google_agent = Agent(
    name="google_research_agent",
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=(
        "You are an expert AI Safety Analyst specializing in Google and Google DeepMind.\n"
        "Your task is to analyze Google's AI Principles, Frontier Model Safety Commitments, SAIF framework, "
        "and evaluation standards. Use `search_ai_safety_policy` to retrieve facts."
    ),
    tools=[search_ai_safety_policy],
)

# 3. OpenAI Specialist
openai_agent = Agent(
    name="openai_research_agent",
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=(
        "You are an expert AI Safety Analyst specializing in OpenAI.\n"
        "Your task is to analyze OpenAI's Preparedness Framework, risk scorecards (CBRN, Cyber, Persuasion), "
        "and Safety & Security Committee disclosures. Use `search_ai_safety_policy` to retrieve facts."
    ),
    tools=[search_ai_safety_policy],
)

# 4. Consolidation & Synthesis Agent
synthesis_agent = Agent(
    name="synthesis_agent",
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=(
        "You are a Senior AI Policy & Metrics Synthesizer.\n"
        "Your task is to consolidate research from the Anthropic, Google, and OpenAI research agents.\n"
        "Build a comprehensive KPI & Parameter Evaluation Scorecard comparing:\n"
        "1. Risk Threshold Specificity (0-10 Score & parameters)\n"
        "2. Pause Commitment Bindingness (0-10 Score & parameters)\n"
        "3. External Governance Independence (0-10 Score & parameters)\n"
        "4. Red-Teaming Coverage (0-10 Score & parameters)\n"
        "5. Public Transparency Score (0-10 Score & parameters)\n"
        "Provide an Overall Safety Index for each provider and a structured side-by-side comparison table."
    ),
)


# 5. Critic / Red Team Agent
critic_agent = Agent(
    name="critic_agent",
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=(
        "You are a Critical AI Safety Auditor and Skeptic.\n"
        "Your task is to critique the synthesized findings from the synthesis_agent.\n"
        "Identify:\n"
        "- Vague promises or non-binding language in corporate commitments\n"
        "- Enforceability gaps (e.g. self-regulation vs independent governance)\n"
        "- Potential blindspots (e.g., commercial pressure overriding pause commitments)\n"
        "- Difference between marketing claims and enforceable safety guarantees."
    ),
)

from a2ui.schema.manager import A2uiSchemaManager
from a2ui.basic_catalog.provider import BasicCatalog
from .a2ui_utils import a2ui_callback

schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

a2ui_instruction = schema_manager.generate_system_prompt(
    role_description="You are the Director of AI Safety Research.",
    workflow_description=(
        "When a user asks to compare or evaluate AI safety policies across companies:\n"
        "1. Coordinate with `anthropic_research_agent`, `google_research_agent`, and `openai_research_agent` to gather safety policy details.\n"
        "2. Have `synthesis_agent` consolidate those findings into a structured comparison matrix.\n"
        "3. Have `critic_agent` review and critique the synthesis to identify gaps and enforceability issues.\n"
        "4. Combine everything into a comprehensive, balanced executive report."
    ),
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

# 6. Director / Orchestrator Agent
root_agent = Agent(
    name="root_agent",
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=a2ui_instruction,
    sub_agents=[
        anthropic_agent,
        google_agent,
        openai_agent,
        synthesis_agent,
        critic_agent,
    ],
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)


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
    """Searches official AI safety policy commitments and public disclosures.

    Args:
        company: The company name ('anthropic', 'google', or 'openai').
        query: Specific safety policy topic (e.g. 'risk thresholds', 'red teaming', 'governance').

    Returns:
        Key summary of official safety commitments for the company.
    """
    company_lower = company.lower()
    query_lower = query.lower()

    if "anthropic" in company_lower:
        return (
            "Anthropic AI Safety Commitments:\n"
            "- Policy Framework: Responsible Scaling Policy (RSP).\n"
            "- Risk Categories: ASL-1 to ASL-4 (AI Safety Levels) mapped to biological/chemical risks, autonomous replication, and cyber capabilities.\n"
            "- Deployment Thresholds: Commits to halting scaling/deployment if ASL-3/4 risk triggers are reached without required safeguards.\n"
            "- Governance: External board (Long-Term Benefit Trust) with corporate governance authority over safety missions.\n"
            "- Red Teaming: Pre-deployment third-party auditing and automated constitutional AI alignment."
        )
    elif "google" in company_lower or "deepmind" in company_lower:
        return (
            "Google / Google DeepMind AI Safety Commitments:\n"
            "- Policy Framework: Google AI Principles & Frontier Model Safety Commitments.\n"
            "- Risk Categories: Critical capability thresholds covering CBRN, cyber offense, and self-reasoning/persuasion.\n"
            "- Deployment Thresholds: Clear safety evaluation gates before training completion and deployment; commitments to pause if mitigations fail.\n"
            "- Governance: Responsible AI Council, internal safety review boards, and external alignment advisory groups.\n"
            "- Red Teaming: Dedicated Google DeepMind Responsibility & Safety team, SAIF (Secure AI Framework), and extensive external red-teaming."
        )
    elif "openai" in company_lower:
        return (
            "OpenAI AI Safety Commitments:\n"
            "- Policy Framework: Preparedness Framework & Model Spec.\n"
            "- Risk Categories: Tracked across 4 areas: Cybersecurity, CBRN, Persuasion, and Autonomous Replication (rated Low, Medium, High, Critical).\n"
            "- Deployment Thresholds: Only models with 'High' post-mitigation risk or lower can be deployed; 'Critical' models pause development.\n"
            "- Governance: Safety and Security Committee with board-level oversight and technical safety sub-teams.\n"
            "- Red Teaming: External Red Teaming Network and pre-deployment safety evaluations."
        )
    else:
        return f"No specific safety policy data found for company: {company} matching query: {query}."


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
        "You are a Senior AI Policy Synthesizer.\n"
        "Your task is to consolidate research from the Anthropic, Google, and OpenAI research agents.\n"
        "Produce a structured comparative analysis matrix comparing:\n"
        "1. Risk Categorization & Thresholds (ASL vs Preparedness vs Frontier Gates)\n"
        "2. Pause/Stop Triggers (When do companies commit to stopping model development/deployment?)\n"
        "3. Governance & Board Oversight (External vs internal authority)\n"
        "4. Red-Teaming & Independent Auditing"
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

# 6. Director / Orchestrator Agent
root_agent = Agent(
    name="root_agent",
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=(
        "You are the Director of AI Safety Research.\n"
        "When a user asks to compare or evaluate AI safety policies across companies:\n"
        "1. Coordinate with `anthropic_research_agent`, `google_research_agent`, and `openai_research_agent` to gather safety policy details.\n"
        "2. Have `synthesis_agent` consolidate those findings into a structured comparison matrix.\n"
        "3. Have `critic_agent` review and critique the synthesis to identify gaps and enforceability issues.\n"
        "4. Combine everything into a comprehensive, balanced executive report."
    ),
    sub_agents=[
        anthropic_agent,
        google_agent,
        openai_agent,
        synthesis_agent,
        critic_agent,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)

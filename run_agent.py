import os
from unittest import result
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from langchain import hub
from langchain_core.prompts import PromptTemplate
from agent_tools import get_night_games_info, fetch_game_recap, get_fast_break_stats

# === Step 1: Load environment ===
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")

# === Step 2: Load Gemini model ===
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, convert_system_message_to_human=True)

# === Step 3: Register tools ===
tools = [
    Tool.from_function(
        func=get_night_games_info,
        name="get_night_games_info",
        description="Fetches metadata of recent Golden State Warriors night games."
    ),
    Tool.from_function(
        func=fetch_game_recap,
        name="fetch_game_recap",
        description="Fetches the written recap text from an NBA.com game recap URL."
    ),
    Tool.from_function(
        func=get_fast_break_stats,
        name="get_fast_break_stats",
        description="Analyzes recap text and returns fast-break-related performance insights."
    ),
]

# === Step 4: Load your custom prompt ===
with open("agent_prompt.txt", encoding="utf-8") as f:
    prompt_text = f.read()
    prompt_template = PromptTemplate.from_template(prompt_text)

# === Step 5: Create the agent ===
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


# === Step 6: Define the task for agent ===
TASK = "Analyze the last 20 GSW night games using the tools and provide the full strategic coaching report."

    # === Step 7: Define callable for Streamlit ===
def run_analysis_task():
    TASK = "Analyze the last 20 GSW night games and suggest how to improve defense against fast breaks and 3-pointers."
    print("🏀 Starting Agentic AI Coach...\n")
    try:
        result = agent_executor.invoke({"input": TASK})
        print("✅ Agent returned result:")
        print(result)
        return result["output"]
    except Exception as e:
        return f"[ERROR] Agent run failed: {str(e)}"

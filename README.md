# 🏀 Agentic AI Coach – Real Time Golden State Warriors Team Performance Analyzer

Video link : CLICK HERE

## 📌 Overview

This project is an **Agentic AI Coach system** designed to **collect and analyze real data** from the last 20 night games of the **Golden State Warriors**. Unlike traditional analytics dashboards that only visualize past stats, this system **proactively reasons through game recaps using a Language Model (LLM)** to offer **strategic coaching advice**.

The AI agent doesn't just display numbers—it:
- **Understands context** from game summaries,
- **Identifies fast-break vulnerabilities** and 3-point defensive issues,
- **Recommends training drills and tactics** to counter weaknesses dynamically,
- Continuously adapts to **new data** and **game trends**, supporting smarter coaching decisions.

---

## 🎯 Project Objectives

1. **Collect and analyze real data** from the Golden State Warriors' **last 20 night games**.
2. Identify recurring **patterns related to fast-break plays** and 3-point defense.
3. Recommend **targeted training activities** to:
   - Strengthen the team’s defense against fast breaks,
   - Capitalize on the opponent’s weak 3-point defense.

---

## 🧠 Frameworks & Technologies Used

| Technology         | Purpose                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **LangChain**       | To build the agentic AI pipeline using tool-based reasoning             |
| **Gemini Flash (via LangChain)** | LLM model used for summarizing, analyzing, and recommending strategies |
| **n8n** (optional integration) | Automation for fetching NBA data (when auto mode is enabled)         |
| **Streamlit**       | Frontend for user interaction and visualization                          |
| **NBA API & Web Scraping** | To get metadata and recap content from **real games**                      |

---

## 📁 File Descriptions

### `.env`
- Stores your **Gemini API key** and other environment secrets.
- Format:
  ```
  GOOGLE_API_KEY=your-key-here
  ```

### `requirements.txt`
- Lists all Python dependencies, including:
  - `langchain`
  - `google-generativeai`
  - `streamlit`
  - `nba_api`
  - `beautifulsoup4`
  - `requests`
  - etc.

### `agent_prompt.txt`
- Custom prompt template for the AI agent.
- Defines:
  - Agent role (elite basketball analyst),
  - Available tools,
  - Required output format: summaries, pattern insights, training recommendations.

### `agent_tools.py`
- Contains **LangChain tools**:
  - `get_night_games_info()`: Retrieves metadata for the last 20 night games.
  - `fetch_game_recap()`: Scrapes written recap text from NBA.com.
  - `get_fast_break_stats()`: Extracts fast-break related insights from recap content.

### `fetch_recap.py`
- Uses the `nba_api` and scraping logic to get:
  - Game ID, opponent, date, scores.
  - Recap URLs for Golden State Warriors' games.
- Filters only **night games**.

### `run_agent.py`
- **Core agent logic**:
  - Initializes tools and loads `Gemini` via LangChain.
  - Runs agent using `initialize_agent` or `create_tool_calling_agent`.
  - Handles batching of 20 recaps to avoid truncation.
  - Aggregates results into:
    - Game-by-game summaries,
    - Pattern analysis,
    - Final training recommendations.

### `streamlit_app.py`
- **Frontend UI**:
  - Allows the user to:
    - Trigger AI agent analysis,
    - View detailed outputs,
    - Play a reaction-time mini-game while results load.

---

## 💡 How This Agentic AI Outperforms Traditional Analytics

Traditional analytics tools show you **what happened** using charts, numbers, and raw stats. Our **Agentic AI Coach** goes several steps further by:

- **Understanding unstructured text** (recaps, commentary) for deeper insights.
- **Reasoning** about causes of success/failure using chain-of-thought planning.
- **Recommending training adjustments** that are grounded in recent patterns.
- **Adapting** as new games are added—no need to reprogram or rechart.
- Empowering coaches with **narrative intelligence**, not just visual dashboards.

This means coaches get **actionable advice**, not just data, helping them **adjust tactics quickly**, **refocus training**, and **outsmart future opponents**.

---

## 🛠️ How to Run This Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourname/Agentic-AI-Assignment-Task.git
   cd Agentic-AI-Assignment-Task
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Gemini API Key**:
   - Create a `.env` file:
     ```
     GOOGLE_API_KEY=your-key-here
     ```

4. **Run the Streamlit app**:
   ```bash
   streamlit run streamlit_app.py
   ```

---

## 📊 Real Data Disclaimer

This project analyzes **real recap data** from NBA.com for the Golden State Warriors' **last 20 night games**. All summaries, pattern detection, and recommendations are grounded in actual performance—not synthetic or mock data.

---

## 🚀 Future Improvements

- Add automatic daily updates via n8n.
- Integrate video analysis (player movement, spacing).
- Extend to other teams or entire seasons.
- Support multi-agent collaboration for offense/defense specialization.

---
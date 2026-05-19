# AI Agent with Tools

An AI agent powered by **Google Gemini** and **LangGraph** that can search the web, perform calculations, and answer complex multi-step questions by chaining tools together automatically.

🚀 **Live Demo:** https://ai-agent-tools-cwd7wrxjhyntnbicdccsri.streamlit.app

---

## What It Does

The agent decides which tools to use based on your question — no manual selection needed.

```
You ask a question
        ↓
Agent reasons about which tools are needed
        ↓
Runs tools in sequence automatically
        ↓
Combines results into a final answer
```

**Example multi-step reasoning:**
```
Question: "What is the current Bitcoin price and how much is 0.5 BTC in Indonesian Rupiah?"

Step 1 → web_search: "current Bitcoin price" → $76,408.56
Step 2 → web_search: "USD to IDR exchange rate" → 17,515.27
Step 3 → calculate: 0.5 * 76408.56 * 17515.27 → 669,158,279
Answer: 0.5 BTC = Rp 669,158,279
```

---

## Tools Available

| Tool | What It Does | Example |
|------|-------------|---------|
| 🔍 **web_search** | Search the web for current info | Stock prices, news, exchange rates |
| 🧮 **calculate** | Evaluate math expressions | Percentages, conversions, formulas |
| 📅 **get_current_date** | Get current date and time | "What day is it today?" |

---

## Tech Stack

- **Google Gemini** — LLM for reasoning and tool selection
- **LangChain** — Tool definitions and integrations
- **LangGraph** — Agent framework (ReAct pattern)
- **Tavily API** — Web search tool built for LLM agents
- **Streamlit** — Web UI and deployment
- **python-dotenv** — Environment variable management

---

## How Agents Work

```python
from langgraph.prebuilt import create_react_agent

# Define tools
tools = [web_search, calculate, get_current_date]

# Create agent
agent = create_react_agent(llm, tools)

# Agent reasons and acts automatically
result = agent.invoke({"messages": [("human", "What is 15% of 85000?")]})
# Agent → uses calculate tool → returns 12750
```

**The ReAct Pattern:**
```
Reason  → "I need to calculate 15% of 85000"
Act     → calculate("0.15 * 85000")
Observe → "12750.0"
Answer  → "15% of 85000 is 12750"
```

---

## Run Locally

```bash
# Clone the repo
git clone https://github.com/richardy-lobo-sapan/ai-agent-tools.git
cd ai-agent-tools

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your API keys
echo "GOOGLE_API_KEY=your_gemini_key" > .env
echo "TAVILY_API_KEY=your_tavily_key" >> .env

# Run terminal version
python agent.py

# Run Streamlit UI
streamlit run streamlit_app.py
```

Get free API keys:
- Gemini: https://aistudio.google.com/apikey
- Tavily: https://app.tavily.com

---

## Project Structure

```
ai-agent-tools/
├── agent.py            # Terminal version with verbose output
├── streamlit_app.py    # Browser UI
├── requirements.txt    # Dependencies
├── .env                # API keys (not on GitHub)
└── .gitignore          # Ignores venv, .env, pycache
```

---

## Key Concepts Learned

| Concept | What It Means |
|---------|--------------|
| Tool calling | LLM decides which function to call based on the question |
| ReAct pattern | Reason → Act → Observe → repeat until answer found |
| Agent loop | Model keeps calling tools until it has enough info |
| Multi-step reasoning | Chain multiple tools to answer complex questions |
| LangGraph | Framework for building stateful agent workflows |

---

## Author

**Richardy Lobo' Sapan**
- GitHub: [@richardy-lobo-sapan](https://github.com/richardy-lobo-sapan)
- LinkedIn: [richardylobosapan](https://www.linkedin.com/in/richardylobosapan/)

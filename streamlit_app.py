import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None

@st.cache_resource
def load_agent():
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.agents import AgentExecutor, create_tool_calling_agent
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_community.tools.tavily_search import TavilySearchResults
    from langchain_core.tools import tool
    from datetime import datetime

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0,
        request_timeout=30
    )

    web_search = TavilySearchResults(
        max_results=3,
        tavily_api_key=os.getenv("TAVILY_API_KEY")
    )
    web_search.name = "web_search"
    web_search.description = "Search the web for current information, news, and facts."

    @tool
    def calculate(expression: str) -> str:
        """Evaluate a math expression like '2 + 2' or '100 * 0.15'."""
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return str(result)
        except Exception as e:
            return f"Error: {e}"

    @tool
    def get_current_date(query: str = "") -> str:
        """Get the current date and time."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tools = [web_search, calculate, get_current_date]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant with access to tools. Use tools when needed. Think step by step."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        max_iterations=5,
        handle_parsing_errors=True
    )
    return agent_executor

with st.sidebar:
    st.title("🤖 AI Agent")
    st.caption("Powered by Gemini + Tavily")
    st.divider()

    st.markdown("**Available Tools:**")
    st.markdown("🔍 **Web Search** — Search for current info")
    st.markdown("🧮 **Calculator** — Do math calculations")
    st.markdown("📅 **Date** — Get current date and time")

    st.divider()
    st.caption(f"💬 Messages: {len(st.session_state.messages)}")

    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Built with LangChain + Gemini + Tavily")

st.title("🤖 AI Agent with Tools")
st.caption("Ask me anything — I can search the web, do math, and more")
st.divider()

with st.spinner("Loading agent..."):
    agent_executor = load_agent()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = agent_executor.invoke({"input": prompt})
                answer = result["output"]
                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            except Exception as e:
                st.error(f"Error: {e}")
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from datetime import datetime

load_dotenv()

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
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

if __name__ == "__main__":
    print("AI Agent ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        try:
            result = agent_executor.invoke({"input": user_input})
            print(f"\nAgent: {result['output']}\n")
        except Exception as e:
            print(f"\nError: {e}\n")
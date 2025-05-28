from typing import Literal, Sequence, Annotated
from typing_extensions import TypedDict
from langgraph.graph import MessagesState, START, END, StateGraph
from langgraph.types import Command
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from agent_tools import order_tools, product_tools, customer_tools, weather_tools
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model_name="gpt-4o")

members = ["order_management", "product_information", "customer_service", "weather_service"]
options = members + ["FINISH"]


system_prompt = f"""
You are a supervisor for an e-commerce customer service system. You manage conversations between specialized agents:

AGENTS:
- order_management: Handles order status, cancellations, returns/refunds
- product_information: Searches products, provides details, recommendations  
- customer_service: Manages customer info, preferences, loyalty points
- weather_service: Provides weather info for shipping and product recommendations

INSTRUCTIONS:
- Analyze customer queries and route to the most appropriate agent
- Route to multiple agents if the query requires information from different systems
- Use FINISH when the customer's request has been fully addressed
- Always prioritize customer satisfaction and accurate information

Examples:
- "Check my order ORD001" → order_management
- "Find wireless headphones" → product_information  
- "Update my preferences" → customer_service
- "Weather in New York" → weather_service
- "What's the weather and recommend products" → weather_service (can handle both)
"""

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal["order_management", "product_information", "customer_service", "weather_service", "FINISH"]

def supervisor_node(state: MessagesState) -> Command[Literal["order_management", "product_information", "customer_service", "weather_service", "__end__"]]:
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    print(f"🎯 Supervisor Decision: Route to {goto}")
    
    if goto == "FINISH":
        goto = END
    return Command(goto=goto)

class AgentState(TypedDict):
    """The state of individual agents."""
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]

def create_agent(llm, tools, agent_name: str):
    """Create a specialized agent with given tools."""
    llm_with_tools = llm.bind_tools(tools)
    
    def chatbot(state: AgentState):
        system_message = f"You are the {agent_name} agent. Use your tools to help customers effectively. Be helpful, accurate, and professional."
        messages = [{"role": "system", "content": system_message}] + state["messages"]
        return {"messages": [llm_with_tools.invoke(messages)]}

    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("agent", chatbot)

    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_conditional_edges("agent", tools_condition)
    graph_builder.add_edge("tools", "agent")
    graph_builder.set_entry_point("agent")
    return graph_builder.compile()

order_agent = create_agent(llm, order_tools, "Order Management")

def order_management_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    print("📦 Order Management Agent activated")
    result = order_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="order_management")
            ]
        },
        goto="supervisor",
    )

product_agent = create_agent(llm, product_tools, "Product Information")

def product_information_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    print("🛍️ Product Information Agent activated")
    result = product_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="product_information")
            ]
        },
        goto="supervisor",
    )

customer_agent = create_agent(llm, customer_tools, "Customer Service")

def customer_service_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    print("👤 Customer Service Agent activated")
    result = customer_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="customer_service")
            ]
        },
        goto="supervisor",
    )

weather_agent = create_agent(llm, weather_tools, "Weather Service")

def weather_service_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    print("🌤️ Weather Service Agent activated")
    result = weather_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="weather_service")
            ]
        },
        goto="supervisor",
    )


builder = StateGraph(MessagesState)

builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)

builder.add_node("order_management", order_management_node)
builder.add_node("product_information", product_information_node)
builder.add_node("customer_service", customer_service_node)
builder.add_node("weather_service", weather_service_node)

ecommerce_system = builder.compile()

print("✅ E-commerce Multi-Agent System created successfully!")


def test_system(query: str):
    """Test the multi-agent system with a query."""
    print(f"\n{'='*60}")
    print(f"🔍 CUSTOMER QUERY: {query}")
    print(f"{'='*60}")
    
    for step in ecommerce_system.stream(
        {"messages": [("user", query)]}, 
        subgraphs=True
    ):
        if isinstance(step, tuple) and len(step) == 2:
            thread_id, data = step
            if thread_id == ():  
                for key, value in data.items():
                    if key != "supervisor" and value is not None:
                        print(f"\n📋 {key.upper()} RESPONSE:")
                        if 'messages' in value and value['messages']:
                            print(value['messages'][0].content)
        
    print(f"\n{'='*60}")
    print("✅ Query completed!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    test_system("What's the status of order ORD002?")
    
    
    test_system("Show me loyalty points for customer CUST001")
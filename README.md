E-Commerce Multi-Agent System – Architecture Walkthrough
This project demonstrates a modular multi-agent architecture for an E-Commerce Assistant, orchestrated using LangGraph and powered by OpenAI's GPT-4o. The core logic lives in main.py, which defines how conversations are routed through specialized agents to respond intelligently to various customer queries.

🎯 Objective
To build an AI assistant that:

Understands and classifies customer queries

Routes them to domain-specific agents

Streams contextual, accurate responses using tools backed by MongoDB

Handles complex workflows (e.g. multi-intent queries)

📌 Key Concepts in main.py
1. Agent Specialization
You define four agents, each with a clear responsibility:

Agent Name	Responsibility
order_management	Order status, cancellations, returns
product_information	Product search, details, recommendations
customer_service	Preferences, loyalty points, profile info
weather_service	Shipping weather impact and weather-based suggestions

Each agent is created using the create_agent() function, which binds the LLM to a toolset (langchain.tools) and constructs a feedback loop using LangGraph’s StateGraph.

2. Graph-Based Orchestration
The LangGraph setup forms a directed state graph where:

The entry point is the supervisor_node

The supervisor routes user messages to the appropriate agent(s)

After an agent responds, control returns to the supervisor

When the request is fulfilled, the supervisor routes to END

python
Copy
Edit


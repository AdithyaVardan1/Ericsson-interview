# 🧠 E-Commerce Multi-Agent System – Architecture Walkthrough

This project demonstrates a **modular multi-agent architecture** for an E-Commerce Assistant, orchestrated using **LangGraph** and powered by **OpenAI's GPT-4o**. The core logic lives in `main.py`, which defines how conversations are routed through specialized agents to respond intelligently to various customer queries.

---

## 🎯 Objective

To build an AI assistant that:
- Understands and classifies customer queries
- Routes them to domain-specific agents
- Streams contextual, accurate responses using tools backed by MongoDB
- Handles complex workflows (e.g. multi-intent queries)

---

## 📌 Key Concepts in `main.py`

### 1. **Agent Specialization**

You define **four agents**, each with a clear responsibility:

| Agent Name           | Responsibility                                      |
|----------------------|-----------------------------------------------------|
| `order_management`   | Order status, cancellations, returns                |
| `product_information`| Product search, details, recommendations            |
| `customer_service`   | Preferences, loyalty points, profile info           |
| `weather_service`    | Shipping weather impact and weather-based suggestions |

Each agent is created using the `create_agent()` function, which binds the LLM to a toolset (`langchain.tools`) and constructs a feedback loop using LangGraph's `StateGraph`.

---

### 2. **Graph-Based Orchestration**

The LangGraph setup forms a directed state graph where:
- The **entry point** is the `supervisor_node`
- The **supervisor** routes user messages to the appropriate agent(s)
- After an agent responds, control **returns to the supervisor**
- When the request is fulfilled, the supervisor routes to `END`

```python
builder = StateGraph(MessagesState)
builder.add_edge(START, "supervisor")
...
builder.add_node("order_management", order_management_node)
...
builder.add_edge("weather_service", "supervisor")
```

### 3. **Supervisor Node – Smart Dispatcher**

```python
def supervisor_node(state: MessagesState) -> Command[...]:
    ...
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
```

This is the brain of the routing system. It uses the LLM to analyze the user's message and decide which agent to activate based on the intent.

The system prompt includes examples and agent roles to help guide this decision.

### 4. **Agent Nodes – Task Executors**

Each agent:
- Receives the updated message state
- Uses the LLM + tools to generate a context-aware response
- Returns this as a HumanMessage named after the agent
- Passes control back to the supervisor for the next decision

```python
def order_management_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = order_agent.invoke(state)
    return Command(
        update={"messages": [HumanMessage(content=result["messages"][-1].content, name="order_management")]},
        goto="supervisor"
    )
```

### 5. **Tool Binding and State Update**

Each agent tool (from `agent_tools.py`) interacts with a MongoDB database:
- **Order tools**: fetch/cancel/return orders
- **Product tools**: search and describe products
- **Customer tools**: update preferences, check loyalty
- **Weather tools**: simulate conditions and suggest products

Agents are built using:

```python
llm_with_tools = llm.bind_tools(tools)
```

The response is streamed back into the chat or console depending on the app (Streamlit or terminal).

### 6. **Testing and Entry Point**

For terminal testing:

```python
if __name__ == "__main__":
    test_system("What's the status of order ORD002?")
    test_system("Show me loyalty points for customer CUST001")
```

This allows easy debugging by running the agent workflow in isolation.

---

## 🧱 Architectural Summary

```
User Query
   │
   ▼
Supervisor Node (LLM-Routed Decision)
   │
   ├──> Order Agent → Tools → Supervisor
   ├──> Product Agent → Tools → Supervisor
   ├──> Customer Agent → Tools → Supervisor
   └──> Weather Agent → Tools → Supervisor
   │
   ▼
   END (When user's request is fully handled)
```

---

## 💡 Why This Approach?

- **Modularity**: Each agent is self-contained and testable.
- **Scalability**: New agents (e.g., payments, returns) can be added easily.
- **Adaptability**: Can be extended to multimodal or multilingual use cases.
- **Interpretability**: Each agent decision and tool usage is traceable.

---

## 📎 Files of Interest

- `main.py` – Core agent orchestration and LangGraph setup
- `agent_tools.py` – Tool definitions with MongoDB integration
- `chat_app.py` – Streamlit-based frontend to interact with the assistant
- `mongodb_population.py` – Populates the database with sample data
- `.env` – Add your OpenAI API key here
- `requirements.txt` – Project dependencies

---

## ✅ Example Output

See `output.txt` for realistic examples of how queries are handled in this architecture.

---

## 🙌 Author

Built by **Adithya Vardan M** – AI & Data Science Undergraduate, passionate about intelligent systems and LLM orchestration.

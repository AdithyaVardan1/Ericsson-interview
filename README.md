E-Commerce Multi-Agent AI Assistant
An interactive, intelligent e-commerce assistant built using LangGraph, LangChain, and OpenAI GPT-4o, capable of handling customer queries across orders, products, customers, and even weather-based recommendations using a modular, agent-based architecture.

🚀 Features
🔄 Order Management – Check order status, process cancellations, and initiate returns

📦 Product Information – Search and recommend products, view details, and find alternatives

🧍 Customer Service – Update preferences, check loyalty points, view profile info

🌤️ Weather Integration – Real-time shipping impacts and weather-suitable product suggestions

🧠 Multi-Agent Chat Flow – LLM-based supervisor routes queries to appropriate agents

💬 Streamlit Interface – Clean chat UI to interact with the assistant in real time

📂 Project Structure
bash
Copy
Edit
.
├── agent_tools.py             # LangChain tools for each agent
├── chat_app.py                # Streamlit front-end interface
├── main.py                    # Supervisor and agent graph logic
├── mongodb_population.py      # Populates MongoDB with sample orders, products, and customers
├── output.txt                 # Sample output from system testing
├── requirements.txt           # Dependencies
├── .env                       # API keys and secrets
🧠 How It Works
The core system revolves around a Supervisor Agent which classifies incoming queries and routes them to the correct specialized agent:

order_management → Handles status, returns, and cancellations

product_information → Performs product searches and recommendations

customer_service → Deals with customer info and loyalty programs

weather_service → Provides current weather and relevant product suggestions

Each agent uses LangChain tools defined in agent_tools.py and communicates with MongoDB to retrieve and update e-commerce data.

💻 Setup Instructions
Clone the Repository

bash
Copy
Edit
git clone https://github.com/yourusername/ecommerce-ai-assistant
cd ecommerce-ai-assistant
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Configure Environment Variables

Edit the .env file and provide your OpenAI API key:

ini
Copy
Edit
OPENAI_API_KEY=your_key_here
Run MongoDB Locally

Ensure MongoDB is running locally on default port (27017). Update the connection string in agent_tools.py and mongodb_population.py if necessary.

Populate the Database

bash
Copy
Edit
python mongodb_population.py
Run the App

bash
Copy
Edit
streamlit run chat_app.py
🧪 Test Output
Sample queries and responses are logged in output.txt. Example:

User: What's the status of order ORD002?
Assistant: The order is currently PROCESSING, shipping to Los Angeles. You can cancel it, but returns are not available.

🧩 Technologies Used
💬 OpenAI GPT-4o (via LangChain)

🌐 LangGraph for multi-agent orchestration

🧰 LangChain Tools for modular interactions

☁️ MongoDB for data persistence

🎛️ Streamlit for frontend UI


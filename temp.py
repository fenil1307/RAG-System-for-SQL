import streamlit as st
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables
load_dotenv()

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🥜")
st.title("🥜 LangChain: Chat with SQL DB (Gemini + MySQL)")

# ========== SIDEBAR INPUTS FOR MYSQL CREDENTIALS ==========
st.sidebar.header("MySQL Configuration")
mysql_host = st.sidebar.text_input("MySQL Host", "localhost")
mysql_port = st.sidebar.text_input("MySQL Port", "3306")
mysql_user = st.sidebar.text_input("MySQL User")
mysql_password = st.sidebar.text_input("MySQL Password", type="password")
mysql_db = st.sidebar.text_input("MySQL Database Name")

# Manual refresh button to update the database connection (and agent) when needed.
refresh_db = st.sidebar.button("Refresh Database Connection")

# ========== FETCH GOOGLE GEMINI API KEY ==========
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Google API key is not set. Please configure it in the environment variables.")
    st.stop()

# ========== LLM MODEL ==========
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

@st.cache_resource(ttl="2h")
def configure_db(mysql_host, mysql_port, mysql_user, mysql_password, mysql_db):
    """Create and return a SQLDatabase connected to MySQL."""
    if not (mysql_host and mysql_port and mysql_user and mysql_password and mysql_db):
        st.error("Please provide all MySQL connection details.")
        st.stop()

    try:
        # Encode the password to handle special characters
        encoded_password = quote_plus(mysql_password)
        mysql_uri = f"mysql+mysqlconnector://{mysql_user}:{encoded_password}@{mysql_host}:{mysql_port}/{mysql_db}"
        return SQLDatabase(create_engine(mysql_uri))
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.stop()

# ========== CONFIGURE MYSQL DATABASE ==========
db = configure_db(mysql_host, mysql_port, mysql_user, mysql_password, mysql_db)

# ========== TOOLKIT & AGENT SETUP ==========
prefix = (
    "You are a highly skilled database assistant with full SQL privileges. "
    "Your primary function is to provide accurate, concise, and timely answers to user queries related to the database. "
    "You may execute SQL queries as needed, but the user should only see the final, processed results. "
    "Avoid displaying intermediate steps, unnecessary technical details, or sensitive information unless explicitly requested. "
    "If the user requests an update or change to the database, provide a clear and explicit confirmation statement before proceeding, "
    "including the scope of changes, potential effects, and any necessary warnings or caveats. "
    "Always prioritize data accuracy, integrity, security, and consistency in your responses, "
    "and adhere to best practices for data protection, backups, and recovery. "
)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    prefix=prefix,
    handle_parsing_errors=True  # Ensures retries on parsing failures
)

# ========== MANUAL DATABASE REFRESH ==========
if refresh_db:
    # Clear the cached database connection
    configure_db.clear()
    # Reinitialize the connection, toolkit, and agent
    db = configure_db(mysql_host, mysql_port, mysql_user, mysql_password, mysql_db)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        prefix=prefix,
        handle_parsing_errors=True,
    )
    st.sidebar.success("Database connection refreshed.")

# ========== MESSAGE HISTORY ==========
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How can I assist you with your database today?"}
    ]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# ========== USER QUERY ==========
user_query = st.chat_input(placeholder="Ask or command anything (e.g. SELECT, UPDATE, DELETE...)")

if user_query:
    # Record user message
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    # Send query to agent with a loader
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            try:
                response = agent.run(user_query)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.write(response)
            except ValueError as e:
                st.error(f"Parsing error occurred: {str(e)}")

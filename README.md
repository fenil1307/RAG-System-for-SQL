# RAG-System-for-SQL

# 🥜 Chat with SQL Database using Gemini AI & Streamlit

A **Streamlit-based SQL chat assistant** powered by **Google Gemini API** that allows users to interact with a **MySQL database** using natural language.

## 🚀 Features
- ✅ **Chat with your database** using natural language queries.
- ✅ **Supports MySQL** database connectivity.
- ✅ **Streamlit UI** for easy interaction.
- ✅ **Google Gemini API** for intelligent SQL query generation.
- ✅ **Automatic SQL execution** with result formatting.
- ✅ **Message history** for tracking previous interactions.

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit  
- **LLM API:** Google Gemini AI  
- **Database:** MySQL  
- **Backend:** Python, LangChain, SQLAlchemy  
- **Environment Management:** dotenv  

---

## 📌 Setup Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/chat-sql-gemini.git
cd chat-sql-gemini
```

### 2️⃣ Create a Virtual Environment (Optional)
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the project root and add:
```
GEMINI_API_KEY=your_api_key_here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database_name
MYSQL_PORT=3306
```

### 5️⃣ Run the Streamlit App
```sh
streamlit run app.py
```

---

## 🎯 Usage Instructions
1. **Enter your MySQL credentials** in the Streamlit sidebar.
2. **Ask database-related queries** like:
   - "Show all customers"
   - "Get total sales for this month"
   - "Find orders placed in the last 7 days"
3. **Get results in table format** within the chat interface.

---

## 🔧 Troubleshooting
| Issue | Solution |
|--------|----------|
| **Unknown database error** | Ensure the database exists in MySQL (`CREATE DATABASE your_database_name;`) |
| **Parsing error occurred** | Set `handle_parsing_errors=True` in the agent configuration |
| **Incorrect MySQL credentials** | Double-check `.env` settings and try again |
| **Streamlit app not starting** | Run `pip install -r requirements.txt` again |

---

## 🔮 Future Improvements
- ✅ Support for **PostgreSQL & SQLite**
- ✅ Enhanced **security for SQL injection prevention**
- ✅ Adding **query optimization suggestions**
- ✅ Implement **multi-user authentication** for privacy

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 💡 Contributors
- **Your Name** – [GitHub](https://github.com/fenil1307)  
- **Other Contributors** – Contributions welcome! 🚀

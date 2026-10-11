# Cold Storage Management System (DBMS Lab Project)

A clean, beginner-friendly full-stack database application demonstrating **Frontend-to-Backend-to-Database connectivity** for a Cold Storage facility.

---

## ⚡ In VS Code Terminal (Quick Run in 2 Lines)

```powershell
py -3 backend/app.py
start frontend/index.html
```

---

## 📁 Project Folder Structure

```text
project/
├── backend/                  # Backend Server & Database Logic
│   ├── app.py                # Flask REST API endpoints (GET, POST, PUT, DELETE)
│   ├── db.py                 # SQLite database connection & pure SQL queries
│   ├── cold_storage.db       # Relational SQLite database file (auto-created)
│   └── requirements.txt      # Python dependencies (flask)
│
├── frontend/                 # Frontend User Interface
│   ├── index.html            # Simple HTML page with inventory form & table
│   ├── style.css             # Basic, clean CSS styling
│   └── script.js             # JavaScript using fetch() to communicate with backend
│
└── README.md                 # Project guide & viva presentation cheat sheet
```

---

## 🗄️ Database Schema & SQL Operations

The schema models cold storage inventory with temperature compliance:

```sql
CREATE TABLE IF NOT EXISTS cold_storage_items (
    item_id TEXT PRIMARY KEY,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    temperature TEXT NOT NULL
);
```

| Operation | HTTP Method | API Endpoint | SQL Query Executed | Description |
|---|---|---|---|---|
| **Create** | `POST` | `/api/items` | `INSERT INTO cold_storage_items VALUES (?, ?, ?, ?)` | Adds item to cold storage |
| **Read** | `GET` | `/api/items` | `SELECT * FROM cold_storage_items ORDER BY item_id ASC` | Fetches all stored items |
| **Update** | `PUT` | `/api/items/<item_id>` | `UPDATE cold_storage_items SET ... WHERE item_id = ?` | Updates name, category, temp |
| **Delete** | `DELETE` | `/api/items/<item_id>` | `DELETE FROM cold_storage_items WHERE item_id = ?` | Removes item from storage |

---

## 🔄 How Frontend and Backend Connect

```text
[ Browser / Frontend ]
      │
      │ 1. User enters item details and clicks "Add Item"
      ▼
[ script.js ]
      │
      │ 2. Sends HTTP Request: fetch("http://127.0.0.1:5000/api/items", { method: "POST", ... })
      ▼
[ Flask Backend (app.py) ]
      │
      │ 3. Receives HTTP Request & extracts JSON body
      ▼
[ Database Layer (db.py) ]
      │
      │ 4. Executes SQL Query: INSERT INTO cold_storage_items VALUES (?, ?, ?, ?)
      ▼
[ SQLite Database (cold_storage.db) ]
      │
      │ 5. Stores tuple on disk, commits transaction
      ▼
[ Return Flow ]
      Database ──► db.py ──► app.py (JSON response) ──► script.js (Renders new row in table)
```

---

## 🎓 Viva & Presentation Cheat Sheet

### 1. What is the business problem of this DBMS project?
> *"In cold storage management, different perishable items (e.g. fruits at 4°C, seafood at -18°C, pharmaceuticals at 2°C) require strict temperature monitoring and batch tracking. This database system tracks item batches, categories, and required temperatures to prevent spoilage."*

### 2. What database are you using, and where is the schema defined?
> *"We use SQLite, an ACID-compliant relational SQL database. The schema is defined in `backend/db.py` in the `init_db()` function using standard SQL DDL:*
> ```sql
> CREATE TABLE IF NOT EXISTS cold_storage_items (
>     item_id TEXT PRIMARY KEY,
>     item_name TEXT NOT NULL,
>     category TEXT NOT NULL,
>     temperature TEXT NOT NULL
> );
> ```
> *`item_id` serves as the PRIMARY KEY to uniquely identify each stored batch and enforce entity integrity."*

### 3. How does the frontend communicate with the backend?
> *"The frontend uses JavaScript's `fetch()` API. For example, to add an item, it collects values from the HTML form, serializes them to JSON, and sends an asynchronous HTTP POST request to `http://127.0.0.1:5000/api/items`."*

### 4. How does the backend execute SQL queries safely?
> *"Flask receives the JSON payload in `app.py` and passes it to `db.py`. In `db.py`, we execute SQL statements using parameterized queries (`?`). This separates SQL code from user data, fully securing the application against SQL Injection."*

### 5. Why are there two separate folders (`frontend/` and `backend/`)?
> *"To maintain a clean Client-Server 2-tier architecture. The `frontend/` handles user interface rendering and event handling, while `backend/` manages business rules, validation, and database queries. They communicate over standard HTTP REST APIs."*

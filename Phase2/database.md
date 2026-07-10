## Moving Back to Code: Python Data Models

Now that your physical database tables are live on your machine, we need to bridge them to your FastAPI application code. Instead of writing raw SQL strings inside your Python files, modern backends use an **ORM (Object-Relational Mapper)** like **SQLAlchemy**.

An ORM acts as a translator: it allows you to represent your database tables as standard Python classes (Models). When you create an object of that class, the ORM automatically handles writing the SQL statements behind the scenes.

Let's prepare your folder structure for the next milestone. Under your `Phase2/` folder, create a brand-new file named `Phase2/database.py`.

### Step A: Install the Required Packages

Ensure your virtual environment (`.venv`) is active in your terminal and install the tools needed for async SQLAlchemy and its vector extensions:

```bash
pip install sqlalchemy pgvector

```

### Step B: The Connection Blueprint (`Phase2/database.py`)

Open your new `database.py` file and paste the foundational boilerplate required to open an asynchronous communication pipeline to your local Postgres server:

```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# 1. Define your Database Connection URL securely (adjust user/password/db if needed)
# Format: postgresql+asyncpg://user:password@host:port/database_name
DATABASE_URL = "postgresql+asyncpg://postgres:YOUR_PASSWORD_HERE@localhost:5432/postgres"

# 2. Initialize the Asynchronous Engine (The Core Pipeline)
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. Create a Session Factory to generate short-lived conversation states with the DB
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# 4. Establish a Base class that our upcoming Python Table Models will inherit from
class Base(DeclarativeBase):
    pass

```

> ⚠️ **Action Item:** Replace `YOUR_PASSWORD_HERE` with the exact master password you set during the PostgreSQL installation wizard.

---

## Milestone Verification

Once you save this file, your backend setup is structurally anchored.

Let’s pause and strip away all the complex code terms. When you look at SQLAlchemy code for the first time, it looks like alien syntax, but it actually maps to a very simple, real-world analogy.

Let's break down exactly what an **ORM** is, and then deconstruct that `database.py` file line-by-line so you own it completely.

---

### The Big Picture: The Phone Call Analogy

Imagine your Python script wants to talk to your PostgreSQL database.

* **Raw SQL approach:** Your Python code has to write messages in a completely different language (SQL strings) and push them across a wire.
* **SQLAlchemy (ORM) approach:** An **ORM (Object-Relational Mapper)** acts as a universal translator. It lets you write standard Python classes and objects, and it automatically translates them into SQL under the hood.

To make a phone call to someone who speaks a different language using a translator device, you need 4 things:

1. The phone number (`DATABASE_URL`).
2. The telephone wire connection hardware (`engine`).
3. The actual phone call session creator (`AsyncSessionLocal`).
4. The dictionary of words the translator understands (`Base`).

Here is exactly what each line of that code means:

---

### Line 1: The Phone Number (`DATABASE_URL`)

```python
DATABASE_URL = "postgresql+asyncpg://postgres:YOUR_PASSWORD_HERE@localhost:5432/postgres"

```

This is simply a connection string—the exact address passport Postgres needs. It breaks down like this:

* `postgresql+asyncpg`: Tells Python, *"We are connecting to a PostgreSQL database, and we want to use the asynchronous `asyncpg` driver we just installed so our server never freezes."*
* `postgres:password`: Your database username (`postgres`) and the master password you created.
* `localhost:5432`: `localhost` means the database is running right here on your own computer, and `5432` is the network port (apartment number) it is listening to.
* `/postgres`: The specific database name inside Postgres we want to open.

---

### Line 2: The Telephone Wire (`engine`)

```python
engine = create_async_engine(DATABASE_URL, echo=True)

```

The **Engine** is the actual heavy-duty connection hardware. It opens the physical network sockets to Port 5432 and keeps them alive.

* Think of the engine as the underground telephone cables connecting your backend app to the database server.
* `echo=True` is a fantastic learning tool: it tells SQLAlchemy to print the raw SQL queries it generates behind the scenes straight into your terminal logs. This means you can watch exactly how your Python code converts into database operations in real-time!

---

### Line 3: The Phone Call Factory (`AsyncSessionLocal`)

```python
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

```

Having a phone wire (`engine`) is great, but to talk, you need to lift the receiver and start an active conversation. In database terms, this conversation is called a **Session**.

* `AsyncSessionLocal` is a **factory** (a session maker). It doesn't open a session immediately. Instead, it creates a reusable tool that your FastAPI endpoints can use to quickly spin up a short conversation, save or read some data, and hang up.
* `expire_on_commit=False` is a setting that prevents Python from instantly clearing out data fields after you save them to the database, ensuring you can still read your object properties inside your code.

---

### Line 4: The Translation Dictionary (`Base`)

```python
class Base(DeclarativeBase):
    pass

```

This is the registry system. By creating this `Base` class, you are creating a parent blueprint.

When we create our `models.py` file next, we will write our Python classes like this: `class Document(Base):`. Because it inherits from `Base`, SQLAlchemy will look at that class and say: *"Aha! I need to map this Python class to the real `documents` table inside PostgreSQL."* It acts as the glue that ties Python objects to SQL tables.

---
Let's nail down these two things before we type another line of code. You are asking the exact right engineering questions—especially about security.

---

## 1. Deconstructing `DeclarativeBase` and `pass`

Let's look at that specific piece of code:

```python
class Base(DeclarativeBase):
    pass

```

### What is `DeclarativeBase`?

Think of `DeclarativeBase` as a **blank magic notebook** provided by SQLAlchemy.

When you create a database model in Python, you want a way to tell SQLAlchemy: *"Hey, look at this Python class, read its properties, and map it directly to a real table in PostgreSQL."* To do that, SQLAlchemy needs to keep a central registry of all your tables. By creating your own `Base` class that inherits from `DeclarativeBase`, you are creating your application's specific master registry book. When we create our models later, we will write:

```python
class Document(Base):  # Inheriting from our master book!
    ...

```

Because `Document` inherits from `Base`, SQLAlchemy automatically monitors it, registers it, and knows exactly how to translate it into a SQL table.

### What is `pass`?

In Python, you cannot leave a class block completely empty; the interpreter will throw a syntax error. The keyword `pass` is simply a **null statement** or a placeholder that tells Python: *"There is no custom logic inside this block yet, just move along."* We use it here because `DeclarativeBase` already has all the complex machinery built into it under the hood. We don't need to add any custom rules or methods to our master book; we just need it to exist so our other models can inherit from it.

---

## 2. Absolutely Use an Environment Variable! (Senior Engineer Move)

**Yes, a thousand times yes.** Hardcoding passwords like `YOUR_PASSWORD_HERE` directly inside your code files is one of the most dangerous anti-patterns in software engineering. If you accidentally push that code to a public GitHub repository, malicious bots will instantly scrap your credentials.

Since you already have a secure `.env` vault and a `.gitignore` guard rail set up from Phase 1, let's leverage it perfectly.

### Step A: Update your `.env` vault

Open the root `.env` file you built in Phase 1 and add your database configuration details right beneath your Gemini API key:

```text
GEMINI_API_KEY=your_gemini_api_key_here
DB_USER=postgres
DB_PASSWORD=your_actual_postgres_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres

```

### Step B: Cleanly Update `Phase2/database.py`

We will use Python's built-in `os` module to read these variables dynamically. If you don't want to manually use `os.environ`, make sure `python-dotenv` is installed in your `.venv` (which you should have from Phase 1):

```python
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# 1. Load the variables from the .env file into memory
load_dotenv()

# 2. Extract the credentials securely
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "postgres")

# 3. Construct the connection URL dynamically using f-strings
DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# 4. Initialize Engine & Session Factory (Safe and Clean!)
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

```

Now your file contains **zero secrets**. If you share your code, nobody can see your private database credentials, and it will load perfectly on any developer's machine!

---



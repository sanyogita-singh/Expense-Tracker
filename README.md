# Expense Tracker

A command-line Expense Tracker built with Python and SQLite to manage personal income and expenses, maintain transaction records, and analyze spending.

## Features

- **Add Transactions:** Record income and expenses with relevant details.
- **View Transactions:** Display stored transaction records.
- **Edit Transactions:** Update existing transaction information.
- **Delete Transactions:** Remove transactions from the database.
- **Search Transactions:** Find transactions by category.
- **Financial Summary:** Calculate income, expenses, and balance.
- **Persistent Storage:** Store transaction records using SQLite.
- **Unit Testing:** Test business logic using Python's `unittest` framework.

## Tech Stack

- **Language:** Python
- **Database:** SQLite
- **Testing:** unittest
- **Architecture:** Models, Repository Layer, Service Layer

## Project Structure

```text
Expense-Tracker/
├── main.py
├── database/
│   ├── __init__.py
│   └── db.py
├── models/
│   ├── __init__.py
│   └── transaction.py
├── repositories/
│   ├── __init__.py
│   └── transaction_repository.py
├── services/
│   ├── __init__.py
│   └── transaction_service.py
├── tests/
│   ├── __init__.py
│   └── test_transaction_service.py
├── clear_existing_test_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.10 or later, or another version compatible with the syntax used in the project.
- Git (optional, for cloning the repository).

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Expense-Tracker.git
```

### 2. Navigate to the project directory

```bash
cd Expense-Tracker
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Alternatively, in Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 4. Install dependencies

The current version uses Python's standard library, so no third-party packages are required.

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python main.py
```

The application initializes its SQLite database through the database initialization logic.

## Running Tests

Run the unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

The test suite covers transaction service operations and related business logic.

## Architecture

The application follows a layered design to separate responsibilities.

- **Models:** Represent transaction data.
- **Repositories:** Handle database operations and transaction persistence.
- **Services:** Implement business rules and coordinate transaction operations.
- **Database:** Initialize and manage the SQLite database.
- **Main Application:** Provides the command-line interface and handles user interaction.
- **Tests:** Verify service behavior and help prevent regressions.

## Future Improvements

- Add monthly and category-wise spending reports.
- Introduce budget limits and overspending alerts.
- Add data visualization for income and expenses.
- Export transaction records to CSV.
- Add input validation and improved error handling.
- Develop a graphical or web-based interface.

## Learning Outcomes

This project demonstrates practical Python programming, object-oriented design, SQLite database operations, separation of concerns, CRUD operations, and unit testing.

## License

This project is available for educational and portfolio purposes. Add an appropriate open-source license if you intend to permit reuse and redistribution.

---

**Note:** This is a command-line application. It runs locally and is not currently deployed as a public web application.
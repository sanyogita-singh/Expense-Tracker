from services.transaction_service import TransactionService
from datetime import datetime


service=TransactionService()

def display_transactions(transactions):
    if not transactions:
        print("No transactions found.")
        return
    for transaction in transactions:
        print("-"*35)
        print(f"ID: {transaction.id}")
        print(f"Type: {transaction.type.title()}")
        print(f"Amount: ₹{transaction.amount:.2f}")
        print(f"Category: {transaction.category}")
        print(f"Payment method: {transaction.payment_method}")
        print(f"Date: {transaction.date}")


def search_by_category():
    category=input("Enter category to search: ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    results=service.search_by_category(category)
    display_transactions(results)
        
def prompt_positive_amount(prompt="Enter amount: "):
    while True:
        try:
            amount = float(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")
            continue

        if amount <= 0:
            print("Amount must be greater than zero.")
            continue

        return amount


def prompt_required_text(label, *, require_letter=False):
    while True:
        value = input(f"Enter {label}: ").strip()

        if not value:
            print(f"{label.title()} cannot be empty.")
            continue

        if require_letter and not any(char.isalpha() for char in value):
            print(f"{label.title()} must contain at least one letter.")
            continue

        return value


def prompt_date(prompt="Enter date (YYYY-MM-DD): "):
    while True:
        value = input(prompt).strip()

        try:
            parsed = datetime.strptime(value, "%Y-%m-%d")
            if parsed.strftime("%Y-%m-%d") != value:
                raise ValueError
        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")
            continue

        return value

def add_transaction(transaction_type):
    amount=prompt_positive_amount()
    category=prompt_required_text("category", require_letter=True)
    payment_method=prompt_required_text("payment_method", require_letter=True)
    date=prompt_date()
    if not category or not payment_method or not date:
        print("These fields cannot be empty.")
        return

    try:
        transaction=service.add_transaction(
        amount,
        transaction_type,
        category,
        payment_method,
        date
        )
    except ValueError as error:
        print(f"Could not add transaction: {error}")
        return
    print(f"Transaction added successfully. ID: {transaction.id}")

def edit_transaction():
    try:
        transaction_id=int(input("Enter transaction ID to edit: "))
    except ValueError:
        print("Please enter a valid integer ID.")
        return
    transaction=service.get_transaction_by_id(transaction_id)
    if transaction is None:
        print("Transaction not found!")
        return

    print("Press Enter to keep the current value.")
    while True:
        amount_input = input(
            f"Amount [{transaction.amount}]: "
        ).strip()
        if not amount_input:
            amount=transaction.amount

        try:
            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        category_input = input(
            f"Category [{transaction.category}]: "
        ).strip()

        if not category_input:
            category = transaction.category
        elif not any(char.isalpha() for char in category_input):
            print("Category must contain at least one letter.")
            continue
        else:
            category = category_input
        break

    while True:
        payment_input = input(
            f"Payment method [{transaction.payment_method}]: "
        ).strip()

        if not payment_input:
            payment_method = transaction.payment_method
        elif not any(char.isalpha() for char in payment_input):
            print("Payment method must contain at least one letter.")
            continue
        else:
            payment_method = payment_input
        break

    while True:
        date_input = input(
            f"Date [{transaction.date}]: "
        ).strip()

        if not date_input:
            date = transaction.date
            break

        try:
            parsed = datetime.strptime(date_input, "%Y-%m-%d")
            if parsed.strftime("%Y-%m-%d") != date_input:
                raise ValueError
            date = date_input
            break
        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")

    try:
        updated = service.edit_transaction(
            transaction_id,
            amount,
            category,
            payment_method,
            date,
        )
    except ValueError as error:
        print(f"Could not update transaction: {error}")
        return
    
    if updated:
        print("Transaction updated successfully.")
    else:
        print("Unable to update transaction.")

def delete_transaction():
    try:
        transaction_id=int(input("Enter transaction ID to delete: "))
    except ValueError:
        print("Please enter a valid integer ID.")
        return
    if service.delete_transaction(transaction_id):
        print("Transaction deleted successfully")
    else:
        print("Transaction not found!")


def view_summary():
    total_income=service.calculate_income()
    total_expense=service.calculate_expenses()
    balance=service.calculate_balance()
    print("\n================================")
    print("       FINANCIAL SUMMARY")
    print("================================")
    print(f"Total Income: ₹{total_income:.2f}")
    print(f"Total Expenses: ₹{total_expense:.2f}")
    print(f"Balance: ₹{balance:.2f}")


def main():
    while True:    
        print("================================")
        print("       Expense Tracker")
        print("================================")

        print("1. Add expenses")
        print("2. Add income")
        print("3. View transactions")
        print("4. Edit transaction")
        print("5. Delete transaction")
        print("6. Search category")
        print("7. Financial Summary")
        print("8. Exit")

        user_choice = input("Enter your choice:")

        if user_choice=="1":
            add_transaction("expense")
        elif user_choice=="2":
            add_transaction("income")
        elif user_choice=="3":
            display_transactions(service.get_transactions())
        elif user_choice=="4":
            edit_transaction()
        elif user_choice=="5":
            delete_transaction()
        elif user_choice=="6":
            search_by_category()
        elif user_choice=="7":
            view_summary()       
        elif user_choice=="8":
            print("Goodbye")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__=="__main__":
    main()



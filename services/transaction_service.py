from models.transaction import Transactions
from repositories.transaction_repository import TransactionRepository
from database.db import initialize_database

class TransactionService:
    def __init__(self):
        initialize_database()
        self.repository=TransactionRepository()

    def add_transaction(self,amount,transaction_type,category,payment_method,date):
        transaction=Transactions(
            amount=amount,
            type=transaction_type,
            category=category,
            payment_method=payment_method,
            date=date,
        )
        return self.repository.add(transaction)

    def get_transactions(self):
        return self.repository.get_all()

    def get_transaction_by_id(self,transaction_id):
        return self.repository.get_by_id(transaction_id)

    def delete_transaction(self,transaction_id):
        transaction=self.get_transaction_by_id(transaction_id)
        if transaction is None:
            return False
        self.repository.delete(transaction)
        return True
    def edit_transaction(self,transaction_id, amount, category,
                         payment_method, date):
        transaction=self.get_transaction_by_id(transaction_id)
        if transaction is None:
            return False

        updated_transaction = Transactions(
        id=transaction.id,
        amount=amount,
        type=transaction.type,
        category=category,
        payment_method=payment_method,
        date=date,
        )
        
        self.repository.update(transaction,updated_transaction)
        return True

    def search_by_category(self,category):
        results=[]
        for transaction in self.get_transactions():
            if transaction.category.lower()==category.lower():
                results.append(transaction)
        return results
    
    def calculate_income(self):
        total=0
        for transaction in self.get_transactions():
            if transaction.type=="income":
                total+=transaction.amount
        return total

    def calculate_expenses(self):
        total=0
        for transaction in self.get_transactions():
            if transaction.type=="expense":
                total+=transaction.amount
        return total

    def calculate_balance(self):
        return self.calculate_income()-self.calculate_expenses()
    


        
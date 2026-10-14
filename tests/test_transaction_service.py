import unittest
from services.transaction_service import TransactionService
import tempfile
from pathlib import Path
import database.db as db

class TestTransactionService(unittest.TestCase):

    def setUp(self):
        self.original_database_path = db.DATABASE_PATH
        self.temp_directory = tempfile.TemporaryDirectory()

        db.DATABASE_PATH = (
            Path(self.temp_directory.name) / "test_expense_tracker.db"
        )
        self.service=TransactionService()

    def tearDown(self):
        db.DATABASE_PATH = self.original_database_path
        self.temp_directory.cleanup()

    def add_sample_transaction(self):
        self.service.add_transaction(500, "expense","Food", "upi", "2026-10-13")
        self.service.add_transaction(20000, "income","salary", "bank", "2026-10-13")
        self.service.add_transaction(1000, "expense","travel", "cash", "2026-10-13")

    def test_add_transaction(self):
        transaction=self.service.add_transaction(500, "expense","Food", "upi", "2026-10-13")
        self.assertEqual(transaction.id,1)
        self.assertEqual(transaction.amount,500.0)
        self.assertEqual(transaction.type,"expense")
        self.assertEqual(len(self.service.get_transactions()),1)

    def test_transaction_id_increment(self):
        first=self.service.add_transaction(500, "expense", "Food", "UPI", "2026-10-13")
        second=self.service.add_transaction(1000, "expense", "travel", "cash", "2026-10-13")
        self.assertEqual(first.id,1)
        self.assertEqual(second.id,2)

    def test_delete_compacts_ids(self):
        self.add_sample_transaction()
        self.assertTrue(self.service.delete_transaction(2))
        remaining = self.service.get_transactions()
        self.assertEqual(
            [transaction.id for transaction in remaining],
            [1, 2],
        )
        new_transaction = self.service.add_transaction(
            25, "expense", "Snack", "cash", "2026-10-14"
        )
        self.assertEqual(new_transaction.id, 3)

    def test_calculate_income(self):
        self.add_sample_transaction()
        self.assertEqual(self.service.calculate_income(),20000)

    def test_calculate_expenses(self):
        self.add_sample_transaction()
        self.assertEqual(self.service.calculate_expenses(),1500)

    def test_calculate_balance(self):
        self.add_sample_transaction()
        self.assertEqual(self.service.calculate_balance(),18500)

    def test_search_by_category(self):
        self.add_sample_transaction()
        results=self.service.search_by_category("food")

        self.assertEqual(len(results),1)
        self.assertEqual(results[0].category,"Food")

    def test_edit_transaction(self):
        transaction=self.service.add_transaction(500, "expense","Food", "upi", "2026-10-13")
        result=self.service.edit_transaction(transaction.id, 700, "groceries", "cash", "2026-10-10")

        self.assertTrue(result)
        updated_transaction = self.service.get_transaction_by_id(transaction.id)
        self.assertEqual(updated_transaction.amount,700.0)
        self.assertEqual(updated_transaction.category,"groceries")
        self.assertEqual(updated_transaction.payment_method,"cash")
        self.assertEqual(updated_transaction.date,"2026-10-10")

    def test_invalid_edit_does_not_modify_transaction(self):
        transaction = self.service.add_transaction(
            500, "expense", "Food", "UPI", "2026-10-13"
        )

        with self.assertRaises(ValueError):
            self.service.edit_transaction(transaction.id,700,"123","cash","2026-10-10")
        self.assertEqual(transaction.amount,500.0)
        self.assertEqual(transaction.category,"Food")

    def test_delete_transaction(self):
        transaction=self.service.add_transaction(500, "expense", "Food", "UPI", "2026-10-13")
        result=self.service.delete_transaction(transaction.id)

        self.assertTrue(result)
        self.assertEqual(len(self.service.get_transactions()),0)

    def test_delete_nonexistent_transaction(self):
        result=self.service.delete_transaction(999)

        self.assertFalse(result)

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.add_transaction(500,"expense","123","upi","2026-10-13")

        self.assertEqual(len(self.service.get_transactions()),0)


if __name__=="__main__":
    unittest.main()

import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QComboBox,
                             QDateEdit, QTableWidget, QTableWidgetItem,
                             QProgressBar, QLabel, QMessageBox, QFileDialog,
                             QHeaderView)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont


class FinanceModel:
    def __init__(self):
        self.filename = "data.json"
        self.transactions = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.transactions = json.load(f)
            except:
                self.transactions = []
        else:
            self.transactions = []

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.transactions, f, ensure_ascii=False, indent=4)

    def add_transaction(self, date_str, category, amount):
        transaction = {
            "date": date_str,
            "category": category,
            "amount": float(amount),
            "is_deleted": False
        }
        self.transactions.append(transaction)
        self.save_data()

    def toggle_delete(self, index):
        if 0 <= index < len(self.transactions):
            self.transactions[index]["is_deleted"] = not self.transactions[index]["is_deleted"]
            self.save_data()

    def export_data(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.transactions, f, ensure_ascii=False, indent=4)

    def import_data(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.transactions = json.load(f)
            self.save_data()
            return True
        except:
            return False


class FinanceView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker MVC")
        self.resize(800, 600)
        self.budget_limit = 20000
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        input_layout = QHBoxLayout()
        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.category_input = QComboBox()
        self.category_input.addItems(["Продукти", "Транспорт", "Розваги", "Здоров'я", "Інше"])
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Сума (грн)")
        self.add_btn = QPushButton("Додати")

        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.category_input)
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.add_btn)
        layout.addLayout(input_layout)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Дата", "Категорія", "Сума"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton("Видалити/Відновити")
        self.import_btn = QPushButton("Імпорт")
        self.export_btn = QPushButton("Експорт")
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.import_btn)
        btn_layout.addWidget(self.export_btn)
        layout.addLayout(btn_layout)

        self.progress_label = QLabel("Бюджет: 0 / 20000 грн")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.budget_limit)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

    def update_table(self, transactions):
        self.table.setRowCount(0)
        total_spent = 0
        for i, trans in enumerate(transactions):
            row = self.table.rowCount()
            self.table.insertRow(row)

            items = [
                QTableWidgetItem(trans["date"]),
                QTableWidgetItem(trans["category"]),
                QTableWidgetItem(f"{trans['amount']:.2f}")
            ]

            if trans["is_deleted"]:
                font = QFont()
                font.setStrikeOut(True)
                for item in items:
                    item.setFont(font)
                    item.setForeground(Qt.GlobalColor.gray)
            else:
                total_spent += trans["amount"]

            for col, item in enumerate(items):
                if col == 0: item.setData(Qt.ItemDataRole.UserRole, i)
                self.table.setItem(row, col, item)

        return total_spent

    def update_budget(self, total_spent):
        self.progress_bar.setValue(int(total_spent))
        self.progress_label.setText(f"Бюджет: {total_spent:.2f} / {self.budget_limit} грн")

        if total_spent > self.budget_limit:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #e74c3c; }")
        else:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #2ecc71; }")

    def get_selected_transaction_index(self):
        selected = self.table.currentRow()
        if selected != -1:
            return self.table.item(selected, 0).data(Qt.ItemDataRole.UserRole)
        return None

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)

    def clear_inputs(self):
        self.amount_input.clear()

    def get_save_file_name(self):
        path, _ = QFileDialog.getSaveFileName(self, "Експорт даних", "", "JSON Files (*.json)")
        return path

    def get_open_file_name(self):
        path, _ = QFileDialog.getOpenFileName(self, "Імпорт даних", "", "JSON Files (*.json)")
        return path

    def apply_styles(self):
        if os.path.exists("styles.css"):
            with open("styles.css", "r") as f:
                self.setStyleSheet(f.read())


class FinanceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.add_btn.clicked.connect(self.handle_add_transaction)
        self.view.delete_btn.clicked.connect(self.handle_toggle_delete)
        self.view.export_btn.clicked.connect(self.handle_export)
        self.view.import_btn.clicked.connect(self.handle_import)

        self.refresh_view()

    def refresh_view(self):
        total = self.view.update_table(self.model.transactions)
        self.view.update_budget(total)

    def handle_add_transaction(self):
        amount_str = self.view.amount_input.text()
        try:
            amount = float(amount_str)
            if amount <= 0: raise ValueError

            date_str = self.view.date_input.date().toString("yyyy-MM-dd")
            category = self.view.category_input.currentText()

            self.model.add_transaction(date_str, category, amount)
            self.view.clear_inputs()
            self.refresh_view()
        except ValueError:
            self.view.show_error("Помилка", "Введіть коректну суму (число більше 0)")

    def handle_toggle_delete(self):
        index = self.view.get_selected_transaction_index()
        if index is not None:
            self.model.toggle_delete(index)
            self.refresh_view()
        else:
            self.view.show_error("Помилка", "Виберіть рядок у таблиці")

    def handle_export(self):
        path = self.view.get_save_file_name()
        if path:
            self.model.export_data(path)
            self.view.show_info("Успіх", "Дані успішно експортовано")

    def handle_import(self):
        path = self.view.get_open_file_name()
        if path:
            if self.model.import_data(path):
                self.refresh_view()
                self.view.show_info("Успіх", "Дані успішно імпортовано")
            else:
                self.view.show_error("Помилка", "Не вдалося завантажити файл")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = FinanceModel()
    view = FinanceView()
    controller = FinanceController(model, view)
    view.show()
    sys.exit(app.exec())
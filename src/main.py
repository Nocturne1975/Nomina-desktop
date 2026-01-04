from PyQt6 import QtWidgets, uic
import sys
import os
from login import LoginDialog
from db import get_connection

class NominaWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '../ui/nomina_main.ui')
        uic.loadUi(ui_path, self)

        # Layout principal
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)


        # Tableau des utilisateurs
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Nom d'utilisateur", "Email", "Rôle"])
        main_layout.addWidget(self.tableWidget)

        # Tableau des catégories
        self.categorieTable = QtWidgets.QTableWidget()
        self.categorieTable.setColumnCount(4)
        self.categorieTable.setHorizontalHeaderLabels(["ID", "Nom", "Description", "Date création"])
        main_layout.addWidget(self.categorieTable)

        # Layout des boutons CRUD
        button_layout = QtWidgets.QHBoxLayout()

        self.addCategorieButton = QtWidgets.QPushButton("Ajouter une catégorie")
        self.addCategorieButton.clicked.connect(self.ajouter_categorie)
        button_layout.addWidget(self.addCategorieButton)

        self.editCategorieButton = QtWidgets.QPushButton("Modifier une catégorie")
        self.editCategorieButton.clicked.connect(self.modifier_categorie)
        button_layout.addWidget(self.editCategorieButton)

        self.deleteCategorieButton = QtWidgets.QPushButton("Supprimer une catégorie")
        self.deleteCategorieButton.clicked.connect(self.supprimer_categorie)
        button_layout.addWidget(self.deleteCategorieButton)

        self.addButton = QtWidgets.QPushButton("Ajouter")
        self.addButton.clicked.connect(self.ajouter_utilisateur)
        button_layout.addWidget(self.addButton)
        self.editButton = QtWidgets.QPushButton("Modifier")
        self.editButton.clicked.connect(self.modifier_utilisateur)
        button_layout.addWidget(self.editButton)
        self.deleteButton = QtWidgets.QPushButton("Supprimer")
        self.deleteButton.clicked.connect(self.supprimer_utilisateur)
        button_layout.addWidget(self.deleteButton)
        main_layout.addLayout(button_layout)

        self.load_users()
        self.load_categories()
        
    def load_categories(self):
        from db import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, description, "createdAt" FROM "Categorie"')
        rows = cur.fetchall()
        self.categorieTable.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.categorieTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
        cur.close()
        conn.close()

    def load_users(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, username, email, role FROM "User"')
        rows = cur.fetchall()
        self.tableWidget.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
        cur.close()
        conn.close()

    def on_start_clicked(self):
        print("Bouton 'Commencer gratuitement' cliqué!")
        
    def ajouter_categorie(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Ajouter une catégorie")
        layout = QtWidgets.QFormLayout(dialog)
        name = QtWidgets.QLineEdit()
        description = QtWidgets.QLineEdit()
        layout.addRow("Nom", name)
        layout.addRow("Description", description)
        btn = QtWidgets.QPushButton("Ajouter")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._insert_categorie(dialog, name.text(), description.text()))
        dialog.exec()
        
    def _insert_categorie(self, dialog, name, description):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO "Categorie" (name, description) VALUES (%s, %s)', (name, description))
        conn.commit()
        cur.close()
        conn.close()
        self.load_categories()
        dialog.accept()

    def ajouter_utilisateur(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Ajouter un utilisateur")
        layout = QtWidgets.QFormLayout(dialog)
        username = QtWidgets.QLineEdit()
        email = QtWidgets.QLineEdit()
        statut = QtWidgets.QLineEdit()
        password = QtWidgets.QLineEdit()
        layout.addRow("Nom d'utilisateur", username)
        layout.addRow("Email", email)
        layout.addRow("Statut", statut)
        layout.addRow("Mot de passe", password)
        btn = QtWidgets.QPushButton("Ajouter")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._insert_user(dialog, username.text(), email.text(), statut.text(), password.text()))
        dialog.exec()

    def _insert_user(self, dialog, username, email, statut, password):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, statut, password) VALUES (%s, %s, %s, %s)", (username, email, statut, password))
        conn.commit()
        cur.close()
        conn.close()
        self.load_users()
        dialog.accept()
        
    def modifier_categorie(self):
        row = self.categorieTable.currentRow()
        if row < 0:
            return
        id = self.categorieTable.item(row, 0).text()
        name = self.categorieTable.item(row, 1).text()
        description = self.categorieTable.item(row, 2).text()
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier catégorie")
        layout = QtWidgets.QFormLayout(dialog)
        name_edit = QtWidgets.QLineEdit(name)
        description_edit = QtWidgets.QLineEdit(description)
        layout.addRow("Nom", name_edit)
        layout.addRow("Description", description_edit)
        btn = QtWidgets.QPushButton("Modifier")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_categorie(dialog, id, name_edit.text(), description_edit.text()))
        dialog.exec()
    
    def _update_categorie(self, dialog, id, name, description):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('UPDATE "Categorie" SET name=%s, description=%s WHERE id=%s', (name, description, id))
        conn.commit()
        cur.close()
        conn.close()
        self.load_categories()
        dialog.accept()

    def modifier_utilisateur(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            return
        id = self.tableWidget.item(row, 0).text()
        username = self.tableWidget.item(row, 1).text()
        email = self.tableWidget.item(row, 2).text()
        statut = self.tableWidget.item(row, 3).text()
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier utilisateur")
        layout = QtWidgets.QFormLayout(dialog)
        username_edit = QtWidgets.QLineEdit(username)
        email_edit = QtWidgets.QLineEdit(email)
        statut_edit = QtWidgets.QLineEdit(statut)
        layout.addRow("Nom d'utilisateur", username_edit)
        layout.addRow("Email", email_edit)
        layout.addRow("Statut", statut_edit)
        btn = QtWidgets.QPushButton("Modifier")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_user(dialog, id, username_edit.text(), email_edit.text(), statut_edit.text()))
        dialog.exec()

    def _update_user(self, dialog, id, username, email, statut):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET username=%s, email=%s, statut=%s WHERE id=%s", (username, email, statut, id))
        conn.commit()
        cur.close()
        conn.close()
        self.load_users()
        dialog.accept()

    def supprimer_categorie(self):
        row = self.categorieTable.currentRow()
        if row < 0:
            return
        id = self.categorieTable.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(self, 'Confirmation', f'Supprimer la catégorie {id} ?', QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM "Categorie" WHERE id=%s', (id,))
            conn.commit()
            cur.close()
            conn.close()
            self.load_categories()
            
    
    def supprimer_utilisateur(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            return
        id = self.tableWidget.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(self, 'Confirmation', f'Supprimer l\'utilisateur {id} ?', QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id=%s", (id,))
            conn.commit()
            cur.close()
            conn.close()
            self.load_users()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Charger le style QSS après la création de l'application
    with open("styles/index.qss", "r") as f:
        app.setStyleSheet(f.read())

    login = LoginDialog()
    if login.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        window = NominaWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)
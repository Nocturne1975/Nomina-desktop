from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractScrollArea
import sys
from login import LoginDialog
from db import (
    get_all_users, get_all_categories, get_all_cultures, 
    insert_categorie, update_categorie, delete_categorie,
    insert_culture, update_culture, delete_culture,
    insert_user, update_user, delete_user
)

class NominaWindow(QtWidgets.QMainWindow):       
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/nomina_main.ui", self)
        self.setup_tables()
        self.setup_crud_buttons()
        self.load_data()

    def setup_tables(self):
        """Configurer les propriétés des tableaux."""
        self.all_tables = [
            self.categoriesTable,
            self.culturesTable,
            self.usersTable,
        ]

        for table in self.all_tables:
            table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(1))  # AlwaysOn
            table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy(2))    # AsNeeded
            header = table.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
            header.setStretchLastSection(False)

    def setup_crud_buttons(self):
        """Configurer les boutons CRUD pour chaque section."""
        # CRUD pour les catégories
        self.addCategoriesButton.clicked.connect(self.ajouter_categorie)
        self.editCategoriesButton.clicked.connect(self.modifier_categorie)
        self.deleteCategoriesButton.clicked.connect(self.supprimer_categorie)

        # CRUD pour cultures
        self.addCulturesButton.clicked.connect(self.ajouter_culture)
        self.editCulturesButton.clicked.connect(self.modifier_culture)
        self.deleteCulturesButton.clicked.connect(self.supprimer_culture)

        # CRUD pour utilisateurs
        self.addUserButton.clicked.connect(self.ajouter_user)
        self.editUserButton.clicked.connect(self.modifier_user)
        self.deleteUserButton.clicked.connect(self.supprimer_user)

    def load_data(self):
        """Charger toutes les données des tables dans l'interface."""
        self.load_categories()
        self.load_cultures()
        self.load_users()

    # CRUD pour Categorie
    def load_categories(self):
        print("Charger les données pour les catégories dans la table.")
        rows = get_all_categories()
        self.categoriesTable.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.categoriesTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def ajouter_categorie(self):
        """Ajouter une nouvelle catégorie."""
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
        """Insérer une catégorie dans la base de données."""
        insert_categorie(name, description)
        self.load_categories()
        dialog.accept()

    def modifier_categorie(self):
        """Modifier une catégorie existante."""
        row = self.categoriesTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez une catégorie à modifier.")
            return

        id_ = self.categoriesTable.item(row, 0).text()
        old_name = self.categoriesTable.item(row, 1).text()
        old_description = self.categoriesTable.item(row, 2).text()

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier catégorie")
        layout = QtWidgets.QFormLayout(dialog)

        name = QtWidgets.QLineEdit(old_name)
        description = QtWidgets.QLineEdit(old_description)
        layout.addRow("Nom", name)
        layout.addRow("Description", description)

        btn = QtWidgets.QPushButton("Modifier")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_categorie(dialog, id_, name.text(), description.text()))
        dialog.exec()

    def _update_categorie(self, dialog, id_, name, description):
        """Mettre à jour une catégorie dans la base de données."""
        update_categorie(id_, name, description)
        self.load_categories()
        dialog.accept()

    def supprimer_categorie(self):
        """Supprimer une catégorie par ID."""
        row = self.categoriesTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez une catégorie à supprimer.")
            return

        id_ = self.categoriesTable.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self, "Confirmation", f"Supprimer la catégorie {id_} ?", 
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            delete_categorie(id_)
            self.load_categories()

    # CRUD pour Culture
    def load_cultures(self):
        """Charger les cultures dans la table dédiée."""
        rows = get_all_cultures()
        self.culturesTable.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.culturesTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def ajouter_culture(self):
        """Ajouter une nouvelle culture."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Ajouter une culture")
        layout = QtWidgets.QFormLayout(dialog)

        name = QtWidgets.QLineEdit()
        description = QtWidgets.QLineEdit()
        layout.addRow("Nom", name)
        layout.addRow("Description", description)

        btn = QtWidgets.QPushButton("Ajouter")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._insert_culture(dialog, name.text(), description.text()))
        dialog.exec()

    def _insert_culture(self, dialog, name, description):
        """Insérer une culture."""
        insert_culture(name, description)
        self.load_cultures()
        dialog.accept()

    def modifier_culture(self):
        """Modifier une culture existante."""
        row = self.culturesTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez une culture à modifier.")
            return

        id_ = self.culturesTable.item(row, 0).text()
        old_name = self.culturesTable.item(row, 1).text()
        old_description = self.culturesTable.item(row, 2).text()

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier culture")
        layout = QtWidgets.QFormLayout(dialog)

        name = QtWidgets.QLineEdit(old_name)
        description = QtWidgets.QLineEdit(old_description)
        layout.addRow("Nom", name)
        layout.addRow("Description", description)

        btn = QtWidgets.QPushButton("Modifier")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_culture(dialog, id_, name.text(), description.text()))
        dialog.exec()

    def _update_culture(self, dialog, id_, name, description):
        """Mettre à jour une culture existante."""
        update_culture(id_, name, description)
        self.load_cultures()
        dialog.accept()

    def supprimer_culture(self):
        """Supprimer une culture."""
        row = self.culturesTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez une culture à supprimer.")
            return

        id_ = self.culturesTable.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self, "Confirmation", f"Supprimer la culture {id_} ?", 
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            delete_culture(id_)
            self.load_cultures()

    # CRUD pour Users
    def load_users(self):
        """Charger les utilisateurs dans la table dédiée."""
        rows = get_all_users()
        self.usersTable.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.usersTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def ajouter_user(self):
        """Ajouter un nouvel utilisateur via un formulaire."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Ajouter un utilisateur")
        layout = QtWidgets.QFormLayout(dialog)

        username = QtWidgets.QLineEdit()
        password = QtWidgets.QLineEdit()
        email = QtWidgets.QLineEdit()
        role = QtWidgets.QLineEdit()
        is_active = QtWidgets.QLineEdit()

        layout.addRow("Nom d'utilisateur :", username)
        layout.addRow("Mot de passe :", password)
        layout.addRow("Email :", email)
        layout.addRow("Rôle :", role)
        layout.addRow("Actif (true/false) :", is_active)

        btn = QtWidgets.QPushButton("Ajouter")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._insert_user(dialog, username.text(), password.text(), email.text(), role.text(), is_active.text()))
        dialog.exec()

    def _insert_user(self, dialog, username, password, email, role, is_active):
        """Insérer un utilisateur."""
        is_active_bool = True if is_active.lower() == "true" else False
        insert_user(username, password, email, role, is_active_bool)
        self.load_users()
        dialog.accept()

    def modifier_user(self):
        """Modifier un utilisateur existant."""
        row = self.usersTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un utilisateur à modifier.")
            return

        id_ = self.usersTable.item(row, 0).text()
        old_username = self.usersTable.item(row, 1).text()
        old_email = self.usersTable.item(row, 2).text()
        old_role = self.usersTable.item(row, 3).text()
        old_is_active = self.usersTable.item(row, 4).text()

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier utilisateur")
        layout = QtWidgets.QFormLayout(dialog)

        username = QtWidgets.QLineEdit(old_username)
        email = QtWidgets.QLineEdit(old_email)
        role = QtWidgets.QLineEdit(old_role)
        is_active = QtWidgets.QLineEdit(old_is_active)

        layout.addRow("Nom d'utilisateur :", username)
        layout.addRow("Email :", email)
        layout.addRow("Rôle :", role)
        layout.addRow("Actif (true/false) :", is_active)

        btn = QtWidgets.QPushButton("Modifier")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_user(dialog, id_, username.text(), email.text(), role.text(), is_active.text()))
        dialog.exec()

    def _update_user(self, dialog, id_, username, email, role, is_active):
        """Mettre à jour un utilisateur en base."""
        is_active_bool = True if is_active.lower() == "true" else False
        update_user(int(id_), username=username, email=email, role=role, isActive=is_active_bool)
        self.load_users()
        dialog.accept()

    def supprimer_user(self):
        """Supprimer un utilisateur existant."""
        row = self.usersTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un utilisateur à supprimer.")
            return

        id_ = self.usersTable.item(row, 0).text()

        reply = QtWidgets.QMessageBox.question(
            self, "Confirmation", f"Supprimer l'utilisateur {id_} ?", 
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            delete_user(int(id_))
            self.load_users()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    try:
        with open("styles/index.qss", "r") as f:
              app.setStyleSheet(f.read())        
    except FileNotFoundError:
        print("Style non appliqué. Fichier index.qss introuvable.")

    login = LoginDialog()
    if login.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        main_window = NominaWindow()
        main_window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)
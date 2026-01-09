from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractScrollArea
import sys
from login import LoginDialog
from db import (
    delete_concept, delete_fragment, delete_lieu, delete_titre, get_all_concepts, get_all_fragments, get_all_lieux, get_all_titres, get_all_users, get_all_categories, get_all_cultures, 
    insert_categorie, insert_concept, insert_fragment, insert_lieu, insert_titre, update_categorie, delete_categorie,
    insert_culture, update_concept, update_culture, delete_culture,
    insert_user, update_fragment, update_lieu, update_titre, update_user, delete_user
)

class NominaWindow(QtWidgets.QMainWindow):       
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/nomina_main.ui", self)
        self.setup_tables()
        self.setup_crud_buttons()
        self.setup_titres_buttons()
        self.setup_fragments_buttons()
        self.setup_concepts_buttons()
        self.setup_lieux_buttons()
        self.load_data()
        self.stackedWidget.setCurrentIndex(0)

    def setup_tables(self):
        """Configurer les propriétés des tableaux."""
        self.all_tables = [
            self.categoriesTable,
            self.culturesTable,
            self.usersTable,
            self.titresTable,
            self.fragmentsTable,
            self.conceptsTable,
            self.lieuxTable,
        ]
    def setup_fragments_buttons(self):
        self.addFragmentsButton.clicked.connect(self.ajouter_fragment)
        self.editFragmentsButton.clicked.connect(self.modifier_fragment)
        self.deleteFragmentsButton.clicked.connect(self.supprimer_fragment)
        self.fragmentsTable.cellDoubleClicked.connect(self.modifier_fragment)

    def setup_concepts_buttons(self):
        self.addConceptsButton.clicked.connect(self.ajouter_concept)
        self.editConceptsButton.clicked.connect(self.modifier_concept)
        self.deleteConceptsButton.clicked.connect(self.supprimer_concept)
        self.conceptsTable.cellDoubleClicked.connect(self.modifier_concept)

    def setup_lieux_buttons(self):
        self.addLieuxButton.clicked.connect(self.ajouter_lieu)
        self.editLieuxButton.clicked.connect(self.modifier_lieu)
        self.deleteLieuxButton.clicked.connect(self.supprimer_lieu)
        self.lieuxTable.cellDoubleClicked.connect(self.modifier_lieu)

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

    def setup_titres_buttons(self):
        """Connecter les boutons CRUD pour Titres."""
        self.addTitresButton.clicked.connect(self.ajouter_titre)
        self.editTitresButton.clicked.connect(self.modifier_titre)
        self.deleteTitresButton.clicked.connect(self.supprimer_titre)
        self.titresTable.cellDoubleClicked.connect(self.modifier_titre)
        
    def load_data(self):
        """Charger toutes les données des tables dans l'interface."""
        self.load_categories()
        self.load_cultures()
        self.load_users()
        self.load_titres()
        self.load_fragments()
        self.load_concepts()
        self.load_lieux()
        
        # CRUD pour Fragments
    def load_fragments(self):
        rows = get_all_fragments()
        self.fragmentsTable.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.fragmentsTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
    def ajouter_fragment(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Ajouter un fragment")
        layout = QtWidgets.QFormLayout(dialog)
        texte = QtWidgets.QLineEdit()
        applies_to = QtWidgets.QLineEdit()
        genre = QtWidgets.QLineEdit()
        min_name_length = QtWidgets.QLineEdit()
        max_name_length = QtWidgets.QLineEdit()
        culture_id = QtWidgets.QLineEdit()
        categorie_id = QtWidgets.QLineEdit()
        layout.addRow("Texte", texte)
        layout.addRow("Applies To", applies_to)
        layout.addRow("Genre", genre)
        layout.addRow("Min Name Length", min_name_length)
        layout.addRow("Max Name Length", max_name_length)
        layout.addRow("Culture ID", culture_id)
        layout.addRow("Catégorie ID", categorie_id)
        btn = QtWidgets.QPushButton("Ajouter")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._insert_fragment(dialog, texte.text(), applies_to.text(), genre.text(), min_name_length.text(), max_name_length.text(), culture_id.text(), categorie_id.text()))
        dialog.exec()

    def _insert_fragment(self, dialog, texte, applies_to, genre, min_name_length, max_name_length, culture_id, categorie_id):
        insert_fragment(texte, applies_to, genre, min_name_length, max_name_length, culture_id, categorie_id)
        self.load_fragments()
        dialog.accept()

    def modifier_fragment(self):
        row = self.fragmentsTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un fragment à modifier.")
            return
        id_ = self.fragmentsTable.item(row, 0).text()
        old_texte = self.fragmentsTable.item(row, 1).text()
        old_applies_to = self.fragmentsTable.item(row, 2).text()
        old_genre = self.fragmentsTable.item(row, 3).text()
        old_min_name_length = self.fragmentsTable.item(row, 4).text()
        old_max_name_length = self.fragmentsTable.item(row, 5).text()
        old_culture_id = self.fragmentsTable.item(row, 6).text()
        old_categorie_id = self.fragmentsTable.item(row, 8).text()
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier fragment")
        layout = QtWidgets.QFormLayout(dialog)
        texte = QtWidgets.QLineEdit(old_texte)
        applies_to = QtWidgets.QLineEdit(old_applies_to)
        genre = QtWidgets.QLineEdit(old_genre)
        min_name_length = QtWidgets.QLineEdit(old_min_name_length)
        max_name_length = QtWidgets.QLineEdit(old_max_name_length)
        culture_id = QtWidgets.QLineEdit(old_culture_id)
        categorie_id = QtWidgets.QLineEdit(old_categorie_id)
        layout.addRow("Texte", texte)
        layout.addRow("Applies To", applies_to)
        layout.addRow("Genre", genre)
        layout.addRow("Min Name Length", min_name_length)
        layout.addRow("Max Name Length", max_name_length)
        layout.addRow("Culture ID", culture_id)
        layout.addRow("Catégorie ID", categorie_id)
        btn = QtWidgets.QPushButton("Modifier")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_fragment(dialog, id_, texte.text(), applies_to.text(), genre.text(), min_name_length.text(), max_name_length.text(), culture_id.text(), categorie_id.text()))
        dialog.exec()

    def _update_fragment(self, dialog, id_, texte, applies_to, genre, min_name_length, max_name_length, culture_id, categorie_id):
        update_fragment(id_, texte, applies_to, genre, min_name_length, max_name_length, culture_id, categorie_id)
        self.load_fragments()
        dialog.accept()

    def supprimer_fragment(self):
        row = self.fragmentsTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un fragment à supprimer.")
            return
        id_ = self.fragmentsTable.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self, "Confirmation", f"Supprimer le fragment {id_} ?", 
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            delete_fragment(id_)
            self.load_fragments()

            # CRUD pour Concepts
    def load_concepts(self):
        rows = get_all_concepts()
        self.conceptsTable.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.conceptsTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
                
    def ajouter_concept(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Ajouter un concept")
        layout = QtWidgets.QFormLayout(dialog)
        valeur = QtWidgets.QLineEdit()
        type_field = QtWidgets.QLineEdit()
        mood = QtWidgets.QLineEdit()
        keywords = QtWidgets.QLineEdit()
        categorie_id = QtWidgets.QLineEdit()
        layout.addRow("Valeur", valeur)
        layout.addRow("Type", type_field)
        layout.addRow("Mood", mood)
        layout.addRow("Keywords", keywords)
        layout.addRow("Catégorie ID", categorie_id)
        btn = QtWidgets.QPushButton("Ajouter")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._insert_concept(dialog, valeur.text(), type_field.text(), mood.text(), keywords.text(), categorie_id.text()))
        dialog.exec()

    def _insert_concept(self, dialog, valeur, type_field, mood, keywords, categorie_id):
        insert_concept(valeur, type_field, mood, keywords, categorie_id)
        self.load_concepts()
        dialog.accept()

    def modifier_concept(self):
        row = self.conceptsTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un concept à modifier.")
            return
        id_ = self.conceptsTable.item(row, 0).text()
        old_valeur = self.conceptsTable.item(row, 1).text()
        old_type = self.conceptsTable.item(row, 2).text()
        old_mood = self.conceptsTable.item(row, 3).text()
        old_keywords = self.conceptsTable.item(row, 4).text()
        old_categorie_id = self.conceptsTable.item(row, 5).text()
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier concept")
        layout = QtWidgets.QFormLayout(dialog)
        valeur = QtWidgets.QLineEdit(old_valeur)
        type_field = QtWidgets.QLineEdit(old_type)
        mood = QtWidgets.QLineEdit(old_mood)
        keywords = QtWidgets.QLineEdit(old_keywords)
        categorie_id = QtWidgets.QLineEdit(old_categorie_id)
        layout.addRow("Valeur", valeur)
        layout.addRow("Type", type_field)
        layout.addRow("Mood", mood)
        layout.addRow("Keywords", keywords)
        layout.addRow("Catégorie ID", categorie_id)
        btn = QtWidgets.QPushButton("Modifier")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_concept(dialog, id_, valeur.text(), type_field.text(), mood.text(), keywords.text(), categorie_id.text()))
        dialog.exec()
        
    def _update_concept(self, dialog, id_, valeur, type_field, mood, keywords, categorie_id):
        update_concept(id_, valeur, type_field, mood, keywords, categorie_id)
        self.load_concepts()
        dialog.accept()
        
    def supprimer_concept(self):
        row = self.conceptsTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un concept à supprimer.")
            return
        id_ = self.conceptsTable.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self, "Confirmation", f"Supprimer le concept {id_} ?", 
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            delete_concept(id_)
            self.load_concepts()

        # CRUD pour Lieux
    def load_lieux(self):
        rows = get_all_lieux()
        self.lieuxTable.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.lieuxTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
                
    def ajouter_lieu(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Ajouter un lieu")
        layout = QtWidgets.QFormLayout(dialog)
        value = QtWidgets.QLineEdit()
        type_field = QtWidgets.QLineEdit()
        categorie_id = QtWidgets.QLineEdit()
        layout.addRow("Value", value)
        layout.addRow("Type", type_field)
        layout.addRow("Catégorie ID", categorie_id)
        btn = QtWidgets.QPushButton("Ajouter")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._insert_lieu(dialog, value.text(), type_field.text(), categorie_id.text()))
        dialog.exec()

    def _insert_lieu(self, dialog, value, type_field, categorie_id):
        insert_lieu(value, type_field, categorie_id)
        self.load_lieux()
        dialog.accept()

    def modifier_lieu(self):
        row = self.lieuxTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un lieu à modifier.")
            return
        id_ = self.lieuxTable.item(row, 0).text()
        old_value = self.lieuxTable.item(row, 1).text()
        old_type = self.lieuxTable.item(row, 2).text()
        old_categorie_id = self.lieuxTable.item(row, 3).text()
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier lieu")
        layout = QtWidgets.QFormLayout(dialog)
        value = QtWidgets.QLineEdit(old_value)
        type_field = QtWidgets.QLineEdit(old_type)
        categorie_id = QtWidgets.QLineEdit(old_categorie_id)
        layout.addRow("Value", value)
        layout.addRow("Type", type_field)
        layout.addRow("Catégorie ID", categorie_id)
        btn = QtWidgets.QPushButton("Modifier")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_lieu(dialog, id_, value.text(), type_field.text(), categorie_id.text()))
        dialog.exec()

    def _update_lieu(self, dialog, id_, value, type_field, categorie_id):
        update_lieu(id_, value, type_field, categorie_id)
        self.load_lieux()
        dialog.accept()

    def supprimer_lieu(self):
        row = self.lieuxTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un lieu à supprimer.")
            return
        id_ = self.lieuxTable.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self, "Confirmation", f"Supprimer le lieu {id_} ?", 
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            delete_lieu(id_)
            self.load_lieux()
        
    # CRUD pour Titres
    def load_titres(self):
        """Charger les titres dans la table dédiée."""
        rows = get_all_titres()
        self.titresTable.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.titresTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def ajouter_titre(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Ajouter un titre")
        layout = QtWidgets.QFormLayout(dialog)

        valeur = QtWidgets.QLineEdit()
        type_field = QtWidgets.QLineEdit()
        genre = QtWidgets.QLineEdit()
        culture_id = QtWidgets.QLineEdit()
        categorie_id = QtWidgets.QLineEdit()
        layout.addRow("Valeur", valeur)
        layout.addRow("Type", type_field)
        layout.addRow("Genre", genre)
        layout.addRow("Culture ID", culture_id)
        layout.addRow("Catégorie ID", categorie_id)

        btn = QtWidgets.QPushButton("Ajouter")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._insert_titre(dialog, valeur.text(), type_field.text(), genre.text(), culture_id.text(), categorie_id.text()))
        dialog.exec()

    def _insert_titre(self, dialog, valeur, type_field, genre, culture_id, categorie_id):
        insert_titre(valeur, type_field, genre, culture_id, categorie_id)
        self.load_titres()
        dialog.accept()

    def modifier_titre(self):
        row = self.titresTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un titre à modifier.")
            return

        id_ = self.titresTable.item(row, 0).text()
        old_valeur = self.titresTable.item(row, 1).text()
        old_type = self.titresTable.item(row, 2).text()
        old_genre = self.titresTable.item(row, 3).text()
        old_culture_id = self.titresTable.item(row, 4).text()
        old_categorie_id = self.titresTable.item(row, 6).text()

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier titre")
        layout = QtWidgets.QFormLayout(dialog)

        valeur = QtWidgets.QLineEdit(old_valeur)
        type_field = QtWidgets.QLineEdit(old_type)
        genre = QtWidgets.QLineEdit(old_genre)
        culture_id = QtWidgets.QLineEdit(old_culture_id)
        categorie_id = QtWidgets.QLineEdit(old_categorie_id)
        layout.addRow("Valeur", valeur)
        layout.addRow("Type", type_field)
        layout.addRow("Genre", genre)
        layout.addRow("Culture ID", culture_id)
        layout.addRow("Catégorie ID", categorie_id)

        btn = QtWidgets.QPushButton("Modifier")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_titre(dialog, id_, valeur.text(), type_field.text(), genre.text(), culture_id.text(), categorie_id.text()))
        dialog.exec()

    def _update_titre(self, dialog, id_, valeur, type_field, genre, culture_id, categorie_id):
        update_titre(id_, valeur, type_field, genre, culture_id, categorie_id)
        self.load_titres()
        dialog.accept()

    def supprimer_titre(self):
        row = self.titresTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un titre à supprimer.")
            return

        id_ = self.titresTable.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self, "Confirmation", f"Supprimer le titre {id_} ?", 
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            delete_titre(id_)
            self.load_titres()

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
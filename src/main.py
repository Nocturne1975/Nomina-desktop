from PyQt6 import QtWidgets, uic
import sys
import os
from login import LoginDialog
from db import (
    get_connection,
    get_all_cultures, get_all_categories, get_all_lieux, get_all_fragments,
    get_all_titres, get_all_concepts,
    insert_culture, update_culture, delete_culture,
    insert_categorie, update_categorie, delete_categorie,
    insert_lieu, update_lieu, delete_lieu,
    insert_fragment, update_fragment, delete_fragment,
    insert_titre, update_titre, delete_titre,
    insert_concept, update_concept, delete_concept
)

class NominaWindow(QtWidgets.QMainWindow):
    def modifier_fragment(self):
        from db import update_fragment, get_all_cultures, get_all_categories
        row = self.fragmentsTable.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un fragment à modifier.")
            return
        fragment_id = self.fragmentsTable.item(row, 0).text()
        old_texte = self.fragmentsTable.item(row, 1).text()
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier un fragment d'histoire")
        layout = QtWidgets.QFormLayout(dialog)
        texte = QtWidgets.QLineEdit(old_texte)
        # Ajouter ici les autres champs si besoin (appliesTo, genre, etc.)
        layout.addRow("Texte", texte)
        btn = QtWidgets.QPushButton("Enregistrer")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: self._update_fragment(dialog, fragment_id, texte.text()))
        dialog.exec()
        def _update_fragment(self, dialog, fragment_id, texte):
            from db import update_fragment
            update_fragment(fragment_id, texte)
            self.load_fragments()
            dialog.accept()
            
    def load_concepts(self):
        from db import get_all_concepts
        self.conceptsTable.setRowCount(0)
        self.conceptsTable.setColumnCount(9)
        self.conceptsTable.setHorizontalHeaderLabels([
            "ID", "Valeur", "Type", "Mood", "Keywords", "Catégorie ID", "Catégorie", "Créé le", "Modifié le"
        ])
        concepts = get_all_concepts()
        for row_idx, concept in enumerate(concepts):
            self.conceptsTable.insertRow(row_idx)
            for col_idx, value in enumerate(concept):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.conceptsTable.setItem(row_idx, col_idx, item)
                
    def ajouter_lieu(self):
            from db import get_all_categories, insert_lieu
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Ajouter un lieu")
            layout = QtWidgets.QFormLayout(dialog)
            value = QtWidgets.QLineEdit()
            type_field = QtWidgets.QLineEdit()
            categorie_combo = QtWidgets.QComboBox()
            categories = get_all_categories()
            categorie_combo.addItem("Aucune", None)
            for cat in categories:
                categorie_combo.addItem(cat[1], cat[0])
            layout.addRow("Nom du lieu", value)
            layout.addRow("Type", type_field)
            layout.addRow("Catégorie", categorie_combo)
            btn = QtWidgets.QPushButton("Ajouter")
            layout.addWidget(btn)
            btn.clicked.connect(lambda: self._insert_lieu(dialog, value.text(), type_field.text(), categorie_combo.currentData()))
            dialog.exec()

    def _insert_lieu(self, dialog, value, type_field, categorie_id):
            from db import insert_lieu
            insert_lieu(value, type_field, categorie_id)
            self.load_lieux()
            dialog.accept()

    def modifier_lieu(self):
            from db import get_all_categories, update_lieu
            row = self.lieuxTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un lieu à modifier.")
                return
            lieu_id = self.lieuxTable.item(row, 0).text()
            old_value = self.lieuxTable.item(row, 1).text()
            old_type = self.lieuxTable.item(row, 2).text()
            old_categorie_id = self.lieuxTable.item(row, 3).text()
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Modifier un lieu")
            layout = QtWidgets.QFormLayout(dialog)
            value = QtWidgets.QLineEdit(old_value)
            type_field = QtWidgets.QLineEdit(old_type)
            categorie_combo = QtWidgets.QComboBox()
            categories = get_all_categories()
            categorie_combo.addItem("Aucune", None)
            for cat in categories:
                categorie_combo.addItem(cat[1], cat[0])
                if str(cat[0]) == old_categorie_id:
                    categorie_combo.setCurrentIndex(categorie_combo.count() - 1)
            layout.addRow("Nom du lieu", value)
            layout.addRow("Type", type_field)
            layout.addRow("Catégorie", categorie_combo)
            btn = QtWidgets.QPushButton("Enregistrer")
            layout.addWidget(btn)
            btn.clicked.connect(lambda: self._update_lieu(dialog, lieu_id, value.text(), type_field.text(), categorie_combo.currentData()))
            dialog.exec()

    def _update_lieu(self, dialog, lieu_id, value, type_field, categorie_id):
            from db import update_lieu
            update_lieu(lieu_id, value, type_field, categorie_id)
            self.load_lieux()
            dialog.accept()

    def supprimer_lieu(self):
            from db import delete_lieu
            row = self.lieuxTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un lieu à supprimer.")
                return
            lieu_id = self.lieuxTable.item(row, 0).text()
            reply = QtWidgets.QMessageBox.question(self, "Confirmer", "Supprimer ce lieu ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                delete_lieu(lieu_id)
                self.load_lieux()
                
    def ajouter_fragment(self):
            from db import insert_fragment
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Ajouter un fragment d'histoire")
            layout = QtWidgets.QFormLayout(dialog)
            texte = QtWidgets.QLineEdit()
            btn = QtWidgets.QPushButton("Ajouter")
            layout.addRow("Texte", texte)
            layout.addWidget(btn)
            btn.clicked.connect(lambda: self._insert_fragment(dialog, texte.text()))
            dialog.exec()

    def _insert_fragment(self, dialog, texte):
            from db import insert_fragment
            insert_fragment(texte)
            self.load_fragments()
            dialog.accept()
        
    def supprimer_fragment(self):
            from db import delete_fragment
            row = self.fragmentsTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un fragment à supprimer.")
                return
            fragment_id = self.fragmentsTable.item(row, 0).text()
            reply = QtWidgets.QMessageBox.question(self, "Confirmer", "Supprimer ce fragment ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                delete_fragment(fragment_id)
                self.load_fragments()

    def ajouter_concept(self):
            from db import get_all_categories, insert_concept
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Ajouter un concept")
            layout = QtWidgets.QFormLayout(dialog)
            valeur = QtWidgets.QLineEdit()
            type_field = QtWidgets.QLineEdit()
            mood = QtWidgets.QLineEdit()
            keywords = QtWidgets.QLineEdit()
            categorie_combo = QtWidgets.QComboBox()
            categorie_combo.addItem("Aucune", None)
            for cat in get_all_categories():
                categorie_combo.addItem(cat[1], cat[0])
            layout.addRow("Valeur", valeur)
            layout.addRow("Type", type_field)
            layout.addRow("Mood", mood)
            layout.addRow("Mots-clés", keywords)
            layout.addRow("Catégorie", categorie_combo)
            btn = QtWidgets.QPushButton("Ajouter")
            layout.addWidget(btn)
            btn.clicked.connect(lambda: self._insert_concept(
                dialog, valeur.text(), type_field.text(), mood.text(), keywords.text(),
                categorie_combo.currentData()
            ))
            dialog.exec()

    def _insert_concept(self, dialog, valeur, type_field, mood, keywords, categorie_id):
            from db import insert_concept
            insert_concept(valeur, type_field, mood, keywords, categorie_id)
            self.load_concepts()
            dialog.accept()

    def modifier_concept(self):
            from db import get_all_categories, update_concept
            row = self.conceptsTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un concept à modifier.")
                return
            concept_id = self.conceptsTable.item(row, 0).text()
            old_valeur = self.conceptsTable.item(row, 1).text()
            old_type = self.conceptsTable.item(row, 2).text()
            old_mood = self.conceptsTable.item(row, 3).text()
            old_keywords = self.conceptsTable.item(row, 4).text()
            old_categorie_id = self.conceptsTable.item(row, 5).text()
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Modifier un concept")
            layout = QtWidgets.QFormLayout(dialog)
            valeur = QtWidgets.QLineEdit(old_valeur)
            type_field = QtWidgets.QLineEdit(old_type)
            mood = QtWidgets.QLineEdit(old_mood)
            keywords = QtWidgets.QLineEdit(old_keywords)
            categorie_combo = QtWidgets.QComboBox()
            categorie_combo.addItem("Aucune", None)
            for cat in get_all_categories():
                categorie_combo.addItem(cat[1], cat[0])
                if str(cat[0]) == old_categorie_id:
                    categorie_combo.setCurrentIndex(categorie_combo.count() - 1)
            layout.addRow("Valeur", valeur)
            layout.addRow("Type", type_field)
            layout.addRow("Mood", mood)
            layout.addRow("Mots-clés", keywords)
            layout.addRow("Catégorie", categorie_combo)
            btn = QtWidgets.QPushButton("Enregistrer")
            layout.addWidget(btn)
            btn.clicked.connect(lambda: self._update_concept(
                dialog, concept_id, valeur.text(), type_field.text(), mood.text(), keywords.text(),
                categorie_combo.currentData()
            ))
            dialog.exec()

    def _update_concept(self, dialog, concept_id, valeur, type_field, mood, keywords, categorie_id):
            from db import update_concept
            update_concept(concept_id, valeur, type_field, mood, keywords, categorie_id)
            self.load_concepts()
            dialog.accept()

    def supprimer_concept(self):
            from db import delete_concept
            row = self.conceptsTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un concept à supprimer.")
                return
            concept_id = self.conceptsTable.item(row, 0).text()
            reply = QtWidgets.QMessageBox.question(self, "Confirmer", "Supprimer ce concept ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                delete_concept(concept_id)
                self.load_concepts()

    def load_lieux(self):
            from db import get_all_lieux
            rows = get_all_lieux()
            self.lieuxTable.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.lieuxTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

                # Layout principal
                central_widget = QtWidgets.QWidget()
                self.setCentralWidget(central_widget)
                main_layout = QtWidgets.QVBoxLayout(central_widget)

                # Tableau des titres
                self.titresTable = QtWidgets.QTableWidget()
                self.titresTable.setColumnCount(10)
                self.titresTable.setHorizontalHeaderLabels([
                    "ID", "Valeur", "Type", "Genre", "Culture (ID)", "Culture (Nom)", "Catégorie (ID)", "Catégorie (Nom)", "Créé", "Modifié"
                ])
                main_layout.addWidget(self.titresTable)

                # Tableau des concepts
                self.conceptsTable = QtWidgets.QTableWidget()
                self.conceptsTable.setColumnCount(9)
                self.conceptsTable.setHorizontalHeaderLabels([
                    "ID", "Valeur", "Type", "Mood", "Keywords", "Catégorie (ID)", "Catégorie (Nom)", "Créé", "Modifié"
                ])
                main_layout.addWidget(self.conceptsTable)

                # Tableau des fragments d'histoire
                self.fragmentsTable = QtWidgets.QTableWidget()
                self.fragmentsTable.setColumnCount(10)
                self.fragmentsTable.setHorizontalHeaderLabels([
                    "ID", "Texte", "AppliesTo", "Genre", "MinLen", "MaxLen",
                    "Culture (ID)", "Culture (Nom)", "Catégorie (ID)", "Catégorie (Nom)"
                ])
                main_layout.addWidget(self.fragmentsTable)

                # Tableau des utilisateurs
                self.tableWidget = QtWidgets.QTableWidget()
                self.tableWidget.setHorizontalHeaderLabels(["ID", "Nom d'utilisateur", "Email", "Rôle"])
                main_layout.addWidget(self.tableWidget)

                # Tableau des catégories
                self.categorieTable = QtWidgets.QTableWidget()
                self.categorieTable.setHorizontalHeaderLabels(["ID", "Nom", "Description", "Date création"])
                main_layout.addWidget(self.categorieTable)

                # Tableau des cultures
                self.cultureTable = QtWidgets.QTableWidget()
                self.cultureTable.setColumnCount(3)
                self.cultureTable.setHorizontalHeaderLabels(["ID", "Nom", "Description"])
                main_layout.addWidget(self.cultureTable)

                # Tableau des lieux
                self.lieuxTable = QtWidgets.QTableWidget()
                self.lieuxTable.setColumnCount(5)
                self.lieuxTable.setHorizontalHeaderLabels(["ID", "Nom du lieu", "Type", "Catégorie (ID)", "Catégorie (Nom)"])
                main_layout.addWidget(self.lieuxTable)

                # Layout des boutons CRUD
                button_layout = QtWidgets.QHBoxLayout()

                # Boutons CRUD pour Titre
                self.addTitreButton = QtWidgets.QPushButton("Ajouter un titre")
                self.addTitreButton.clicked.connect(self.ajouter_titre)
                button_layout.addWidget(self.addTitreButton)

                self.editTitreButton = QtWidgets.QPushButton("Modifier un titre")
                self.editTitreButton.clicked.connect(self.modifier_titre)
                button_layout.addWidget(self.editTitreButton)

                self.deleteTitreButton = QtWidgets.QPushButton("Supprimer un titre")
                self.deleteTitreButton.clicked.connect(self.supprimer_titre)
                button_layout.addWidget(self.deleteTitreButton)

                # Boutons CRUD pour Concept
                self.addConceptButton = QtWidgets.QPushButton("Ajouter un concept")
                self.addConceptButton.clicked.connect(self.ajouter_concept)
                button_layout.addWidget(self.addConceptButton)

                self.editConceptButton = QtWidgets.QPushButton("Modifier un concept")
                self.editConceptButton.clicked.connect(self.modifier_concept)
                button_layout.addWidget(self.editConceptButton)

                self.deleteConceptButton = QtWidgets.QPushButton("Supprimer un concept")
                self.deleteConceptButton.clicked.connect(self.supprimer_concept)
                button_layout.addWidget(self.deleteConceptButton)

                # Boutons CRUD pour FragmentsHistoire
                self.ajouterFragmentButton = QtWidgets.QPushButton("Ajouter un fragment")
                self.ajouterFragmentButton.clicked.connect(self.ajouter_fragment)
                button_layout.addWidget(self.ajouterFragmentButton)

                self.editFragmentButton = QtWidgets.QPushButton("Modifier un fragment")
                self.editFragmentButton.clicked.connect(self.modifier_fragment)
                button_layout.addWidget(self.editFragmentButton)

                self.deleteFragmentButton = QtWidgets.QPushButton("Supprimer un fragment")
                self.deleteFragmentButton.clicked.connect(self.supprimer_fragment)
                button_layout.addWidget(self.deleteFragmentButton)

                # Boutons CRUD pour Catégorie
                self.addCategorieButton = QtWidgets.QPushButton("Ajouter une catégorie")
                self.addCategorieButton.clicked.connect(self.ajouter_categorie)
                button_layout.addWidget(self.addCategorieButton)

                self.editCategorieButton = QtWidgets.QPushButton("Modifier une catégorie")
                self.editCategorieButton.clicked.connect(self.modifier_categorie)
                button_layout.addWidget(self.editCategorieButton)

                self.deleteCategorieButton = QtWidgets.QPushButton("Supprimer une catégorie")
                self.deleteCategorieButton.clicked.connect(self.supprimer_categorie)
                button_layout.addWidget(self.deleteCategorieButton)

                # Boutons CRUD pour Utilisateur
                self.addButton = QtWidgets.QPushButton("Ajouter un utilisateur")
                self.addButton.clicked.connect(self.ajouter_utilisateur)
                button_layout.addWidget(self.addButton)

                self.editButton = QtWidgets.QPushButton("Modifier un utilisateur")
                self.editButton.clicked.connect(self.modifier_utilisateur)
                button_layout.addWidget(self.editButton)

                self.deleteButton = QtWidgets.QPushButton("Supprimer un utilisateur")
                self.deleteButton.clicked.connect(self.supprimer_utilisateur)
                button_layout.addWidget(self.deleteButton)

                # Boutons CRUD pour Culture
                self.addCultureButton = QtWidgets.QPushButton("Ajouter une culture")
                self.addCultureButton.clicked.connect(self.ajouter_culture)
                button_layout.addWidget(self.addCultureButton)

                self.editCultureButton = QtWidgets.QPushButton("Modifier une culture")
                self.editCultureButton.clicked.connect(self.modifier_culture)
                button_layout.addWidget(self.editCultureButton)

                self.deleteCultureButton = QtWidgets.QPushButton("Supprimer une culture")
                self.deleteCultureButton.clicked.connect(self.supprimer_culture)
                button_layout.addWidget(self.deleteCultureButton)

                # Boutons CRUD pour Lieux
                self.addLieuxButton = QtWidgets.QPushButton("Ajouter un lieu")
                self.addLieuxButton.clicked.connect(self.ajouter_lieu)
                button_layout.addWidget(self.addLieuxButton)

                self.editLieuxButton = QtWidgets.QPushButton("Modifier un lieu")
                self.editLieuxButton.clicked.connect(self.modifier_lieu)
                button_layout.addWidget(self.editLieuxButton)

                self.deleteLieuxButton = QtWidgets.QPushButton("Supprimer un lieu")
                self.deleteLieuxButton.clicked.connect(self.supprimer_lieu)
                button_layout.addWidget(self.deleteLieuxButton)

                main_layout.addLayout(button_layout)

                self.load_users()
                self.load_categories()
                self.load_cultures()
                self.load_fragments()
                self.load_titres()
                self.load_concepts()

    def load_categories(self):
               
                return

    def load_titres(self):
            from db import get_all_titres
            rows = get_all_titres()
            self.titresTable.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.titresTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def ajouter_titre(self):
            from db import get_all_cultures, get_all_categories, insert_titre
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Ajouter un titre")
            layout = QtWidgets.QFormLayout(dialog)
            valeur = QtWidgets.QLineEdit()
            type_field = QtWidgets.QLineEdit()
            genre = QtWidgets.QLineEdit()
            culture_combo = QtWidgets.QComboBox()
            categorie_combo = QtWidgets.QComboBox()
            culture_combo.addItem("Aucune", None)
            for c in get_all_cultures():
                culture_combo.addItem(c[1], c[0])
            categorie_combo.addItem("Aucune", None)
            for cat in get_all_categories():
                categorie_combo.addItem(cat[1], cat[0])
            layout.addRow("Valeur", valeur)
            layout.addRow("Type", type_field)
            layout.addRow("Genre", genre)
            layout.addRow("Culture", culture_combo)
            layout.addRow("Catégorie", categorie_combo)
            btn = QtWidgets.QPushButton("Ajouter")
            layout.addWidget(btn)
            btn.clicked.connect(lambda: self._insert_titre(
                dialog, valeur.text(), type_field.text(), genre.text(),
                culture_combo.currentData(), categorie_combo.currentData()
            ))
            dialog.exec()

    def _insert_titre(self, dialog, valeur, type_field, genre, culture_id, categorie_id):
            from db import insert_titre
            insert_titre(valeur, type_field, genre, culture_id, categorie_id)
            self.load_titres()
            dialog.accept()

    def modifier_titre(self):
            from db import get_all_cultures, get_all_categories, update_titre
            row = self.titresTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un titre à modifier.")
                return
            titre_id = self.titresTable.item(row, 0).text()
            old_valeur = self.titresTable.item(row, 1).text()
            old_type = self.titresTable.item(row, 2).text()
            old_genre = self.titresTable.item(row, 3).text()
            old_culture_id = self.titresTable.item(row, 4).text()
            old_categorie_id = self.titresTable.item(row, 6).text()
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Modifier un titre")
            layout = QtWidgets.QFormLayout(dialog)
            valeur = QtWidgets.QLineEdit(old_valeur)
            type_field = QtWidgets.QLineEdit(old_type)
            genre = QtWidgets.QLineEdit(old_genre)
            culture_combo = QtWidgets.QComboBox()
            categorie_combo = QtWidgets.QComboBox()
            culture_combo.addItem("Aucune", None)
            for c in get_all_cultures():
                culture_combo.addItem(c[1], c[0])
                if str(c[0]) == old_culture_id:
                    culture_combo.setCurrentIndex(culture_combo.count() - 1)
            categorie_combo.addItem("Aucune", None)
            for cat in get_all_categories():
                categorie_combo.addItem(cat[1], cat[0])
                if str(cat[0]) == old_categorie_id:
                    categorie_combo.setCurrentIndex(categorie_combo.count() - 1)
            layout.addRow("Valeur", valeur)
            layout.addRow("Type", type_field)
            layout.addRow("Genre", genre)
            layout.addRow("Culture", culture_combo)
            layout.addRow("Catégorie", categorie_combo)
            btn = QtWidgets.QPushButton("Enregistrer")
            layout.addWidget(btn)
            btn.clicked.connect(lambda: self._update_titre(
                dialog, titre_id, valeur.text(), type_field.text(), genre.text(),
                culture_combo.currentData(), categorie_combo.currentData()
            ))
            dialog.exec()

    def _update_titre(self, dialog, titre_id, valeur, type_field, genre, culture_id, categorie_id):
            from db import update_titre
            update_titre(titre_id, valeur, type_field, genre, culture_id, categorie_id)
            self.load_titres()
            dialog.accept()

    def supprimer_titre(self):
            from db import delete_titre
            row = self.titresTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un titre à supprimer.")
                return
            titre_id = self.titresTable.item(row, 0).text()
            reply = QtWidgets.QMessageBox.question(self, "Confirmer", "Supprimer ce titre ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                delete_titre(titre_id)
                self.load_titres()
            
    def __init__(self):
            super().__init__()
            ui_path = os.path.join(os.path.dirname(__file__), '../ui/nomina_main.ui')
            uic.loadUi(ui_path, self)

            # Layout principal
            central_widget = QtWidgets.QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QtWidgets.QVBoxLayout(central_widget)

            # Tableau des titres
            self.titresTable = QtWidgets.QTableWidget()
            self.titresTable.setColumnCount(10)
            self.titresTable.setHorizontalHeaderLabels([
                "ID", "Valeur", "Type", "Genre", "Culture (ID)", "Culture (Nom)", "Catégorie (ID)", "Catégorie (Nom)", "Créé", "Modifié"
            ])
            main_layout.addWidget(self.titresTable)

            # Tableau des concepts
            self.conceptsTable = QtWidgets.QTableWidget()
            self.conceptsTable.setColumnCount(9)
            self.conceptsTable.setHorizontalHeaderLabels([
                "ID", "Valeur", "Type", "Mood", "Keywords", "Catégorie (ID)", "Catégorie (Nom)", "Créé", "Modifié"
            ])
            main_layout.addWidget(self.conceptsTable)

            # Tableau des fragments d'histoire
            self.fragmentsTable = QtWidgets.QTableWidget()
            self.fragmentsTable.setColumnCount(10)
            self.fragmentsTable.setHorizontalHeaderLabels([
                "ID", "Texte", "AppliesTo", "Genre", "MinLen", "MaxLen",
                "Culture (ID)", "Culture (Nom)", "Catégorie (ID)", "Catégorie (Nom)"
            ])
            main_layout.addWidget(self.fragmentsTable)

            # Tableau des utilisateurs
            self.tableWidget = QtWidgets.QTableWidget()
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Nom d'utilisateur", "Email", "Rôle"])
            main_layout.addWidget(self.tableWidget)

            # Tableau des catégories
            self.categorieTable = QtWidgets.QTableWidget()
            self.categorieTable.setHorizontalHeaderLabels(["ID", "Nom", "Description", "Date création"])
            main_layout.addWidget(self.categorieTable)

            # Tableau des cultures
            self.cultureTable = QtWidgets.QTableWidget()
            self.cultureTable.setColumnCount(3)
            self.cultureTable.setHorizontalHeaderLabels(["ID", "Nom", "Description"])
            main_layout.addWidget(self.cultureTable)

            # Tableau des lieux
            self.lieuxTable = QtWidgets.QTableWidget()
            self.lieuxTable.setColumnCount(5)
            self.lieuxTable.setHorizontalHeaderLabels(["ID", "Nom du lieu", "Type", "Catégorie (ID)", "Catégorie (Nom)"])
            main_layout.addWidget(self.lieuxTable)

            # Layout des boutons CRUD
            button_layout = QtWidgets.QHBoxLayout()

            # Boutons CRUD pour Titre
            self.addTitreButton = QtWidgets.QPushButton("Ajouter un titre")
            self.addTitreButton.clicked.connect(self.ajouter_titre)
            button_layout.addWidget(self.addTitreButton)

            self.editTitreButton = QtWidgets.QPushButton("Modifier un titre")
            self.editTitreButton.clicked.connect(self.modifier_titre)
            button_layout.addWidget(self.editTitreButton)

            self.deleteTitreButton = QtWidgets.QPushButton("Supprimer un titre")
            self.deleteTitreButton.clicked.connect(self.supprimer_titre)
            button_layout.addWidget(self.deleteTitreButton)

            # Boutons CRUD pour Concept
            self.addConceptButton = QtWidgets.QPushButton("Ajouter un concept")
            self.addConceptButton.clicked.connect(self.ajouter_concept)
            button_layout.addWidget(self.addConceptButton)

            self.editConceptButton = QtWidgets.QPushButton("Modifier un concept")
            self.editConceptButton.clicked.connect(self.modifier_concept)
            button_layout.addWidget(self.editConceptButton)

            self.deleteConceptButton = QtWidgets.QPushButton("Supprimer un concept")
            self.deleteConceptButton.clicked.connect(self.supprimer_concept)
            button_layout.addWidget(self.deleteConceptButton)

            # Boutons CRUD pour FragmentsHistoire
            self.ajouterFragmentButton = QtWidgets.QPushButton("Ajouter un fragment")
            self.ajouterFragmentButton.clicked.connect(self.ajouter_fragment)
            button_layout.addWidget(self.ajouterFragmentButton)

            self.editFragmentButton = QtWidgets.QPushButton("Modifier un fragment")
            self.editFragmentButton.clicked.connect(self.modifier_fragment)
            button_layout.addWidget(self.editFragmentButton)

            self.deleteFragmentButton = QtWidgets.QPushButton("Supprimer un fragment")
            self.deleteFragmentButton.clicked.connect(self.supprimer_fragment)
            button_layout.addWidget(self.deleteFragmentButton)

            # Boutons CRUD pour Catégorie
            self.addCategorieButton = QtWidgets.QPushButton("Ajouter une catégorie")
            self.addCategorieButton.clicked.connect(self.ajouter_categorie)
            button_layout.addWidget(self.addCategorieButton)

            self.editCategorieButton = QtWidgets.QPushButton("Modifier une catégorie")
            self.editCategorieButton.clicked.connect(self.modifier_categorie)
            button_layout.addWidget(self.editCategorieButton)

            self.deleteCategorieButton = QtWidgets.QPushButton("Supprimer une catégorie")
            self.deleteCategorieButton.clicked.connect(self.supprimer_categorie)
            button_layout.addWidget(self.deleteCategorieButton)

            # Boutons CRUD pour Utilisateur
            self.addButton = QtWidgets.QPushButton("Ajouter un utilisateur")
            self.addButton.clicked.connect(self.ajouter_utilisateur)
            button_layout.addWidget(self.addButton)

            self.editButton = QtWidgets.QPushButton("Modifier un utilisateur")
            self.editButton.clicked.connect(self.modifier_utilisateur)
            button_layout.addWidget(self.editButton)

            self.deleteButton = QtWidgets.QPushButton("Supprimer un utilisateur")
            self.deleteButton.clicked.connect(self.supprimer_utilisateur)
            button_layout.addWidget(self.deleteButton)

            # Boutons CRUD pour Culture
            self.addCultureButton = QtWidgets.QPushButton("Ajouter une culture")
            self.addCultureButton.clicked.connect(self.ajouter_culture)
            button_layout.addWidget(self.addCultureButton)

            self.editCultureButton = QtWidgets.QPushButton("Modifier une culture")
            self.editCultureButton.clicked.connect(self.modifier_culture)
            button_layout.addWidget(self.editCultureButton)

            self.deleteCultureButton = QtWidgets.QPushButton("Supprimer une culture")
            self.deleteCultureButton.clicked.connect(self.supprimer_culture)
            button_layout.addWidget(self.deleteCultureButton)

            # Boutons CRUD pour Lieux
            self.addLieuxButton = QtWidgets.QPushButton("Ajouter un lieu")
            self.addLieuxButton.clicked.connect(self.ajouter_lieu)
            button_layout.addWidget(self.addLieuxButton)

            self.editLieuxButton = QtWidgets.QPushButton("Modifier un lieu")
            self.editLieuxButton.clicked.connect(self.modifier_lieu)
            button_layout.addWidget(self.editLieuxButton)

            self.deleteLieuxButton = QtWidgets.QPushButton("Supprimer un lieu")
            self.deleteLieuxButton.clicked.connect(self.supprimer_lieu)
            button_layout.addWidget(self.deleteLieuxButton)

            main_layout.addLayout(button_layout)

            self.load_users()
            self.load_categories()
            self.load_cultures()
            self.load_fragments()
            self.load_titres()
            self.load_concepts()

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

    def load_cultures(self):
            from db import get_all_cultures
            rows = get_all_cultures()
            self.cultureTable.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.cultureTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def ajouter_culture(self):
            from db import insert_culture
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
            from db import insert_culture
            insert_culture(name, description)
            self.load_cultures()
            dialog.accept()

    def modifier_culture(self):
            from db import update_culture
            row = self.cultureTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez une culture à modifier.")
                return
            culture_id = self.cultureTable.item(row, 0).text()
            old_name = self.cultureTable.item(row, 1).text()
            old_description = self.cultureTable.item(row, 2).text()
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Modifier une culture")
            layout = QtWidgets.QFormLayout(dialog)
            name = QtWidgets.QLineEdit(old_name)
            description = QtWidgets.QLineEdit(old_description)
            layout.addRow("Nom", name)
            layout.addRow("Description", description)
            btn = QtWidgets.QPushButton("Enregistrer")
            layout.addWidget(btn)
            btn.clicked.connect(lambda: self._update_culture(dialog, culture_id, name.text(), description.text()))
            dialog.exec()

    def _update_culture(self, dialog, culture_id, name, description):
            from db import update_culture
            update_culture(culture_id, name, description)
            self.load_cultures()
            dialog.accept()

    def supprimer_culture(self):
            from db import delete_culture
            row = self.cultureTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez une culture à supprimer.")
                return
            culture_id = self.cultureTable.item(row, 0).text()
            reply = QtWidgets.QMessageBox.question(self, "Confirmer", "Supprimer cette culture ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                delete_culture(culture_id)
                self.load_cultures()

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

    def supprimer_fragment(self):
            from db import delete_fragment
            row = self.fragmentsTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un fragment à supprimer.")
                return
            fragment_id = self.fragmentsTable.item(row, 0).text()
            reply = QtWidgets.QMessageBox.question(self, "Confirmer", "Supprimer ce fragment ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                delete_fragment(fragment_id)
                self.load_fragments()

    def modifier_fragment(self):
            from db import update_fragment, get_all_cultures, get_all_categories
            row = self.fragmentsTable.currentRow()
            if row < 0:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Sélectionnez un fragment à modifier.")
                return
            fragment_id = self.fragmentsTable.item(row, 0).text()
            old_texte = self.fragmentsTable.item(row, 1).text()
            old_appliesTo = self.fragmentsTable.item(row, 2).text()
            old_genre = self.fragmentsTable.item(row, 3).text()
            old_minNameLength = self.fragmentsTable.item(row, 4).text()
            old_maxNameLength = self.fragmentsTable.item(row, 5).text()
            old_culture_id = self.fragmentsTable.item(row, 6).text()
            old_categorie_id = self.fragmentsTable.item(row, 8).text()
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Modifier un fragment d'histoire")
            layout = QtWidgets.QFormLayout(dialog)
            texte = QtWidgets.QLineEdit(old_texte)
            appliesTo = QtWidgets.QLineEdit(old_appliesTo)
            genre = QtWidgets.QLineEdit(old_genre)
            minNameLength = QtWidgets.QLineEdit(old_minNameLength)
            maxNameLength = QtWidgets.QLineEdit(old_maxNameLength)
            culture_combo = QtWidgets.QComboBox()
            categorie_combo = QtWidgets.QComboBox()
            culture_combo.addItem("Aucune", None)
            for c in get_all_cultures():
                culture_combo.addItem(c[1], c[0])
                if str(c[0]) == old_culture_id:
                    culture_combo.setCurrentIndex(culture_combo.count() - 1)
            categorie_combo.addItem("Aucune", None)
            for cat in get_all_categories():
                categorie_combo.addItem(cat[1], cat[0])
                if str(cat[0]) == old_categorie_id:
                    categorie_combo.setCurrentIndex(categorie_combo.count() - 1)
            layout.addRow("Texte", texte)
            layout.addRow("AppliesTo", appliesTo)
            layout.addRow("Genre", genre)
            layout.addRow("MinLen", minNameLength)
            layout.addRow("MaxLen", maxNameLength)
            layout.addRow("Culture", culture_combo)
            layout.addRow("Catégorie", categorie_combo)
            btn = QtWidgets.QPushButton("Enregistrer")
            layout.addWidget(btn)
            btn.clicked.connect(lambda: self.update_fragment(
                dialog, fragment_id, texte.text(), appliesTo.text(), genre.text(),
                minNameLength.text(), maxNameLength.text(), culture_combo.currentData(), categorie_combo.currentData()
            ))
            dialog.exec()
            
    def load_fragments(self):
            from db import get_all_fragments
            rows = get_all_fragments()
            self.fragmentsTable.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.fragmentsTable.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
                    
    def update_fragment(self, dialog, fragment_id, texte, appliesTo, genre, minNameLength, maxNameLength, culture_id, categorie_id):
            from db import update_fragment
            update_fragment(fragment_id, texte, appliesTo, genre, minNameLength, maxNameLength, culture_id, categorie_id)
            self.load_fragments()
            dialog.accept()

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
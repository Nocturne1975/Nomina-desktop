from PyQt6 import QtWidgets
from db import get_all_users, insert_user, update_user, delete_user

class UserManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des utilisateurs")
        self.resize(700, 400)
        layout = QtWidgets.QVBoxLayout()

        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom d'utilisateur", "Email", "Rôle", "Actif", "Créé le", "Modifié le"
        ])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.edit_user)
        layout.addWidget(self.table)

        # Boutons
        btn_layout = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("Ajouter")
        self.add_btn.clicked.connect(self.add_user)
        btn_layout.addWidget(self.add_btn)
        self.del_btn = QtWidgets.QPushButton("Supprimer")
        self.del_btn.clicked.connect(self.delete_selected_user)
        btn_layout.addWidget(self.del_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.refresh_table()

    def refresh_table(self):
        users = get_all_users()
        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            for col, value in enumerate(user):
                self.table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    def add_user(self):
        dialog = UserDialog(self)
        if dialog.exec():
            username, password, email, role, isActive = dialog.get_data()
            insert_user(username, password, email, role, isActive)
            self.refresh_table()

    def edit_user(self, row, col):
        user_id = int(self.table.item(row, 0).text())
        username = self.table.item(row, 1).text()
        email = self.table.item(row, 2).text()
        role = self.table.item(row, 3).text()
        isActive = self.table.item(row, 4).text() == 'True'
        dialog = UserDialog(self, username, email, role, isActive)
        if dialog.exec():
            new_username, password, new_email, new_role, new_isActive = dialog.get_data()
            update_user(user_id, username=new_username, password=password, email=new_email, role=new_role, isActive=new_isActive)
            self.refresh_table()

    def delete_selected_user(self):
        row = self.table.currentRow()
        if row < 0:
            return
        user_id = int(self.table.item(row, 0).text())
        reply = QtWidgets.QMessageBox.question(self, "Confirmation", f"Supprimer l'utilisateur {user_id} ?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            delete_user(user_id)
            self.refresh_table()

class UserDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, username="", email="", role="Editor", isActive=True):
        super().__init__(parent)
        self.setWindowTitle("Gestion d'utilisateur")
        layout = QtWidgets.QFormLayout()
        self.username_input = QtWidgets.QLineEdit(username)
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.email_input = QtWidgets.QLineEdit(email)
        self.role_input = QtWidgets.QComboBox()
        self.role_input.addItems(["Admin", "Editor", "Viewer"])
        self.role_input.setCurrentText(role)
        self.active_input = QtWidgets.QCheckBox()
        self.active_input.setChecked(isActive)
        layout.addRow("Nom d'utilisateur", self.username_input)
        layout.addRow("Mot de passe", self.password_input)
        layout.addRow("Email", self.email_input)
        layout.addRow("Rôle", self.role_input)
        layout.addRow("Actif", self.active_input)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)
        self.setLayout(layout)

    def get_data(self):
        return (
            self.username_input.text(),
            self.password_input.text(),
            self.email_input.text(),
            self.role_input.currentText(),
            self.active_input.isChecked()
        )
        
    def validate_inputs(self):
        if not self.username_input.text().strip():
            return "Le nom d'utilisateur ne peut pas être vide."
        if not self.email_input.text().strip():
            return "L'email est obligatoire."
        return None

    def accept(self):
        error = self.validate_inputs()
        if error:
            QtWidgets.QMessageBox.warning(self, "Validation", error)
        else:
            super().accept()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = UserManager()
    win.show()
    sys.exit(app.exec())
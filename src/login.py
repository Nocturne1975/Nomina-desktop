from PyQt6 import QtWidgets
from db import check_user_credentials

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setFixedSize(300, 150)

        layout = QtWidgets.QVBoxLayout()

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        layout.addWidget(self.username_input)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QtWidgets.QPushButton("Se connecter")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.error_label = QtWidgets.QLabel("")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if check_user_credentials(username, password):
            self.accept()
        else:
            self.error_label.setText("Identifiants incorrects.")

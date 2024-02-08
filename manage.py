from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from pygame import mixer
from moviepy.editor import AudioFileClip
import qrcode

class CadastroWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Cadastro')
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.label_nome = QLabel('Nome:', self)
        self.label_nome.setObjectName('labelNome')
        self.label_nome.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.label_nome)

        self.input_nome = QLineEdit(self)
        self.input_nome.setObjectName('inputNome')
        self.input_nome.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.input_nome)

        self.label_email = QLabel('E-mail:', self)
        self.label_email.setObjectName('labelEmail')
        self.label_email.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.label_email)

        self.input_email = QLineEdit(self)
        self.input_email.setObjectName('inputEmail')
        self.input_email.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.input_email)

        self.button_cadastrar = QPushButton('Cadastrar', self)
        self.button_cadastrar.setIcon(QIcon('icon_cadastro.png'))
        self.layout.addWidget(self.button_cadastrar)

        self.button_cadastrar.clicked.connect(self.realizar_cadastro)

        self.setLayout(self.layout)

    def realizar_cadastro(self):
        nome = self.input_nome.text()
        email = self.input_email.text()

        if nome and email:
            QMessageBox.information(self, 'Cadastro Realizado', f'Cadastro realizado com sucesso!\nNome: {nome}\nE-mail: {email}')
            self.audio_window = AudioWindow()
            self.audio_window.show()
            generate_qr_code()  # Chamada da função para gerar o QR Code
        else:
            QMessageBox.warning(self, 'Erro no Cadastro', 'Por favor, preencha todos os campos.')

class AudioWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Reprodução de Áudio')
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.button_reproduzir_audio = QPushButton('Reproduzir Áudio', self)
        self.button_reproduzir_audio.setIcon(QIcon('icon_audio.png'))
        self.button_reproduzir_audio.clicked.connect(self.reproduzir_audio)
        self.layout.addWidget(self.button_reproduzir_audio)

        self.setLayout(self.layout)

        self.arquivo_audio_mp3 = 'audio.mp3'
        self.arquivo_audio_wav = 'audio.wav'

        audio_clip = AudioFileClip(self.arquivo_audio_mp3)
        audio_clip.write_audiofile(self.arquivo_audio_wav)

        mixer.init()

    def reproduzir_audio(self):
        try:
            mixer.music.load(self.arquivo_audio_wav)
            mixer.music.play()
        except Exception as e:
            QMessageBox.warning(self, 'Erro na Reprodução', f'Ocorreu um erro ao reproduzir o áudio: {str(e)}')

# Função para gerar o QR Code
def generate_qr_code():
    app_link = "https://drive.google.com/drive/folders/1eo72a6_TdXs5-ggxTW-C77xW20Ot5J4o?usp=drive_link"  # Substitua isso pelo link real do seu arquivo no Google Drive
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(app_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("app_qr_code.png")

if __name__ == '__main__':
    app = QApplication([])

    style = """
    QLineEdit {
        border-radius: 10px;
        border: 2px solid #ccc;
        padding: 8px;
    }

    #inputNome {
        background-color: #f2f2f2;
    }

    #inputEmail {
        background-color: #f2f2f2;
    }

    QPushButton {
        background-color: #4287f5; /* Azul */
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 10px;
    }

    QPushButton:hover {
        background-color: #0e5ea5; /* Azul mais escuro no hover */
    }

    QPushButton:pressed {
        background-color: #0a4369; /* Azul ainda mais escuro quando pressionado */
    }

    #labelNome, #labelEmail {
        font-size: 16px;
        font-weight: bold;
        color: #333;
    }
    """
    app.setStyleSheet(style)

    cadastro_window = CadastroWindow()
    cadastro_window.show()

    app.exec_()

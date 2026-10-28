import sys
import threading
from flask import Flask, request
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                               QFileDialog, QLabel, QComboBox)
from playsound3 import playsound

app = Flask(__name__)
audio_path_global = ""

@app.route('/alarme', methods=['GET', 'POST'])
def alarme():
    print("Alarme recebido do NVR!")
    if audio_path_global:
        try:
            playsound(audio_path_global, block=False)
        except Exception as e:
            print(f"Erro ao tocar áudio: {e}")
    return "OK", 200

def iniciar_servidor():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alarme Antifadiga Alert System")
        self.setGeometry(100, 100, 500, 300)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Fabricante do NVR:"))
        self.combo_modelo = QComboBox()
        self.combo_modelo.addItems(["Intelbras", "Hikvision", "Outro"])
        layout.addWidget(self.combo_modelo)

        layout.addWidget(QLabel("Arquivo de Áudio:"))
        self.btn_audio = QPushButton("Selecionar Áudio")
        self.btn_audio.clicked.connect(self.selecionar_audio)
        self.lbl_audio = QLabel("Nenhum arquivo selecionado")
        layout.addWidget(self.btn_audio)
        layout.addWidget(self.lbl_audio)

        self.lbl_status = QLabel("Status: Parado")
        layout.addWidget(self.lbl_status)

        self.btn_iniciar = QPushButton("Iniciar Escuta")
        self.btn_iniciar.clicked.connect(self.iniciar_escuta)
        layout.addWidget(self.btn_iniciar)

        self.setLayout(layout)

    def selecionar_audio(self):
        global audio_path_global
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Áudio", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_name:
            audio_path_global = file_name
            self.lbl_audio.setText(file_name)

    def iniciar_escuta(self):
        if not audio_path_global:
            self.lbl_status.setText("Status: Selecione um áudio primeiro!")
            return
        thread = threading.Thread(target=iniciar_servidor, daemon=True)
        thread.start()
        self.lbl_status.setText("Status: Escutando na porta 5000...")
        self.btn_iniciar.setEnabled(False)

if __name__ == "__main__":
    app_qt = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app_qt.exec())

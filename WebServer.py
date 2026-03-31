from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """Класс для обработки запросов от клиента"""

    def get_html_content(self, filename):
        """Вспомогательный метод для чтения файлов"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return None

    def do_GET(self):
        path = self.path

        if path == "/":
            filename = "main.html"
        else:
            filename = path.lstrip("/")

        content = self.get_html_content(filename)

        if content:

            content_type = "text/plain"
            if filename.endswith(".html"):
                content_type = "text/html"
            elif filename.endswith(".css"):
                content_type = "text/css"
            elif filename.endswith(".js"):
                content_type = "application/javascript"
            elif filename.endswith(".png"):
                content_type = "image/png"
            elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
                content_type = "image/jpeg"

            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404 Not Found", "utf-8"))


if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("server started: http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("server stopped")

import http.server
import socketserver
import os
import urllib.parse
import mimetypes

PORT = 3000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

mimetypes.add_type('text/javascript', '.mjs')
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('font/woff', '.woff')
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('image/webp', '.webp')

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def translate_path(self, path):
        # Strip query string and fragments
        parsed = urllib.parse.urlparse(path)
        clean_path = parsed.path

        # Handle root or /demos/beach routes
        if clean_path in ('', '/', '/demos/beach', '/demos/beach/'):
            return os.path.join(BASE_DIR, 'index.html')

        # Strip leading slash
        rel_path = clean_path.lstrip('/')
        
        # Check if requesting directly from images/ or assets/
        if rel_path.startswith('images/'):
            target = os.path.join(BASE_DIR, 'assets', rel_path)
            if os.path.exists(target):
                return target

        # Direct file in workspace or assets
        target = os.path.join(BASE_DIR, rel_path.replace('/', os.sep))
        if os.path.exists(target):
            return target
            
        # Check inside assets/
        assets_target = os.path.join(BASE_DIR, 'assets', rel_path.replace('/', os.sep))
        if os.path.exists(assets_target):
            return assets_target

        # Check inside assets/images/
        basename = os.path.basename(clean_path)
        img_target = os.path.join(BASE_DIR, 'assets', 'images', basename)
        if os.path.exists(img_target):
            return img_target

        # Fallback to default translation
        return super().translate_path(clean_path)

def run():
    port = PORT
    for p in [3000, 8080, 5000, 8000]:
        try:
            handler = CustomHandler
            # Allow address reuse
            socketserver.TCPServer.allow_reuse_address = True
            with socketserver.TCPServer(("", p), handler) as httpd:
                print(f"SERVER_STARTED_ON_PORT:{p}")
                print(f"Serving Wedding Invitation Card template at http://localhost:{p}")
                print(f"Also accessible at http://127.0.0.1:{p}/demos/beach")
                httpd.serve_forever()
            break
        except OSError as e:
            if e.errno == 10048 or "Address already in use" in str(e):
                continue
            else:
                raise e

if __name__ == '__main__':
    run()

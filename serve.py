# Servidor estático con soporte de Range (necesario para <video>) y gzip para texto, como hará Apache con .htaccess
import os, re, sys, gzip, io
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
class H(SimpleHTTPRequestHandler):
    GZ = ('text/html', 'text/css', 'application/javascript', 'text/javascript', 'application/json', 'text/plain', 'application/xml', 'text/xml', 'image/svg+xml', 'application/manifest+json')
    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            if not self.path.endswith('/') or not os.path.isfile(os.path.join(path, 'index.html')): return super().send_head()
            path = os.path.join(path, 'index.html')
        ctype = self.guess_type(path)
        if 'Range' not in self.headers and ctype in self.GZ and 'gzip' in self.headers.get('Accept-Encoding', ''):
            try: raw = open(path, 'rb').read()
            except OSError: self.send_error(404); return None
            body = gzip.compress(raw, 6)
            self.send_response(200)
            self.send_header('Content-type', ctype); self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(body))); self.send_header('Cache-Control', 'no-cache')
            self.end_headers(); return io.BytesIO(body)
        if 'Range' not in self.headers:
            return super().send_head()
        try: f = open(path, 'rb')
        except OSError: self.send_error(404); return None
        size = os.fstat(f.fileno()).st_size
        m = re.match(r'bytes=(\d*)-(\d*)', self.headers['Range'])
        start = int(m.group(1) or 0); end = int(m.group(2) or size - 1); end = min(end, size - 1)
        if start > end: self.send_error(416); f.close(); return None
        self.send_response(206)
        self.send_header('Content-type', self.guess_type(path))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        f.seek(start); self.range = (start, end); return f
    def copyfile(self, src, dst):
        r = getattr(self, 'range', None)
        if not r: return super().copyfile(src, dst)
        left = r[1] - r[0] + 1
        while left > 0:
            chunk = src.read(min(65536, left))
            if not chunk: break
            dst.write(chunk); left -= len(chunk)
        self.range = None
    def log_message(self, *a): pass
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()

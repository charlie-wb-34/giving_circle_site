#!/usr/bin/env python3
"""Dev server that mirrors the nginx try_files routing: $uri $uri.html /pages$uri.html"""
import http.server, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Strip query string
        path = path.split('?', 1)[0].split('#', 1)[0]
        candidates = [
            path,
            path.rstrip('/') + '.html' if not path.endswith('.html') else None,
            '/pages' + path.rstrip('/') + '.html' if not path.endswith('.html') else None,
        ]
        for c in candidates:
            if c is None:
                continue
            full = ROOT + c
            if os.path.isfile(full):
                return full
        return ROOT + path  # let base class handle (will 404)

    def log_message(self, fmt, *args):
        print(fmt % args)

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
with http.server.HTTPServer(('', port), Handler) as s:
    print(f'Serving at http://localhost:{port}')
    s.serve_forever()

#!/usr/bin/env python3
"""윤문비교 폴더를 브라우저가 fetch 할 수 있게 띄운다.

클립보드로 붙여넣으면 사용자가 복사를 할 때마다 충돌한다. 대신 Dola 페이지에서
http://localhost:8765/ch05/보낼산문.txt 를 직접 읽어 가게 한다.

    py tools/serve_prose.py
"""
from __future__ import annotations

import functools
import http.server
import socketserver
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "윤문비교"
PORT = 8765


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        # https 페이지가 localhost 를 부를 때 크롬이 요구하는 헤더
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        """/save?ch=ch26 으로 받은 본문을 윤문비교/ch26/Dola_응답.txt 로 저장한다."""
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(self.path).query)
        ch = (q.get("ch") or [""])[0]
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n).decode("utf-8", "replace")
        ok = False
        if ch and body.strip():
            dst = ROOT / ch / "Dola_응답.txt"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(body, encoding="utf-8")
            ok = True
        self.send_response(200 if ok else 400)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ok" if ok else b"no")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    handler = functools.partial(Handler, directory=str(ROOT))
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"http://localhost:{PORT}/ 에서 {ROOT} 제공 중")
        httpd.serve_forever()

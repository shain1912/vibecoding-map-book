#!/usr/bin/env python3
"""그림작업 폴더를 브라우저에서 열 수 있게 띄운다 (file:// 은 확장이 못 연다).

    py tools/serve_fig.py
"""
from __future__ import annotations

import functools
import http.server
import socketserver
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "그림작업"
PORT = 8790


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT),
                                functools.partial(Handler, directory=str(ROOT))) as s:
        print(f"http://localhost:{PORT}/ 에서 {ROOT} 제공 중")
        s.serve_forever()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel Serverless Function - 股票市场数据中转站
路径: /api/index.py
访问: https://your-project.vercel.app/api
"""

import json
from http.server import BaseHTTPRequestHandler

# Vercel Serverless Function 主入口
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            'message': 'API is working!',
            'path': self.path
        }
        self.wfile.write(json.dumps(response).encode())

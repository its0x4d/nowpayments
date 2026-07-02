"""
Minimal IPN webhook receiver for local testing.

Usage:
  export NOWPAYMENTS_IPN_SECRET=your_ipn_secret
  python examples/webhook_server.py

Expose with ngrok:
  ngrok http 8080
  # Use the ngrok URL as ipn_callback_url when creating payments
"""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from nowpayment import IPNVerificationError, extract_ipn_signature, verify_ipn_payload


class IPNHandler(BaseHTTPRequestHandler):
    ipn_secret = os.environ.get("NOWPAYMENTS_IPN_SECRET", "")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        signature = extract_ipn_signature(self.headers)
        try:
            verified = verify_ipn_payload(payload, self.ipn_secret, signature)
        except IPNVerificationError as exc:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(str(exc).encode("utf-8"))
            return

        print("Verified IPN:", verified)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


def main() -> None:
    if not IPNHandler.ipn_secret:
        raise SystemExit("Set NOWPAYMENTS_IPN_SECRET before starting the webhook server.")

    host = "0.0.0.0"
    port = 8080
    server = HTTPServer((host, port), IPNHandler)
    print(f"Listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()

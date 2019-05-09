import json
import marshal
import os
from base64 import b64decode
from contextlib import redirect_stderr, redirect_stdout
from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import StringIO

MARSHAL_RAISES = (KeyError, ValueError, TypeError, EOFError)


class Executor:
    def __init__(self, host="", port=18888, handler=SimpleHTTPRequestHandler):
        self._httpd = HTTPServer((host, port), handler)
        self._httpd.serve_forever()

    @staticmethod
    def execute(self, code):
        out = StringIO()
        err = StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            exec(code)

        return {"out": out.getvalue(), "err": err.getvalue()}


class Handler(SimpleHTTPRequestHandler):
    execute = Executor.execute

    def do_POST(self, *args, **kwargs):
        content_length = int(self.headers["Content-Length"])
        raw_body = self.rfile.read(content_length).decode()
        print(raw_body)
        body = json.loads(raw_body)

        try:
            code = marshal.loads(b64decode(body["code"]))
            self.respond(self.execute(code), 200)
        except MARSHAL_RAISES as exc:
            self.respond("FAIL", 400)
        except Exception as exc:
            self.respond("FAIL", 500)

    def respond(self, result, code):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(json.dumps({"result": result}).encode())


if __name__ == "__main__":
    executor = Executor(port=os.environ.get("EXECUTOR_PORT", 18888), handler=Handler)

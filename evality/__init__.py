import ast
import atexit
import json
import marshal
import os
import socket
import time
from base64 import b64encode
from contextlib import contextmanager
from pathlib import Path
from urllib.request import Request, urlopen

import docker

from evality.purifier import Insecure, Purifier


class Evality:
    def __init__(self, docker_client, api_client):
        self._docker_client = docker_client
        self._api_client = api_client
        self._image = self.obtain_image(force_build = True)

        self._instances = {}
        self._ports = {}

        self._delay = 1.5
        self._purifier = Purifier()
        atexit.register(self.quit)

    def run_cmd(self, code, idx=0):
        """Runs python code on the containers,
        code is self-explaining, step-by-step"""

        tree = ast.parse(code)
        try:
            self._purifier.visit(tree)

            code = compile(tree, "<evality>", "exec")
            code = marshal.dumps(code)
            code = b64encode(code)

            payload = {"code": code.decode()}
            payload = json.dumps(payload)

            with self.run_instance(idx) as container:
                request = Request(
                    f"http://localhost:{self._ports[container]}",
                    data=payload.encode(),
                    method="POST",
                )

                response = urlopen(request)
                response = json.loads(response.read().decode())

        except Insecure as exc:
            response = {"result": "FAIL", "msg": exc}

        return response

    @contextmanager
    def run_instance(self, idx):
        new = self._instances.get(idx)
        if new:
            container = new
        else:
            port = self._get_free_port()
            container = self._docker_client.containers.run(
                "evality", ports={"18888/tcp": port}, detach=True
            )
            self._ports[container] = port
            self._instances[idx] = container
        try:
            if new:
                container.unpause()
            else:
                time.sleep(self._delay)
            yield container
        finally:
            container.pause()

    def quit(self):
        for container in self._instances.copy():
            self.quit_single(container)

        self._ports = {}

    def quit_single(self, idx):
        return self._instances.pop(idx).kill()

    def obtain_image(self, force_build = False):
        try:
            if force_build:
                raise docker.errors.ImageNotFound(None)
            return self._docker_client.images.get("evality")
        except docker.errors.ImageNotFound:
            return self._docker_client.images.build(
                path=os.fspath(Path(__file__).parent), tag="evality"
            )[0]

    def _get_free_port(self, plus=1):
        port = max(self._ports.values(), default=1764) + plus
        if self.check_empty_port(port):
            return self._get_free_port(plus=(port - 1764) + 1)
        else:
            return port

    @staticmethod
    def check_empty_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return not bool(sock.connect_ex(("127.0.0.1", port)))

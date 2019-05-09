import ast
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

from purifier import Insecure, Purifier


class Evality:
    def __init__(self, docker_client, api_client):
        self._docker_client = docker_client
        self._api_client = api_client
        self._image = self.obtain_image()

        self._ports = {}

        self._delay = 1
        self._purifier = Purifier()

    def run_cmd(self, code):
        tree = ast.parse(code)
        try:
            # step by step for easy understanding
            self._purifier.visit(tree)

            code = compile(tree, "<evality>", "exec")
            code = marshal.dumps(code)
            code = b64encode(code)

            payload = {"code": code.decode()}
            payload = json.dumps(payload)

            with self.run_instance() as container:
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
    def run_instance(self):
        port = self._get_free_port()
        container = self._docker_client.containers.run(
            "evality", ports={"18888/tcp": port}, detach=True
        )
        self._ports[container] = port
        try:
            time.sleep(self._delay)
            yield container
        finally:
            container.kill()

    def obtain_image(self):
        try:
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


if __name__ == "__main__":
    docker_client = docker.from_env()
    api_client = docker.APIClient(base_url="unix://var/run/docker.sock")
    evality = Evality(docker_client, api_client)

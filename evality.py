import os
import docker
from pathlib import Path

class Evality:
    def __init__(self, docker_client, api_client):
        self._docker_client = docker_client
        self._api_client = api_client
        self._image = self.obtain_image()

    def obtain_image(self):
        try:
            return self._docker_client.images.get('evality')
        except docker.errors.ImageNotFound:
            return self._docker_client.images.build(
                path = os.fspath(Path(__file__).parent), 
                tag='evality'
            )[0]

if __name__ == '__main__':
    docker_client = docker.from_env()
    api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
    evality = Evality(docker_client, api_client)
    print(evality._image)

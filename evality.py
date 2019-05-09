import docker
from platform import python_version
    
class Evality:
    def __init__(self, client):
        self._client = client
        self._base_image = self.obtain_image(python_version())

    def obtain_image(self, version):
        image = f"python:{version[:3]}-alpine"
        try:
            image = self._client.images.get(image)
        except:
            image = self._client.images.pull(image)
        
        return image

if __name__ == '__main__':
    client = docker.from_env()
    evality = Evality(client)
    print(evality._image)

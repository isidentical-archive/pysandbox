import docker
from io import BytesIO
from dataclass import dataclass, field
from platform import python_version

BytField = field(default_factory=BytesIO)

@dataclass
class Buffers:
    stdout: BytesIO = BytField
    stdin: BytesIO = BytField
    
@dataclass
class Result:
    exit_code: int
    buffers: Buffers = field(default_factory=Buffers)
    
class Evality:
    def __init__(self, client):
        self._client = client
        self._image = self.obtain_image(

    def obtain_image(self, version):
        image = f"python:{version[:3]}-alpine"
        try:
            image = self._client.images.get(image)
        except:
            image = self._client.images.pull(image)
        
        return image

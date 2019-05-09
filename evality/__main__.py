import sys
import docker
from evality import Evality

def main(evality, cmd):
    res = evality.run_cmd(cmd.strip("'"))
    print(res)
    
if __name__ == "__main__":
    docker_client = docker.from_env()
    api_client = docker.APIClient(base_url="unix://var/run/docker.sock")
    evality = Evality(docker_client, api_client)
    main(evality, *sys.argv[1:])

import time

import docker

from evality import Evality


def main(evality):
    cmd = "print('hello world')"
    while cmd != "!q":
        t0 = time.time()
        res = evality.run_cmd(cmd)
        t1 = time.time()
        print(res, f"{t1 - t0} seconds")
        cmd = input("cmd> ")
    evality.quit()


if __name__ == "__main__":
    docker_client = docker.from_env()
    api_client = docker.APIClient(base_url="unix://var/run/docker.sock")
    evality = Evality(docker_client, api_client)
    main(evality)

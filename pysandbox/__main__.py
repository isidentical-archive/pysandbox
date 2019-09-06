import time

import docker

from pysandbox import PySandbox


def main(pysandbox):
    cmd = "print('hello world')"
    while cmd != "!q":
        t0 = time.time()
        res = pysandbox.run_cmd(cmd)
        t1 = time.time()
        print(res, f"{t1 - t0} seconds")
        cmd = input("cmd> ")
    pysandbox.quit()


if __name__ == "__main__":
    docker_client = docker.from_env()
    api_client = docker.APIClient(base_url="unix://var/run/docker.sock")
    pysandbox = PySandbox(docker_client, api_client)
    main(pysandbox)

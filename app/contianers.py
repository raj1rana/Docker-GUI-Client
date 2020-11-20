import docker

client = docker.from_env()


def get_containers():
    ct = []
    for container in client.containers.list():
        ct.append({"id": container.id, "name": container.name, "image": container.name, "network": container.ports})
    print(ct)
    return ct

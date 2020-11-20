import docker
client = docker.from_env()

data = client.images.get_registry_data(name="php", auth_config=None)
print(data.id, data.attrs)
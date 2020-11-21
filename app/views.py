from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import docker
from django.contrib import messages
import requests
import json
#from json import JSONEncoder
from .customfunctions import customDecoder

# Create your views here.
client = docker.from_env()
docker_hub_url = ''
repoName = ''


def index(request):
    images = client.images.list()
    total_running_containers = len(client.containers.list())
    image_list = len(client.images.list())
    stopped_containers = len(client.containers.list(filters={"status": "exited"}))

    return render(request, 'home.html', {'total_running_containers': total_running_containers, 'image_list': image_list,
                                         'stopped_containers': stopped_containers, 'images': images})


def pull_image(request):
    output = []
    image = client.images.pull(request.GET('image_name'))
    output.append(image.id)
    output.append(image.repository)
    output.append(image.tag)
    return HttpResponse(output)


def create_container(request):
    if request.method == 'POST':
        try:
            name = request.POST['container_name']
            image = str(request.POST['image'])
            inner_port = request.POST['inner_port']
            outer_port = request.POST['outer_port']
            client.containers.run(image=image, name=name, ports={inner_port: outer_port}, detach=True)
            messages.success(request, "The container {0} has been successfully created".format(name))
            return HttpResponseRedirect(reverse('create_container'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('create_container'))
    else:
        images = client.images.list()
        containers = client.containers.list(all=True)
        return render(request, 'containers.html', {"images": images, "containers": containers})


def stop_container(request, id):
    # noinspection PyBroadException
    try:
        container = client.containers.get(id)
        container.stop()
        messages.warning(request, "The container {0} has been successfully stopped".format(container.name))
        return HttpResponseRedirect(reverse('create_container'))
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('create_container'))


def start_container(request, id):
    try:
        container = client.containers.get(id)
        container.start()
        messages.success(request, "The container {0} has been successfully started".format(container.name))
        return HttpResponseRedirect(reverse('create_container'))
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('create_container'))


def delete_container(request, id):
    try:
        container = client.containers.get(id)
        container.remove(v=True)
        messages.info(request, "The container {0} has been successfully deleted".format(container.name))
        return HttpResponseRedirect(reverse('create_container'))
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('create_container'))


def get_image(request):
    try:
        image = client.images.search(request.POST['name'])
        return render(request, 'images.html', {"images": image})
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('index'))


def get_image_info(request, name, stars, repo):
    try:
        global docker_hub_url
        global repoName
        docker_hub_url = 'https://registry.hub.docker.com/v2/repositories/library/{0}/tags'.format(name)
        data = requests.get('https://registry.hub.docker.com/v2/repositories/library/{0}/tags'.format(name))
        repoName = name
        obj = json.loads(data.content, object_hook=customDecoder)
        return render(request, 'image_detail.html',
                      {"name": repo + '/' + name, "stars": stars, "repo": repo, "data": obj})
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('get_image'))


def search_image(request):
    try:
        string = request.POST['search_image']
        global docker_hub_url
        global repoName
        url = docker_hub_url + '/' + string
        data = requests.get(url)
        obj = json.loads(data.text, object_hook=customDecoder)
        print(type(obj))
        return render(request, 'search_tag.html', {"data": obj, "repoNme": repoName})
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('get_image'))


def previous_tag_list(request, encoded_url):
    try:
        data = requests.get(encoded_url)
        global repoName
        obj = json.loads(data.text, object_hook=customDecoder)
        return render(request, 'pagination_tags.html', {"data": obj, "repoNme": repoName})
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('get_image_info2'))


def next_tag_list(request, encoded_url):
    try:
        data = requests.get(encoded_url)
        global repoName
        obj = json.loads(data.text, object_hook=customDecoder)
        return render(request, 'pagination_tags.html', {"data": obj, "repoNme": repoName})
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('get_image_info2'))


def pull_image_from_docker_hub(request, rpnme, tag):
    try:
        client.images.pull(repository=rpnme, tag=tag)
        messages.success(request, "the image {}/{} has been successfully pulled from docker hub".format(rpnme, tag))
        return HttpResponseRedirect(reverse('index'))

    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('index'))


def build_image(request):

    return render(request, 'build_image.html')
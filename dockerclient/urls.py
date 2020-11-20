"""dockerclient URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('pull_image', pull_image, name="pull_image"),
    path('create_container', create_container, name="create_container"),
    path('stop_container/<str:id>/', stop_container, name="stop_container"),
    path('start_container/<str:id>/', start_container, name="start_container"),
    path('delete_container/<str:id>/', delete_container, name="delete_container"),
    path('get_image_info/<str:name>/<str:stars>', get_image_info, name="get_image_info"),
    path('get_image_info/<str:repo>/<str:name>/<str:stars>', get_image_info, name="get_image_info2"),
    path('search_image', search_image, name="search_image"),
    path('get_image/', get_image, name="get_image"),
    path('previous_tag_list/<path:encoded_url>/', previous_tag_list, name="previous_tag_list"),
    path('next_tag_list/<path:encoded_url>/', next_tag_list, name="next_tag_list"),
    path('pull_image/<str:rpnme>/<str:tag>/', pull_image_from_docker_hub, name="pull_image"),
]


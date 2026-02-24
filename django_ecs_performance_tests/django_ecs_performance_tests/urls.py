"""URL configuration for django_ecs_performance_tests project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/

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
from django.urls import path, re_path
from world.views import (
    ChatConsumer,
    chat_index,
    chat_room,
    db,
    db_async,
    dbs,
    sse,
    sse_async,
    dbs_async,
    fortunes,
    fortunes_async,
    json_view,
    json_view_async,
    plaintext,
    plaintext_async,
    update,
    update_async,
)

urlpatterns = [
    # SYNC VIEWS
    path("admin/", admin.site.urls),
    path("plaintext/", plaintext),
    path("json/", json_view),
    path("db/", db),
    path("dbs/", dbs),
    path("fortunes/", fortunes),
    path("update/", update),
    path("sse/", sse),

    # ASYNC VIEWS
    path("plaintext_async/", plaintext_async),
    path("json_async/", json_view_async),
    path("db_async/", db_async),
    path("dbs_async/", dbs_async),
    path("fortunes_async/", fortunes_async),
    path("update_async/", update_async),
    path("sse_async/", sse_async),

    path("chat_index/", chat_index, name="chat_index"),
    path("chat/<str:room_name>/", chat_room, name="chat_room"),
]

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]

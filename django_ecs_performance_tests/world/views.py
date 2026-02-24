import asyncio
import json
import logging
import random
import time
from functools import partial
from operator import itemgetter

from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from orjson import dumps

from world.models import Fortune, World

_random_int = partial(random.randint, 1, 10000)

logger = logging.getLogger(__name__)


# SYNC VIEWS
def _get_queries(request):
    try:
        queries = int(request.GET.get("queries", 1))
    except Exception:
        queries = 1
    queries = max(queries, 1)
    return min(queries, 500)


def plaintext(request):
    return StreamingHttpResponse("Hello, World!", content_type="text/plain")


def json_view(request):
    return HttpResponse(
        dumps({"message": "Hello, World!"}), content_type="application/json",
    )


def db(request):
    r = _random_int()
    world = dumps({"id": r, "randomNumber": World.objects.get(id=r).randomnumber})
    return HttpResponse(world, content_type="application/json")


def dbs(request):
    queries = _get_queries(request)

    def caller(input_):
        int_ = _random_int()
        return {"id": int_, "randomNumber": World.objects.get(id=int_).randomnumber}

    worlds = tuple(map(caller, range(queries)))

    return HttpResponse(dumps(worlds), content_type="application/json")


def fortunes(request):
    fortunes = list(Fortune.objects.values("id", "message"))
    fortunes.append({"id": 0, "message": "Additional fortune added at request time."})
    fortunes.sort(key=itemgetter("message"))

    return render(request, "fortunes.html", {"fortunes": fortunes})


def update(request):
    queries = _get_queries(request)

    def caller(input_):
        w = World.objects.get(id=_random_int())
        w.randomnumber = _random_int()
        w.save()
        return {"id": w.pk, "randomNumber": w.randomnumber}

    worlds = tuple(map(caller, range(queries)))

    return HttpResponse(dumps(worlds), content_type="application/json")


def sse(request):
    def event_stream():
        i = 0
        while True:
            yield f"data: hello {i}\n"
            i += 1
            time.sleep(1)

    return StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream",
    )


# ASYNC VIEWS
async def _get_queries_async(request):
    try:
        queries = int(request.GET.get("queries", 1))
    except Exception:
        queries = 1
    queries = max(queries, 1)
    return min(queries, 500)


async def plaintext_async(request):
    return StreamingHttpResponse("Hello, World!", content_type="text/plain")


async def json_view_async(request):
    return HttpResponse(
        dumps({"message": "Hello, World!"}), content_type="application/json",
    )


async def db_async(request):
    r = _random_int()
    world = dumps({"id": r, "randomNumber": World.objects.get(id=r).randomnumber})
    return HttpResponse(world, content_type="application/json")


async def dbs_async(request):
    queries = await _get_queries_async(request)

    async def caller(input_):
        int_ = _random_int()
        return {"id": int_, "randomNumber": World.objects.get(id=int_).randomnumber}

    worlds = tuple(map(caller, range(queries)))

    return HttpResponse(dumps(worlds), content_type="application/json")


async def fortunes_async(request):
    fortunes = list(Fortune.objects.values("id", "message"))
    fortunes.append({"id": 0, "message": "Additional fortune added at request time."})
    fortunes.sort(key=itemgetter("message"))

    return render(request, "fortunes.html", {"fortunes": fortunes})


async def update_async(request):
    queries = await _get_queries_async(request)

    async def caller(input_):
        w = await World.objects.aget(id=_random_int())
        w.randomnumber = _random_int()
        await w.asave()
        return {"id": w.pk, "randomNumber": w.randomnumber}

    worlds = [await caller(_) for _ in range(queries)]

    # worlds = tuple(map(await caller, range(queries)))

    return HttpResponse(dumps(worlds), content_type="application/json")


async def sse_async(request):
    async def event_stream():
        i = 0
        while True:
            yield f"data: hello {i}\n"
            i += 1
            await asyncio.sleep(1)

    return StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream",
    )


# ASGI Chat Views
def chat_index(request):
    return render(request, "chat_index.html")


def chat_room(request, room_name: str):
    return render(request, "chat_room.html", {"room_name": room_name})


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code: int):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None):
        if not text_data:
            return
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_type = text_data_json["type"]
        t = text_data_json["t"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": message_type, "message": message, "t": t},
        )

    # Receive message from room group
    async def chat_message(self, event: dict):
        message = event["message"]
        message_type = event["type"]
        t = event["t"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"type": message_type, "message": message, "t": t}))


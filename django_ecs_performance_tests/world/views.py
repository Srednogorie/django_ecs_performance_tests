import random
from functools import partial
from operator import itemgetter

from django.views import View
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from orjson import dumps

from world.models import Fortune, World
import time
import asyncio

_random_int = partial(random.randint, 1, 10000)


class TextViewAsync(View):
    async def get(self, request):
        return HttpResponse("Hello, World!", content_type="text/plain")


# Ultra-minimal endpoint for baseline testing
async def async_json(request):
    await asyncio.sleep(0.5)
    return HttpResponse(
        dumps({"message": "Hello, World!"}), content_type="application/json",
    )


def _get_queries(request):
    try:
        queries = int(request.GET.get("queries", 1))
    except Exception:
        queries = 1
    queries = max(queries, 1)
    return min(queries, 500)


def plaintext(request):
    return StreamingHttpResponse("Hello, World!", content_type="text/plain")


def json(request):
    time.sleep(0.5)
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

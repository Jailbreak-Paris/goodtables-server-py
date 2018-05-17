# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from aiohttp import web
from functools import partial
from goodtables import Inspector
from importlib import import_module


# Module API

class Handler(object):

    # Public

    def __init__(self, inspector=None):
        if inspector is not None:
            module, name = inspector.rsplit('.', 1)
            inspector = getattr(import_module(module), name)
        else:
            inspector = Inspector()
        self.__inspector = inspector

    async def handle_GET(self, req):
        options = {
            key: value
            for key, value in req.query.items()
            if value
        }
        if "source" not in options:
            return web.json_response({"error": "Missing 'source' parameter"}, status=400)
        options['preset'] = 'table'
        options['scheme'] = 'http'
        inspect = partial(self.__inspector.inspect, **options)
        report = await req.app.loop.run_in_executor(req.app['executor'], inspect)
        return web.json_response(report)

    async def handle_POST(self, req):
        data = await req.post()
        if "source" not in data:
            return web.json_response({"error": "Missing 'source' parameter"}, status=400)
        encoding = data.get("encoding", "utf-8")
        options = {
            "encoding": encoding,
            "format": "csv",
            'preset': 'table',
            'scheme': 'text',
            "source": data["source"].file.read().decode(encoding),
        }
        schema = data.get("schema")
        if schema is not None:
            options["schema"] = data["schema"]
        inspect = partial(self.__inspector.inspect, **options)
        report = await req.app.loop.run_in_executor(req.app['executor'], inspect)
        return web.json_response(report)

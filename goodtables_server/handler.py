# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
from functools import partial
from importlib import import_module
from io import BytesIO

from aiohttp import web

import tabulator.helpers
from goodtables import Inspector

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
        if options.get("encoding") is None:
            options["encoding"] = "utf-8"
        inspect = partial(self.__inspector.inspect, **options)
        report = await req.app.loop.run_in_executor(req.app['executor'], inspect)
        return web.json_response(report, dumps=json_dumps)

    async def handle_POST(self, req):
        data = await req.post()
        if "source" not in data:
            return web.json_response({"error": "Missing 'source' parameter"}, status=400)
        encoding = data.get("encoding", "utf-8")
        _, format = tabulator.helpers.detect_scheme_and_format(data["source"].filename)
        options = {
            "format": format,
            'scheme': 'stream',
            "source": BytesIO(data["source"].file.read()),
        }
        schema = data.get("schema")
        if schema is not None:
            options["schema"] = data["schema"]
        inspect = partial(self.__inspector.inspect, **options)
        report = await req.app.loop.run_in_executor(req.app['executor'], inspect)
        return web.json_response(report, dumps=json_dumps)


def json_dumps(data):
    return json.dumps(data, default=str)

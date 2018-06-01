from concurrent.futures import ProcessPoolExecutor

import aiohttp_cors
from aiohttp import web

from .handler import Handler


def create_app(path='/', inspector=None):
    handler = Handler(inspector)
    app = web.Application()
    app['executor'] = ProcessPoolExecutor()
    cors = aiohttp_cors.setup(app)
    cors_options = {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
        )
    }
    cors.add(
        app.router.add_route('GET', path, handler.handle_GET),
        cors_options,
    )
    cors.add(
        app.router.add_route('POST', path, handler.handle_POST),
        cors_options,
    )
    return app

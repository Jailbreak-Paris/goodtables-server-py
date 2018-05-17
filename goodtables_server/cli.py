# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import click
import logging
from aiohttp import web
import aiohttp_cors
from concurrent.futures import ProcessPoolExecutor
from .handler import Handler


# Module API

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


@click.command()
@click.option('--host', default='localhost')
@click.option('--port', default=5000)
@click.option('--path', default='/')
@click.option('--inspector', default=None)
def cli(host, port, path, inspector):
    logging.basicConfig(level=logging.DEBUG)
    app = create_app(path=path, inspector=inspector)
    web.run_app(app, host=host, port=port)


# Main program

if __name__ == '__main__':
    cli()

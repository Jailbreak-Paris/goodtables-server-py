# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

import click
from aiohttp import web

from .app import create_app

# Module API


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

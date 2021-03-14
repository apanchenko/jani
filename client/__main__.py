""" Entry point """

import logging

from .container import Container
from .service import channel_offset


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
        level=logging.INFO)

    container = Container()
    container.init_resources()
    container.wire(modules=[channel_offset])

    from .jani import run
    run()
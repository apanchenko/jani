import os
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

import jani

# logging.basicConfig(
#     format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
#     level=logging.INFO)

# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    traces_sample_rate=1.0,
    integrations=[sentry_logging]
)

if __name__ == "__main__":
    jani.run()
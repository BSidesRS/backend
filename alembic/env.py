import os
import sys

import bsidesrs.app
from bsidesrs.config import getConfig
from alembic import context
from freenit.migration import run_migrations_offline, run_migrations_online


sys.path.append(os.getcwd())
config = getConfig()


if context.is_offline_mode():
    run_migrations_offline(config)
else:
    run_migrations_online(config)

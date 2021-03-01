from DB.pgsql_conn import pgsql_conn
from DB.pgsql_requests import test_connect

import asyncio

print(asyncio.get_event_loop().run_until_complete(pgsql_conn(test_connect())))

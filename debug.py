import datetime
from pprint import pprint


pprint(datetime.datetime.now())
pprint(datetime.datetime.fromisoformat("2021-07-17 21:58:21.093162"))
pprint(datetime.datetime.now() + datetime.timedelta(minutes=10))

if datetime.datetime.now() < datetime.datetime.now() + datetime.timedelta(minutes=10):
    pprint(True)
else:
    pprint(False)

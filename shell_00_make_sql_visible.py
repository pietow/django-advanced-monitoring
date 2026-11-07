from django.db import connection
from django.test.utils import CaptureQueriesContext
from monitoring.models import Station

with CaptureQueriesContext(connection) as ctx:
    qs = Station.objects.all() # lazy eval
    result = list(qs) # DB Abfrage
    # print(qs)

print(len(ctx.captured_queries))            # 1
print(ctx.captured_queries[-1]["sql"])      # ... FROM "monitoring_station"

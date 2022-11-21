import requests
import csv
from contextlib import closing

csvurl = "CHANGEME"

content = {
    "PostgreSQL": [],
    "MySQL": [],
    "Redis": [],
    "Apache Kafka": [],
    "OpenSearch": [],
    "Service": [],
    "": [],
}
with closing(requests.get(csvurl, stream=True, allow_redirects=True)) as r:
    f = (line.decode('utf-8') for line in r.iter_lines())
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        content[row[0]].append(row)

for svc in content:
    if svc == "Service" or svc == "":
        continue
    print(svc)
    r = content[svc]
    for row in r:
        print(f"{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[8]},{row[9]}")
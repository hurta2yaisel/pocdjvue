import requests
import json
from rest_framework.response import Response


def elastic_result(self, request):
    path = request.META['PATH_INFO'].partition("catalog")[2]
    fullpath = 'http://db.local:9200' + path

    # if "?" not in fullpath:
    #     fullpath += "?" + request.META['QUERY_STRING']
    requestdata = {}
    try:
        requestdata = json.loads(request.body)
    except Exception as e:
        pass

    if request.method == "POST":
        r = requests.post(fullpath, json=requestdata)

    if request.method == "GET":
        if requestdata:
            r = requests.get(fullpath, json=requestdata)
        else:
            r = requests.get(fullpath)

    items = r.json()
    return Response(items)

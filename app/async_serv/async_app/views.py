import json
import time
import random
import requests
from concurrent import futures
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


executor = futures.ThreadPoolExecutor(max_workers=1)
global cnt
cnt = 0
ServerToken = "abahjsvbdwekvnva"
url = "http://192.168.0.106:8080/monitoring-requests/user-payment-finish"
headers = {"Server-Token":"abahjsvbdwekvnva"}


def get_receipt(req_body):
    global cnt
    cnt += 1
    time.sleep(5)
    req_body['Receipt'] = f"Номер чека: {cnt}, Номер заявки:{req_body['requestId']}, Дата:{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}"
    return req_body

def status_callback(task):
    try:
      result = task.result()
      print(result)
    except futures._base.CancelledError:
      return
    requests.put(url, data=json.dumps(result), timeout=3,headers=headers)

@api_view(['Put'])
def addPayment(request):
    if request.headers.get("Server-Token") == ServerToken:
        req_body = json.loads(request.body)
        task = executor.submit(get_receipt, req_body)
        task.add_done_callback(status_callback)        
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)



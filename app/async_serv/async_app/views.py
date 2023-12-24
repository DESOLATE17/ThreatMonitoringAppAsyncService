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
url = "http://192.168.160.12:8080/monitoring-requests/user-payment-finish"


def probability_function():
    if random.random() < 0.8:
        return "успешно"
    else:
        return "отклонено"

def get_receipt(req_body):
    global cnt
    cnt += 1
    time.sleep(5)
    req_body['receipt'] = f"Статус: {probability_function()}  Номер чека: {cnt}, Номер заявки:{req_body['requestId']}, Дата:{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}"
    return req_body

def status_callback(task):
    try:
      result = task.result()
      print(result)
    except futures._base.CancelledError:
      return
    requests.put(url, data=json.dumps(result), timeout=3)

@api_view(['Put'])
def addPayment(request):
    req_body = json.loads(request.body)
    if req_body["Server-Token"] == ServerToken:
        task = executor.submit(get_receipt, req_body)
        task.add_done_callback(status_callback)        
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)



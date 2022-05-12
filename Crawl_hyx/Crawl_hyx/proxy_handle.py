import json
import requests


def get_proxy():
    # response = requests.get("http://192.168.31.230:5010/get/").text
    # result = json.loads(response)
    # # print(result, type(result))
    # return result['proxy']
    # 5010：settings中设置的监听端口，不是Redis服务的端口
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


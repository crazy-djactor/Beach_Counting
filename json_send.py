
import requests
import base64
import json
import sys


def make_request_json(ip_addr, img_file, count=0):

    file_data = open(img_file, 'rb')

    json_data = {
        "type": 'post',
        "ip": ip_addr,
        "image": base64.b64encode(file_data.read()).decode('UTF-8'),
        "count": count
    }

    return json_data


def send_request(server, req_json):

    response = requests.post(url=server, json=req_json)
    print("Server responded with %s" % response.status_code)

    response_json = response.json()
    return response_json


if __name__ == '__main__':

    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = '../samples/Aguete/IMG_2656.jpeg'

    # url_server = 'http://localhost:3000/beach_analysis/v1.0'
    url_server = 'http://13.93.78.173:3000/beach_analysis/v1.0'

    json_request = make_request_json(ip_addr='192.168.1.122', img_file=filename, count=10)
    ret_response = send_request(url_server, json_request)

    print(json.dumps(ret_response, indent=4))

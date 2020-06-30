
import requests
import base64
import json
import sys


def make_request_json(ip_addr, img_file, cam_name, count=0):

    # file_data = open(img_file, 'rb')

    json_data = {
        "type": 'post',
        "ip": ip_addr,
        # "image": base64.b64encode(file_data.read()).decode('UTF-8'),
        "count": count,
        "cam_name": cam_name
    }

    return json_data


def send_request(server, cam_name, req_json):
    try:
        post_url = server+cam_name
        response = requests.post(url=post_url, json=req_json)
        print("Server responded with %s" % response.status_code)
        response_json = response.json()
        return response_json
    except:
        return None


if __name__ == '__main__':

    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = '../samples/Aguete/IMG_2656.jpeg'

    url_server = 'http://localhost:3000/ap1/v1/zonecam/'
    # url_server = 'http://13.93.78.173:3000/beach_analysis/v1.0'

    json_request = make_request_json(ip_addr='192.168.1.122', img_file=filename, cam_name='B01Z01', count=10)
    ret_response = send_request(server=url_server, cam_name='B01Z01', req_json=json_request)

    print(json.dumps(ret_response, indent=4))

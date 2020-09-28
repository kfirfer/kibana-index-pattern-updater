# -*- coding: utf-8 -*-
import requests
import base64

from src import KUBERNETES_HOST, KUBERNETES_TOKEN, KIBANA_HOST, KIBANA_USERNAME, KIBANA_PASSWORD

KIBANA_AUTH = "{}:{}".format(KIBANA_USERNAME, KIBANA_PASSWORD)
message_bytes = KIBANA_AUTH.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
KIBANA_AUTH = base64_bytes.decode('ascii')


def get_namespaces():
    url = "{}/api/v1/namespaces".format(KUBERNETES_HOST)
    headers = {
        'authorization': 'Bearer {}'.format(KUBERNETES_TOKEN)
    }
    response = requests.request("GET", url, headers=headers, verify=False, timeout=60).json()
    return response


def create_index_patterns(namespace):
    print("Creating index pattern: {}".format(namespace))
    url = "{}/api/saved_objects/index-pattern/logstash-{}-*".format(KIBANA_HOST, namespace)
    payload = {
        "attributes": {
            "title": "logstash-{}-*".format(namespace),
            "timeFieldName": "@timestamp"
        }
    }
    headers = {
        'kbn-xsrf': 'anything',
        'Authorization': 'Basic {}'.format(KIBANA_AUTH),
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, json=payload, timeout=60)
    print(response.text.encode('utf8'))


def is_index_pattern_exists(namespace):
    url = "{}/api/saved_objects/index-pattern/logstash-{}-*".format(KIBANA_HOST, namespace)
    headers = {
        'kbn-xsrf': 'anything',
        'Authorization': 'Basic {}'.format(KIBANA_AUTH)
    }
    response = requests.request("GET", url, headers=headers, timeout=60)
    if response.status_code == 404:
        return False
    return True


def job():
    namespaces = get_namespaces()
    for item in namespaces["items"]:
        name = item["metadata"]["name"]
        index_pattern_exists = is_index_pattern_exists(name)
        if index_pattern_exists is False:
            create_index_patterns(name)

# -*- coding: utf-8 -*-
import base64
import os
import random
import string

import requests
from kubernetes import client, config

from src import KIBANA_HOST, KIBANA_USERNAME, KIBANA_PASSWORD, LOAD_KUBECONFIG, LOAD_INCLUSTER_CONFIG, \
    ELASTICSEARCH_HOST, DOMAIN, ES_VERSION
from src.loggings.logger import logger

KIBANA_AUTH = "{}:{}".format(KIBANA_USERNAME, KIBANA_PASSWORD)
message_bytes = KIBANA_AUTH.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
KIBANA_AUTH = base64_bytes.decode('ascii')
log = logger(__name__)
exclude_namespaces_set = set()

if 'EXCLUDE_NAMESPACES' in os.environ and os.environ["EXCLUDE_NAMESPACES"] != "":
    EXCLUDE_NAMESPACES = os.environ['EXCLUDE_NAMESPACES']
    exclude_namespaces_set = set(EXCLUDE_NAMESPACES.split(","))


def get_namespaces():
    if LOAD_KUBECONFIG == "1":
        config.load_kube_config()
    if LOAD_INCLUSTER_CONFIG == "1":
        config.load_incluster_config()
    v1 = client.CoreV1Api()
    namespaces = v1.list_namespace(watch=False)
    return namespaces


def create_index_patterns(namespace):
    log.info("Creating index pattern: {}".format(namespace))
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
    log.info("", extra={"props": {"response": response.text}})


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


def create_space(namespace):
    url = "{}/api/spaces/space".format(KIBANA_HOST)
    payload = {
        "id": namespace,
        "name": namespace,
        "disabledFeatures": [
            "timelion",
            "dev_tools",
            "enterpriseSearch",
            "logs",
            "siem",
            "advancedSettings",
            "monitoring",
            "stackAlerts",
            "actions",
            "ingestManager",
            "ml",
            "infrastructure",
            "apm",
            "uptime"
        ]
    }
    headers = {
        'kbn-xsrf': 'anything',
        'Authorization': 'Basic {}'.format(KIBANA_AUTH)
    }
    response = requests.request("POST", url, headers=headers, json=payload, timeout=60, verify=False)
    log.info("", extra={"props": {"response": response.text}})


def create_role(namespace):
    url = "{}/api/security/role/{}".format(KIBANA_HOST, namespace)
    payload = {
        "metadata": {
            "version": 1
        },
        "elasticsearch": {
            "cluster": [],
            "indices": [
                {
                    "names": [
                        "logstash-{}-*".format(namespace)
                    ],
                    "privileges": [
                        "read"
                    ]
                }
            ]
        },
        "kibana": [
            {
                "base": [],
                "feature": {
                    "dashboard": [
                        "all"
                    ],
                    "discover": [
                        "all"
                    ],
                    "canvas": [
                        "all"
                    ],
                    "maps": [
                        "all"
                    ],
                    "visualize": [
                        "all"
                    ],
                    "savedObjectsManagement": [
                        "read"
                    ]
                },
                "spaces": [
                    namespace
                ]
            }
        ]
    }
    headers = {
        'kbn-xsrf': 'anything',
        'Authorization': 'Basic {}'.format(KIBANA_AUTH)
    }
    response = requests.request("PUT", url, headers=headers, json=payload, timeout=60, verify=False)
    log.info("", extra={"props": {"response": response.text}})


def create_user(namespace):
    url = "{}/_security/user/{}".format(ELASTICSEARCH_HOST, namespace)
    password = random_string()

    payload = {
        "password": password,
        "roles": [namespace],
        "full_name": namespace,
        "email": "{}@{}".format(namespace, DOMAIN),
        "metadata": {}
    }
    headers = {
        'kbn-xsrf': 'anything',
        'Authorization': 'Basic {}'.format(KIBANA_AUTH)
    }
    response = requests.request("POST", url, headers=headers, json=payload, timeout=60, verify=False)
    log.info("", extra={"props": {"response": response.text}})
    log.info("", extra={"props": {"username": namespace, "password": password}})


def create_space_index_pattern(namespace):
    url = "{}/s/{}/api/saved_objects/index-pattern/logstash-{}-*".format(KIBANA_HOST, namespace, namespace)
    payload = {
        "attributes": {
            "title": "logstash-{}-*".format(namespace),
            "timeFieldName": "@timestamp"
        }
    }
    headers = {
        'kbn-xsrf': 'anything',
        'Authorization': 'Basic {}'.format(KIBANA_AUTH)
    }
    response = requests.request("POST", url, headers=headers, json=payload, timeout=60, verify=False)
    log.info("", extra={"props": {"response": response.text}})


def random_string(size=20):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def config_space_default_index_pattern(namespace):
    url = "{}/s/{}/spaces/enter".format(KIBANA_HOST, namespace)
    headers = {
        'kbn-xsrf': 'anything',
        'Authorization': 'Basic {}'.format(KIBANA_AUTH)
    }
    requests.request("GET", url, headers=headers, timeout=60, verify=False)

    payload = {
        "attributes": {
            "defaultIndex": "logstash-{}-*".format(namespace)
        }
    }
    url = "{}/s/{}/api/saved_objects/config/{}".format(KIBANA_HOST, namespace, ES_VERSION)
    response = requests.request("PUT", url, headers=headers, json=payload, timeout=60, verify=False)
    log.info("", extra={"props": {"response": response.text}})


def job():
    namespaces = get_namespaces()
    for item in namespaces.items:
        namespace = item.metadata.name
        index_pattern_exists = is_index_pattern_exists(namespace)
        if index_pattern_exists is False:
            create_index_patterns(namespace)
            if namespace in exclude_namespaces_set:
                continue
            create_space(namespace)
            create_role(namespace)
            create_user(namespace)
            create_space_index_pattern(namespace)
            config_space_default_index_pattern(namespace)

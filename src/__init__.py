# -*- coding: utf-8 -*-
import os

os.environ["ELASTICSEARCH_HOST"] = os.getenv("ELASTICSEARCH_HOST", "https://127.0.0.1:9200")
os.environ["KIBANA_HOST"] = os.getenv("KIBANA_HOST", "https://127.0.0.1:5601")
os.environ["KIBANA_USERNAME"] = os.getenv("KIBANA_USERNAME", "admin")
os.environ["KIBANA_PASSWORD"] = os.getenv("KIBANA_PASSWORD", "admin")
os.environ["LOAD_KUBECONFIG"] = os.getenv("LOAD_KUBECONFIG", "1")
os.environ["LOAD_INCLUSTER_CONFIG"] = os.getenv("LOAD_INCLUSTER_CONFIG", "0")
os.environ["DOMAIN"] = os.getenv("DOMAIN", "example.com")
os.environ["JSON_LOG_CONSOLE"] = os.getenv("JSON_LOG_CONSOLE", "0")
os.environ["LOG_TO_CONSOLE"] = os.getenv("LOG_TO_CONSOLE", "1")
os.environ["LOGGER_LEVEL"] = os.getenv("LOGGER_LEVEL", "debug")
os.environ["ES_VERSION"] = os.getenv("ES_VERSION", "7.10.2")
os.environ["EXCLUDE_NAMESPACES"] = os.getenv("EXCLUDE_NAMESPACES", "kube-system,kube-public")

ELASTICSEARCH_HOST = os.environ["ELASTICSEARCH_HOST"]
KIBANA_HOST = os.environ["KIBANA_HOST"]
KIBANA_USERNAME = os.environ["KIBANA_USERNAME"]
KIBANA_PASSWORD = os.environ["KIBANA_PASSWORD"]
LOAD_KUBECONFIG = os.environ["LOAD_KUBECONFIG"]
LOAD_INCLUSTER_CONFIG = os.environ["LOAD_INCLUSTER_CONFIG"]
DOMAIN = os.environ["DOMAIN"]
ES_VERSION = os.environ["ES_VERSION"]

# -*- coding: utf-8 -*-
import os

os.environ["KIBANA_HOST"] = os.getenv("KIBANA_HOST", "127.0.0.1")
os.environ["KIBANA_USERNAME"] = os.getenv("KIBANA_USERNAME", "admin")
os.environ["KIBANA_PASSWORD"] = os.getenv("KIBANA_PASSWORD", "admin")
os.environ["LOAD_KUBECONFIG"] = os.getenv("LOAD_KUBECONFIG", "0")
os.environ["LOAD_INCLUSTER_CONFIG"] = os.getenv("LOAD_INCLUSTER_CONFIG", "0")

KIBANA_HOST = os.environ["KIBANA_HOST"]
KIBANA_USERNAME = os.environ["KIBANA_USERNAME"]
KIBANA_PASSWORD = os.environ["KIBANA_PASSWORD"]
LOAD_KUBECONFIG = os.environ["LOAD_KUBECONFIG"]
LOAD_INCLUSTER_CONFIG = os.environ["LOAD_INCLUSTER_CONFIG"]

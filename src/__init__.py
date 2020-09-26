# -*- coding: utf-8 -*-
import os

os.environ["KUBERNETES_HOST"] = os.getenv("KUBERNETES_HOST", "127.0.0.1")
os.environ["KUBERNETES_TOKEN"] = os.getenv("KUBERNETES_TOKEN", "token")
os.environ["KIBANA_HOST"] = os.getenv("KIBANA_HOST", "127.0.0.1")
os.environ["KIBANA_USERNAME"] = os.getenv("KIBANA_USERNAME", "admin")
os.environ["KIBANA_PASSWORD"] = os.getenv("KIBANA_PASSWORD", "admin")

KUBERNETES_HOST = os.environ["KUBERNETES_HOST"]
KUBERNETES_TOKEN = os.environ["KUBERNETES_TOKEN"]
KIBANA_HOST = os.environ["KIBANA_HOST"]
KIBANA_USERNAME = os.environ["KIBANA_USERNAME"]
KIBANA_PASSWORD = os.environ["KIBANA_PASSWORD"]

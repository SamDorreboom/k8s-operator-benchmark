import yaml

def make_deployment(name, label, image):
    return yaml.safe_load(f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {label}
  template:
    metadata:
      labels:
        app: {label}
    spec:
      imagePullSecrets:
      - name: gitlab-registry
      containers:
      - name: {label}
        image: "{image}"
""")

def get_deploymail():
    return make_deployment("mail-deployment", "mail-deployment", "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/mail:1.7.0")

def get_deployweb():
    return make_deployment("web-deployment", "web-deployment", "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/web:1.7.0")

def get_deploysms():
    return make_deployment("sms-deployment", "sms-deployment", "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/sms:1.7.0")

def get_deploystorage():
    return make_deployment("storage-deployment", "storage-deployment", "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/storage:1.7.0")

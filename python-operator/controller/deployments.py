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

def get_deploymail(naam):
    return make_deployment(f"mail-deployment-{naam}", f"mail-deployment-{naam}", "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/mail:1.7.0")

def get_deployweb(naam):
    return make_deployment(f"web-deployment-{naam}", f"web-deployment-{naam}", "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/web:1.7.0")

def get_deploysms(naam):
    return make_deployment(f"sms-deployment-{naam}", f"sms-deployment-{naam}", "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/sms:1.7.0")

def get_deploystorage(naam):
    return make_deployment(f"storage-deployment-{naam}", f"storage-deployment-{naam}", "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/storage:1.7.0")

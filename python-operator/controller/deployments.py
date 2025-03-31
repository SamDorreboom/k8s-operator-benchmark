import yaml

def get_deploysms(spec, name, **kwargs):

    depl = yaml.safe_load(f"""
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: 
        spec:
          replicas: 1
          template:
            metadata:
              labels:
                app: "mail-deploy"
            spec:
              imagePullSecrets:
                name: gitlab-registry
              containers:
              - name: mail
                image: "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/sms:1.7.0"
                            
    """)
    return depl

def get_deployweb(spec, name, **kwargs):

    depl = yaml.safe_load(f"""
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: 
        spec:
          replicas: 1
          template:
            metadata:
              labels:
                app: securedropzone-web
            spec:
              imagePullSecrets:
                name: gitlab-registry
              containers:
              - name: mail
                image: "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/web:1.7.0"
                            
    """)
    return depl

def get_deploystorage(spec, name, **kwargs):

    depl = yaml.safe_load(f"""
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: 
        spec:
          replicas: 1
          template:
            metadata:
              labels:
                app: "mail-deploy"
            spec:
              imagePullSecrets:
                name: gitlab-registry
              containers:
              - name: mail
                image: "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/storage:1.7.0"
                            
    """)
    return depl

def get_deploymail(spec, name, **kwargs):

    depl = yaml.safe_load(f"""
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: 
        spec:
          replicas: 1
          template:
            metadata:
              labels:
                app: "mail-deploy"
            spec:
              imagePullSecrets:
                name: gitlab-registry
              containers:
              - name: mail
                image: "registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/mail:1.7.0"
                            
    """)
    return depl
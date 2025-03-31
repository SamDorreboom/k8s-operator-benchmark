import os
import kopf
import kubernetes
import yaml
import deployments

@kopf.on.create('securedropzone')
def create_fn(spec, namespace, logger, **kwargs):

    
    mail_depl = deployments.get_deploymail
    web_depl = deployments.get_deployweb
    sms_depl = deployments.get_deploysms
    storage_depl = deployments.get_deploystorage

    deployments = [mail_depl, web_depl, sms_depl, storage_depl]
    api = kubernetes.client.AppsV1API()
    for i in deployments:
        kopf.adopt(i)

        obj = api.create_namespaced_deployment(
            namespace="default",
            body=i,
        )
    

    api = kubernetes.client.CoreV1Api()
    mail_service = get_service("mail-deployment", "mail-service", **kwargs )
    web_service = get_service("web-deployment", "web-service", **kwargs )
    sms_service = get_service("sms-deployment", "sms-service", **kwargs )
    storage_service = get_service("storage-deployment", "storage-service", **kwargs )

    services = [mail_service, web_service, sms_service, storage_service]
    for i in services:
        kopf.adopt(i)
        obj = api.create_namespaced_service(
            namespace="default",
            body=i,
        )

    logger.info(f"Pod is aangemaakt: {obj}")


def get_service(selector, name, **kwargs):
    
    service = yaml.safe_load(f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {name}
        spec:
          selector: {selector}
        ports:
          - name: http
            protocol: TCP
            port: 8080
            targetPort: 8080        
    """)
    return service

import kopf
import kubernetes
import deployments
from service import get_service

@kopf.on.create('securedropzones', group='operators.samdorreboom.nl', version='v1alpha1')
def create_fn(spec, namespace, logger, **kwargs):
    api_apps = kubernetes.client.AppsV1Api()
    api_core = kubernetes.client.CoreV1Api()

    # Maak deployments aan
    deploy_specs = [
        deployments.get_deploymail(),
        deployments.get_deployweb(),
        deployments.get_deploysms(),
        deployments.get_deploystorage(),
    ]

    for depl in deploy_specs:
        kopf.adopt(depl)
        api_apps.create_namespaced_deployment(namespace=namespace, body=depl)

    # Maak services aan
    service_specs = [
        get_service("mail-deploy", "mail-service"),
        get_service("web-deploy", "web-service"),
        get_service("sms-deploy", "sms-service"),
        get_service("storage-deploy", "storage-service"),
    ]

    for svc in service_specs:
        kopf.adopt(svc)
        api_core.create_namespaced_service(namespace=namespace, body=svc)

    logger.info(f"Deployments en services aangemaakt in namespace: {namespace}")

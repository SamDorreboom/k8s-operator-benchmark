import kopf
import kubernetes
import deployments
from service import get_service

@kopf.on.create('securedropzones', group='operators.samdorreboom.nl', version='v1alpha1')
def create_fn(spec, namespace, logger, **kwargs):
    naam = spec.get('name')
    api_apps = kubernetes.client.AppsV1Api()
    api_core = kubernetes.client.CoreV1Api()

    # Maak deployments aan
    deploy_specs = [
        deployments.get_deploymail(naam),
        deployments.get_deployweb(naam),
        deployments.get_deploysms(naam),
        deployments.get_deploystorage(naam),
    ]

    for depl in deploy_specs:
        kopf.adopt(depl)
        api_apps.create_namespaced_deployment(namespace=namespace, body=depl)

    # Maak services aan
    service_specs = [
        get_service(f"mail-deployment-{naam}", f"mail-service-{naam}"),
        get_service(f"web-deployment-{naam}", f"web-service-{naam}"),
        get_service(f"sms-deployment-{naam}", f"sms-service-{naam}"),
        get_service(f"storage-deployment-{naam}", f"storage-service-{naam}"),
    ]

    for svc in service_specs:
        kopf.adopt(svc)
        api_core.create_namespaced_service(namespace=namespace, body=svc)

    logger.info(f"Deployments en services aangemaakt in namespace: {namespace}")




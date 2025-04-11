import kopf
import kubernetes
import deployments
from service import get_service

@kopf.on.create('securedropzones', group='operators.samdorreboom.nl', version='v1alpha1')
def create_fn(spec, namespace, logger, **kwargs):
    naam = spec.get('name')
    replicas = spec.get('replicas')
    api_apps = kubernetes.client.AppsV1Api()
    api_core = kubernetes.client.CoreV1Api()

    # Maak deployments aan
    deploy_specs = [
        deployments.get_deploymail(naam, replicas),
        deployments.get_deployweb(naam, replicas),
        deployments.get_deploysms(naam, replicas),
        deployments.get_deploystorage(naam), replicas,
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


@kopf.on.update('securedropzones', group='operators.samdorreboom.nl', version='v1alpha1')
def update_fn(spec, namespace, logger, **kwargs):
    naam = spec.get('name')
    new_replicas = spec.get('replicas')

    if not naam or new_replicas is None:
        logger.warning("Naam of replicas niet opgegeven in spec.")
        return

    logger.info(f"Nieuwe gewenste replica-aantal: {new_replicas}")

    api_apps = kubernetes.client.AppsV1Api()

    deployments_to_update = [
        f"mail-deployment-{naam}",
        f"web-deployment-{naam}",
        f"sms-deployment-{naam}",
        f"storage-deployment-{naam}",
    ]

    for deploy_name in deployments_to_update:
        try:
            # Haal huidige deployment op
            deployment = api_apps.read_namespaced_deployment(name=deploy_name, namespace=namespace)
            current_replicas = deployment.spec.replicas

            # Vergelijk met gewenste staat uit de CR
            if current_replicas != new_replicas:
                logger.info(f"Deployment '{deploy_name}' heeft {current_replicas} replicas, aanpassen naar {new_replicas}...")
                deployment.spec.replicas = new_replicas
                api_apps.patch_namespaced_deployment(name=deploy_name, namespace=namespace, body=deployment)
                logger.info(f"Deployment '{deploy_name}' aangepast.")
            else:
                logger.info(f"Deployment '{deploy_name}' had al het juiste aantal replicas ({new_replicas}). Geen wijziging nodig.")

        except kubernetes.client.exceptions.ApiException as e:
            logger.error(f"Fout bij updaten van deployment '{deploy_name}': {e}")
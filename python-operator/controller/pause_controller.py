import os
import kopf
import kubernetes
import yaml

@kopf.on.create('operatorpython')
def create_fn(spec, namespace, logger, **kwargs):

    naam = spec.get('naam')
    podNaam = 'pause' + naam
    if not naam:
        raise kopf.PermanentError(f"Naam is niet opgegeven. {naam!r}.")

    path = os.path.join(os.path.dirname(__file__), 'pause-pod.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(podNaam=podNaam)
    data = yaml.safe_load(text)

    kopf.adopt(data)

    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_pod(
        namespace=namespace,
        body=data,
    )

    logger.info(f"Pod is aangemaakt: {obj}")


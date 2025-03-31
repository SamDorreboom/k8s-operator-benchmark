
```bash
source ~/venvs/project-env/bin/activate
```

```bash
kubectl logs -l application=python-operator -n python-operator
```

```bash
docker build -t samdorreboom/k8s-operator-benchmark:python controller/
```

```bash
docker push samdorreboom/k8s-operator-benchmark:python
```

```bash
kubectl delete pods -l application=python-operator -n python-operator
```



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

C:\Users\samdo\Github\k8s-operator-benchmark\python-operator>kubectl get service -o custom-columns="NAME:.metadata.name,CREATED:.metadata.creationTimestamp"
NAME              CREATED
mail-service      2025-04-03T11:51:31Z
sms-service       2025-04-03T11:51:31Z
storage-service   2025-04-03T11:51:31Z
web-service       2025-04-03T11:51:31Z

C:\Users\samdo\Github\k8s-operator-benchmark\python-operator>kubectl get deployment -o custom-columns="NAME:.metadata.name,CREATED:.metadata.creationTimestamp"
NAME                 CREATED
mail-deployment      2025-04-03T11:51:31Z
python-operator      2025-04-02T08:44:07Z
sms-deployment       2025-04-03T11:51:31Z
storage-deployment   2025-04-03T11:51:31Z
web-deployment       2025-04-03T11:51:31Z

C:\Users\samdo\Github\k8s-operator-benchmark\python-operator>kubectl get securedropzones -o custom-columns="NAME:.metadata.name,CREATED:.metadata.creationTimestamp"
NAME                    CREATED
operatorpython-sample   2025-04-03T11:51:30Z
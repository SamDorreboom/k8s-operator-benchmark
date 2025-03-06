# Dit is de repository voor het testen van de verschillen tussen verschillende operators


## Commando's
Ophalen van controller logs
```bash
kubectl logs -l control-plane=controller-manager -n k8s-operator-benchmark-system
```

Verwijderen van de container pod:
```bash
kubectl delete pod -l control-plane=controller-manager -n k8s-operator-benchmark-system
```

Voor het aanmaken van de custom resources kan het bash script cr-generator gebruikt worden. De types: "Go", "ansible", "python"
```bash
./cr-generator.sh <aantal> <locatie> <type>
```

## Audit inschakelen in Minikube
```bash
minikube stop
```
```bash
mkdir -p ~/.minikube/files/etc/ssl/certs
```
```bash
cat <<EOF > ~/.minikube/files/etc/ssl/certs/audit-policy.yaml
# Log all requests at the Metadata level.
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
EOF
```
```bash
minikube start \
  --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml \
  --extra-config=apiserver.audit-log-path=-
```
```bash
kubectl logs kube-apiserver-minikube -n kube-system | grep audit.k8s.io/v1
```

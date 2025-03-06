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


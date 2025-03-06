#!/bin/bash

aantal=$1
locatie=$2
type=$3

# for loop voor het generen van de custom resources
for i in $(seq 1 "$aantal"); do
  cat <<EOF > "$locatie/operatorgo-$i.yaml"
apiVersion: operators.samdorreboom.nl/v1alpha1
kind: Operator$type
metadata:
  labels:
    app.kubernetes.io/name: k8s-operator-benchmark
    app.kubernetes.io/managed-by: kustomize
  name: $type-test-$i
spec:
  naam: "test-$i"
EOF
done

echo "$aantal CR YAML-bestanden gegenereerd in de map $locatie."

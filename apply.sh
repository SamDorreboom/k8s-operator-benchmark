#!/bin/bash

x=0

while [ $x -lt 100 ]
do
    kubectl apply -f /home/sam/github/k8s-operator-benchmark/python-operator/operatorpython-sample.yaml -n default
    sleep 3
    kubectl delete -f /home/sam/github/k8s-operator-benchmark/python-operator/operatorpython-sample.yaml -n default
    sleep 3
done
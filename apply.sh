#!/bin/bash

x=0
echo "Iteration, Timestamp, Securedropzone Creation Time, Deployment Creation Time, Service Creation Time" > /home/sam/github/k8s-operator-benchmark/data.csv


while [ $x -lt 10 ]
do
    kubectl apply -f /home/sam/github/k8s-operator-benchmark/python-operator/cr
    sleep 3
    echo "$x" >> data.txt
    kubectl get securedropzones -o custom-columns="NAME:.metadata.name,CREATED:.metadata.creationTimestamp" -n onderzoek >> /home/sam/github/k8s-operator-benchmark/data.txt
    kubectl get deployments -o custom-columns="NAME:.metadata.name,CREATED:.metadata.creationTimestamp" -n onderzoek >> /home/sam/github/k8s-operator-benchmark/data.txt
    kubectl get services -o custom-columns="NAME:.metadata.name,CREATED:.metadata.creationTimestamp" -n onderzoek >> /home/sam/github/k8s-operator-benchmark/data.txt


    kubectl delete -f /home/sam/github/k8s-operator-benchmark/python-operator/cr
    sleep 5
    x=$(( $x + 1 ))
done
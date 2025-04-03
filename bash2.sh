#!/bin/bash

x=0

# Maak een lege data.csv file voor gestructureerde data
echo "Iteration, Timestamp, Securedropzone Creation Time, Deployment Creation Time, Service Creation Time" > /home/sam/github/k8s-operator-benchmark/data.csv

# Lijst van CR-bestanden (verondersteld dat alle CR-bestanden in de map staan)
cr_files="/home/sam/github/k8s-operator-benchmark/python-operator/cr/*"

while [ $x -lt 10 ]
do
    echo "Iteration $x - $(date)"

    # Upload alle CR's tegelijk
    kubectl apply -f /home/sam/github/k8s-operator-benchmark/python-operator/cr/
    sleep 3  # Wacht 3 seconden voor initialisatie

    # Wacht totdat de resource aangemaakt is
    until kubectl get securedropzones -n onderzoek --no-headers | grep -q <securedropzone-name>; do
        sleep 1
    done

    # Verzamel de creationTimestamp van resources
    securedropzone_creation_time=$(kubectl get securedropzones -o custom-columns="CREATED:.metadata.creationTimestamp" -n onderzoek)

    # Wacht tot Deployment is aangemaakt
    until kubectl get deployments -n onderzoek --no-headers | grep -q <deployment-name>; do
        sleep 1
    done

    # Verzamel de creationTimestamp voor Deployment
    deployment_creation_time=$(kubectl get deployments -o custom-columns="CREATED:.metadata.creationTimestamp" -n onderzoek)

    # Wacht tot Service is aangemaakt
    until kubectl get services -n onderzoek --no-headers | grep -q <service-name>; do
        sleep 1
    done

    # Verzamel de creationTimestamp voor Service
    service_creation_time=$(kubectl get services -o custom-columns="CREATED:.metadata.creationTimestamp" -n onderzoek)

    # Log de resultaten in CSV-formaat
    echo "$x, $(date), $securedropzone_creation_time, $deployment_creation_time, $service_creation_time" >> /home/sam/github/k8s-operator-benchmark/data.csv

    # Verwijder alle CR's tegelijk
    kubectl delete -f /home/sam/github/k8s-operator-benchmark/python-operator/cr/
    sleep 5  # Wacht tot CR is verwijderd

    x=$(( $x + 1 ))
done

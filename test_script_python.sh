#!/bin/bash

# Herhaal de test 5 keer
for i in {1..5}; do
    echo "Iteratie $i - Start time: $(date)" > timeresults/time$i.txt

    # Fase A: CR's aanmaken
    echo "Iteratie $i - Fase: Aanmaken - $(date)" >> timeresults/time$i.txt
    kubectl apply -f python/aanmaken
    # Indien nodig, wacht even voordat je de status controleert
    sleep 7
    kubectl get deployments,services,securedropzone -n onderzoek \
        -o custom-columns=NAME:.metadata.name,CREATIONTIME:.metadata.creationTimestamp \
        --sort-by=.metadata.creationTimestamp >> timeresults/time$i.txt

    # Fase B: Direct wijzigen
    echo "Iteratie $i - Fase: Wijzigen - $(date)" >> timeresults/time$i.txt
    update_start=$(date +%s)
    echo "Iteratie $i - Update start: $(date)" >> timeresults/time$i.txt
    kubectl apply -f python/wijzigen

    # Poll op update: wacht tot deployment update klaar is
    while [ $(kubectl get deployment -o custom-columns=REPLICAS:.spec.replicas -n onderzoek --no-headers=true | grep 1 | wc -l) -gt 0 ]; do
        sleep 0.1
    done
    echo "Iteratie $i - All updated: $(date)" >> timeresults/time$i.txt

    # Kleine pauze voor stabiliteit
    sleep 5

    # Fase C: Verwijderen
    echo "Iteratie $i - Fase: Verwijderen - $(date)" >> timeresults/time$i.txt
    kubectl delete -f python/aanmaken

    # Poll tot alle resources verwijderd zijn
    while [ $(kubectl get all -n onderzoek --no-headers | wc -l) -gt 0 ]; do
        sleep 0.1
    done
    echo "Iteratie $i - Alle resources verwijderd: $(date)" >> timeresults/time$i.txt
    sleep 30
done



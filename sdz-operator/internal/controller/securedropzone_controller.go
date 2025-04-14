/*
Copyright 2025.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
	"context"
	"fmt"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/log"

	//corev1 "k8s.io/api/core/v1"
	//appsv1 "k8s.io/api/apps/v1"
	securedropzonev1 "gitlab.warpnet.nl/securedropzone/sdz-operator/api/v1"
)

// SecureDropzoneReconciler reconciles a SecureDropzone object
type SecureDropzoneReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=securedropzone.securedropzone.nl,resources=securedropzones,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=securedropzone.securedropzone.nl,resources=securedropzones/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=securedropzone.securedropzone.nl,resources=securedropzones/finalizers,verbs=update

// +kubebuilder:rbac:groups="",resources=services,verbs=list;create;watch;update;patch;delete
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=list;create;watch;update;patch;delete

// Reconcile is part of the main kubernetes reconciliation loop which aims to
// move the current state of the cluster closer to the desired state.
// TODO(user): Modify the Reconcile function to compare the state specified by
// the SecureDropzone object against the actual cluster state, and then
// perform operations to make the cluster state reflect the state specified by
// the user.
//
// For more details, check Reconcile and its Result here:
// - https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.19.0/pkg/reconcile
func (r *SecureDropzoneReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	log := log.FromContext(ctx)

	sdz := &securedropzonev1.SecureDropzone{}

	// Checks voor het ophalen van de securedropzone resource
	if err := r.Get(ctx, req.NamespacedName, sdz); err != nil {
		if errors.IsNotFound(err) {
			log.Info("Can't find SecureDropzone resource")
			return ctrl.Result{}, nil
		}
		log.Error(err, "Error with getting CR SecureDropzone")
		return ctrl.Result{}, err
	}

	name := sdz.Spec.Name
	replicas := int32(sdz.Spec.Replicas)

	deployments := []appsv1.Deployment{
		newDeployment(fmt.Sprintf("mail-deployment-%s", name), replicas, fmt.Sprintf("mail-deployment-%s", name),
			"registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/mail:1.7.0"),
		newDeployment(fmt.Sprintf("web-deployment-%s", name), replicas, fmt.Sprintf("web-deployment-%s", name),
			"registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/web:1.7.0"),
		newDeployment(fmt.Sprintf("sms-deployment-%s", name), replicas, fmt.Sprintf("sms-deployment-%s", name),
			"registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/sms:1.7.0"),
		newDeployment(fmt.Sprintf("storage-deployment-%s", name), replicas, fmt.Sprintf("storage-deployment-%s", name),
			"registry.gitlab.warpnet.nl/securedropzone/securedropzone-e2ee/storage:1.7.0"),
	}

	for _, dep := range deployments {
		// Stel owner reference in voor garbage collection
		if err := controllerutil.SetControllerReference(sdz, &dep, r.Scheme); err != nil {
			log.Error(err, "unable to set owner reference", "Deployment", dep.Name)
			return ctrl.Result{}, err
		}

		var existingDep appsv1.Deployment
		err := r.Get(ctx, client.ObjectKey{Namespace: req.Namespace, Name: dep.Name}, &existingDep)
		if err != nil {
			if errors.IsNotFound(err) {
				// Deployment bestaat niet; maak deze aan
				if err := r.Create(ctx, &dep); err != nil {
					log.Error(err, "failed to create Deployment", "Deployment", dep.Name)
					return ctrl.Result{}, err
				}
				log.Info("Created Deployment", "Deployment", dep.Name)
			} else {
				return ctrl.Result{}, err
			}
		} else {
			// Deployment bestaat: update het aantal replicas indien nodig
			if existingDep.Spec.Replicas != nil && *existingDep.Spec.Replicas != replicas {
				log.Info("Updating Deployment replica count",
					"Deployment", dep.Name,
					"currentReplicas", *existingDep.Spec.Replicas,
					"desiredReplicas", replicas)
				existingDep.Spec.Replicas = &replicas
				if err := r.Update(ctx, &existingDep); err != nil {
					log.Error(err, "failed to update Deployment", "Deployment", dep.Name)
					return ctrl.Result{}, err
				}
			}
		}
	}

	// Maak een lijst van gewenste services
	services := []corev1.Service{
		newService(fmt.Sprintf("mail-deployment-%s", name), fmt.Sprintf("mail-service-%s", name)),
		newService(fmt.Sprintf("web-deployment-%s", name), fmt.Sprintf("web-service-%s", name)),
		newService(fmt.Sprintf("sms-deployment-%s", name), fmt.Sprintf("sms-service-%s", name)),
		newService(fmt.Sprintf("storage-deployment-%s", name), fmt.Sprintf("storage-service-%s", name)),
	}

	// Creëer services indien zij niet bestaan
	for _, svc := range services {
		if err := controllerutil.SetControllerReference(sdz, &svc, r.Scheme); err != nil {
			log.Error(err, "unable to set owner reference", "Service", svc.Name)
			return ctrl.Result{}, err
		}

		var existingSvc corev1.Service
		err := r.Get(ctx, client.ObjectKey{Namespace: req.Namespace, Name: svc.Name}, &existingSvc)
		if err != nil {
			if errors.IsNotFound(err) {
				if err := r.Create(ctx, &svc); err != nil {
					log.Error(err, "failed to create Service", "Service", svc.Name)
					return ctrl.Result{}, err
				}
				log.Info("Created Service", "Service", svc.Name)
			} else {
				return ctrl.Result{}, err
			}
		}
	}

	return ctrl.Result{}, nil
}

// SetupWithManager sets up the controller with the Manager.
func (r *SecureDropzoneReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&securedropzonev1.SecureDropzone{}).
		Complete(r)
}

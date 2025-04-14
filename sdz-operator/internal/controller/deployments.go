package controller

import (
	securedropzonev1 "gitlab.warpnet.nl/securedropzone/sdz-operator/api/v1"
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// Helper functie om een Deployment resource op te bouwen
func newDeployment(name string, replicas int32, label string, image string, sdz *securedropzonev1.SecureDropzone) appsv1.Deployment {
	return appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      name,
			Namespace: sdz.Namespace,
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: &replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: map[string]string{
					"app": label,
				},
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: map[string]string{
						"app": label,
					},
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{
						{
							Name:  label,
							Image: image,
						},
					},
					ImagePullSecrets: []corev1.LocalObjectReference{
						{
							Name: "gitlab-registry",
						},
					},
				},
			},
		},
	}
}

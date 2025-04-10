
Audit policy file: policy.yaml

kube-apiserver \
  --audit-policy-file=/path/naar/audit-policy.yaml \
  --audit-log-path=/var/log/kubernetes/audit.log \



      - mountPath: /etc/kubernetes/manifests/policy.yaml
      name: audit
      readOnly: true
    - mountPath: /etc/kubernetes/manifests/audit/
      name: audit-log
      readOnly: false


  - hostPath:
      path: /etc/kubernetes/manifests/audit.yaml
      type: File
    name: audit
  - hostPath:
      path: /etc/kubernetes/manifests/audit/
      type: DirectoryOrCreate
    name: audit-log

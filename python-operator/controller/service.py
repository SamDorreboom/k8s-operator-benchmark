import yaml

def get_service(app_label, name):
    return yaml.safe_load(f"""
apiVersion: v1
kind: Service
metadata:
  name: {name}
spec:
  selector:
    app: {app_label}
  ports:
  - name: http
    protocol: TCP
    port: 8080
    targetPort: 8080
""")

from graphviz import Digraph

# Maak een Graphviz-diagram
erd = Digraph('ERD_Kubernetes_Operator', format='png')

# Definieer entiteiten (tabellen/concepten)
erd.node('CRD', 'Custom Resource Definition', shape='rectangle', style='filled', fillcolor='lightblue')
erd.node('Operator', 'SecureDropzone Operator', shape='rectangle', style='filled', fillcolor='lightyellow')
erd.node('Deployment', 'Kubernetes Deployment', shape='rectangle', style='filled', fillcolor='lightgreen')
erd.node('Service', 'Kubernetes Service', shape='rectangle', style='filled', fillcolor='lightpink')
erd.node('ConfigMap', 'ConfigMap', shape='rectangle', style='filled', fillcolor='lightgrey')
erd.node('Pod', 'Application Pod', shape='rectangle', style='filled', fillcolor='lightcyan')
erd.node('Storage', 'Persistent Volume', shape='rectangle', style='filled', fillcolor='lightcoral')

# Relaties tussen de componenten
erd.edge('CRD', 'Operator', label="Managed by")
erd.edge('Operator', 'Deployment', label="Creates and Updates")
erd.edge('Deployment', 'Pod', label="Manages")
erd.edge('Pod', 'Service', label="Exposes via")
erd.edge('Pod', 'ConfigMap', label="Uses Configuration from")
erd.edge('Pod', 'Storage', label="Stores Data in")

# Render het diagram en toon het
erd.render('k8s_operator_erd', view=True)

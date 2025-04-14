from graphviz import Digraph

# Maak een Graphviz-diagram
erd = Digraph('ERD_Kubernetes_Operator', format='png')

# Definieer entiteiten (tabellen/concepten)
erd.node('CRD', 'Custom Resource Definition', shape='rectangle', style='filled', fillcolor='lightblue')
erd.node('Operator', 'SecureDropzone Operator', shape='rectangle', style='filled', fillcolor='lightyellow')
erd.node('SMS', 'SMS service', shape='rectangle', style='filled', fillcolor='lightgreen')
erd.node('Mail', 'Mail Service', shape='rectangle', style='filled', fillcolor='lightpink')
erd.node('Web', 'Web service', shape='rectangle', style='filled', fillcolor='lightgrey')
# erd.node('Pod', 'Application Pod', shape='rectangle', style='filled', fillcolor='lightcyan')
erd.node('Storage', 'Storage service', shape='rectangle', style='filled', fillcolor='lightcoral')


# Relaties tussen de componenten
erd.edge('CRD', 'Operator', label="Managed by")
erd.edge('Operator', 'SMS')
erd.edge('Operator', 'Mail')
erd.edge('Operator', 'Web')
erd.edge('Operator', 'Storage')

erd.edge('Storage','K8s service')
erd.edge('Storage','K8s deployment')

erd.edge('SMS','K8s service sms')
erd.edge('SMS','K8s deployment sms')

erd.edge('Mail','K8s service mail')
erd.edge('Mail','K8s deployment mail')

erd.edge('Web','K8s service web')
erd.edge('Web','K8s deployment web')

# Render het diagram en toon het
erd.render('k8s_operator_erd', view=True)

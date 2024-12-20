from p4utils.mininetlib.network_API import NetworkAPI
import networkx as nx 
import matplotlib.pyplot as plt 
import os


net = NetworkAPI()

# Network general options
net.setLogLevel('info')
net.enableCli()

# Network definition
switches = ['s1']
n_hosts = 4
hosts = [f'h{i}' for i in range(n_hosts)]
n_pss = 1
pss = [f'ps{i}' for i in range(n_pss)]
#Creating concurrently the graph
G = nx.Graph()
colors = []

for _ in switches: 
    print(_)
    net.addP4Switch(_, cli_input='s1-commands.txt')
    G.add_node(_, type='switch')
    colors.append('green')

net.setP4SourceAll('p4src/ATP_switch.p4')
# fa una topologia a STELLA
for _ in hosts: 
    net.addHost(_)
    net.addLink('s1', _)
    G.add_node(_, type='host')
    G.add_edge('s1', _)
    colors.append('yellow')

for _ in pss:
    net.addHost(_)
    net.addLink('s1', _)
    G.add_node(_, type='host')
    G.add_edge('s1', _)
    colors.append('blue')


#Saving the picture of the topology in a folder 
pos = nx.spring_layout(G)
nx.draw(G, pos, labels={node:node for node in G.nodes()}, node_color = colors)
plt.title('Network Topology')
output_file = 'topology.png'

path = os.getcwd() + '/pictures' #getting the current directory 
if not os.path.exists(path):
    os.makedirs(path)
    print(f"folder {path} created.")
else: 
    print(f'folder {path} already existed')

plt.savefig(path + '/'+ output_file, format= "PNG")
print("GRAPH SAVED")



# Assignment strategy
net.l2()

# Nodes general options
net.enablePcapDumpAll()
net.enableLogAll()

# Start network
net.startNetwork()
from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import *
from p4utils.utils.thrift_API import ThriftAPI
import time 
import grpc
from p4.v1 import p4runtime_pb2
from p4.v1 import p4runtime_pb2_grpc
from p4.config.v1 import p4info_pb2

topo = load_topo('topology.json')
controllers = {}

#port is 9090
thrift_port = 9090

for switch, data in topo.get_p4switches().items():
    print(data)
    thrift_ip = topo.get_thrift_ip(switch)
    controllers[switch] = SimpleSwitchThriftAPI(thrift_port=data['thrift_port'],
                                                   json_path=data['json_path'])

client = ThriftAPI(thrift_port, thrift_ip, pre_type = None)
counter = 0

while True: 

    print(f'Iterazione: {counter}')
    for i in range(50):
        value = client.register_read('big_pool', index=i)
        print(value, end = " ")
    print()

    counter+=1
    print('Waiting ...')
    time.sleep(10)
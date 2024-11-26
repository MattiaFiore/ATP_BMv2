from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
import time 
import grpc
from p4.v1 import p4runtime_pb2
from p4.v1 import p4runtime_pb2_grpc
from p4.config.v1 import p4info_pb2

topo = load_topo('topology.json')
controllers = {}

for switch, data in topo.get_p4rtswitches().items():
    controllers[switch] = SimpleSwitchP4RuntimeAPI(data['device_id'], data['grpc_port'],
                                                   p4rt_path=data['p4rt_path'],
                                                   json_path=data['json_path'])

controller = controllers['s1']                        

controller.table_add('pool_access', 'aggregate', ['0'], ['0'])
controller.table_add('pool_access', 'aggregate', ['1'], ['10'])
controller.table_add('pool_access', 'aggregate', ['2'], ['20'])
controller.table_add('pool_access', 'aggregate', ['3'], ['30'])
controller.table_add('pool_access', 'aggregate', ['4'], ['40'])

#Setting for job ID 1 the number of worker to be 4
#So that when it will be full, the system will free the memory of the register
controller.table_add('workers4job', 'clear_memory', ['1', '4'])
controller.table_add('workers4job', 'clear_memory', ['2', '7'])
controller.table_add('workers4job', 'clear_memory', ['5', '10'])


#Adding configuration to automatically print the values inside the register 


# Load P4Info and establish gRPC connection
def read_register_value(address, device_id, register_name, index):
    # gRPC connection to the P4Runtime server
    channel = grpc.insecure_channel(address)
    stub = p4runtime_pb2_grpc.P4RuntimeStub(channel)

    # Read the register
    request = p4runtime_pb2.ReadRequest()
    request.device_id = device_id

    # Specify the register entry
    entity = request.entities.add()
    entity.register_entry.register_id = get_register_id(register_name)
    entity.register_entry.index.index = index

    # Send the request
    responses = stub.Read(request)
    for response in responses:
        for entity in response.entities:
            value = entity.register_entry.data.packet_register_value
            print(f"Register[{index}] = {value}")

def get_register_id(register_name):
    # Load the p4info file to resolve the ID of the register
    # (Example implementation; replace with actual loading logic)
    return 123  # Replace with your register's ID from p4info

# Parameters
grpc_address = "localhost:9559"
device_id = 1
register_name = "big_pool"
index = 0  # Read specific register entry




while True: 

    
    print("Speriamo")
    for i in range(50):
        read_register_value(grpc_address, device_id, register_name, i)
        print(i)
    
    time.sleep(10)
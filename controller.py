from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI


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
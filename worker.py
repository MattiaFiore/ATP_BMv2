import sys 
import socket   
import argparse
from random import randint
from typing import Tuple, List, Any
from scapy.all import Ether, Packet, BitField, IP
from scapy.all import sendp, get_if_list, get_if_hwaddr, load_layer

'''
Packet 
Eth 
Group_header:
    - group reserved 
    - index 

'''
ETHERTYPE_IPV4 = 0x0800
PROTOCOL_ATP = 0x99

class ATP(Packet):
    '''
    Total Lenght of the header is 16 bytes
    - bitmap0: 32 bits 
    - bitmap1: 32 bits 
    - fanInDegree0: 5 bits
    - fanInDegree1: 5 bits
    - overflow: 1 bit
    - resend: 1 bit
    - collision: 1 bit
    - ecn: 1 bit
    - edgeSwitchIdentifier: 1 bit
    - isAck: 1 bit
    - aggregatorIndex: 16 bits
    - JobIdAndSequenceNumber: 32 bits
    '''
    name = 'ATP'
    fields_desc = [
        BitField('bitmap0', default = 0, size = 32),
        BitField('bitmap1', default = 0, size = 32),
        BitField('row_3', default = 0, size = 16),
        BitField('JobIdAndSequenceNumber', default = 0, size = 32)
        ]
    
class Data(Packet): 
    name = 'Data'
    #As the numbers of elements that will enter in a 
    #Moved the aggregatorIndex to the data 
    fields_desc = [BitField('aggregatorIndex', default = 0, size = 15), BitField('BOS', default = 0, size = 1)] + [BitField(f'd{i}', default=0, size = 32) for i in range(1,11)]

def get_ip() -> str:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def get_if() -> str:
    iface = None
    for i in get_if_list():
        if 'eth' in i: 
            iface = i
    
    if iface: 
        return iface 
    else: 
        print('Interfaccia non trovata')
        sys.exit(1)
    
def build_row_3(row3: tuple) -> int: 
    bits = [5, 5, 1, 1, 1, 1, 1, 1]
    bit_string = ''
    for i, j in enumerate(row3):
        #print(f'value: {j}, bin {bin(j)}')
        #print(bin(j % (bits[i]+1))[2:])
        bit_string += bin(j % (bits[i]+1))[2:] #removing the 0b
    
    print(int(bit_string, 2))
    print(bit_string)
    return int(bit_string, 2)

def convert_bitstring(fields: List[Tuple[int, int]]) -> int: 

    bit_string = ''
    for elem in fields:
        bit_string += bin(elem[0] % (2**(elem[1] +1)))[2:].zfill(elem[1])

    
    #print('#'*30)   
    #print(int(bit_string,2))
    #print(bit_string)
    #print('#'*30)

    return int(bit_string, 2)


def parse()-> Any:
    '''
    The program will ask for ID, Sequence number and will compute the hash function 
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--id_job', type=int, help='[ATP]: ID del job', required=True)
    parser.add_argument('-sn', '--sequencenumber', type=int, help='[ATP]: Sequence Number', required=True)
    parser.add_argument('-agg', '--aggregator_number', type = int, help='[ATP]: Number of aggregators', required=True)
    args = parser.parse_args()
    '''
    A sentimento gli diamo:
    - 8 bit per i job id 
    - 24 bit per i sequence number 
    '''
    
    
    return args

def build_payload(length: int, job_id: Any) -> Data:
    width = 32
    #return  ''.join([bin(randint(0,255))[2:].zfill(width) for i in range(length)])
    index = get_agggregator_index(job_id)
    #print()
    return  Data(aggregatorIndex = index, d1=1, d2=1, d3=1, d4=1, d5=1, d6=1, d7=1, d8=1, d9=1, d10=1)


def get_job_id_sequence_number(id_job, sequencenumber): 
    job_id_sequence_number = convert_bitstring([(id_job, 8),(sequencenumber, 24)])
    return job_id_sequence_number

def get_agggregator_index(job_id_sequence_number): 
    aggregator_index = hash(job_id_sequence_number) % args.aggregator_number
    return aggregator_index

if __name__ == '__main__': 

    #Parsing arguments 
    args = parse()

    # Verifica tutta la lista di interfacce
    iface = get_if()
    
    #Creazione del pacchetto
    # destinazione broadcast, tanto per il momento lo deve elaborare lo switch
    eth_header = Ether(src= get_if_hwaddr(iface), dst = 'FF:FF:FF:FF:FF:FF', type = ETHERTYPE_IPV4)
    ip_header = IP(src = get_ip(), proto=PROTOCOL_ATP)

    #Sending jus the first job_id and sequence number, the others will be modified by the switch
    job_id = get_job_id_sequence_number(args.id_job, args.sequencenumber)
    atp_header = ATP(JobIdAndSequenceNumber= job_id)
    packet = eth_header / ip_header / atp_header

    #Building the data 
    length_payload = 10

    #Data in a row
    n_stacked = 3
    for i in range(n_stacked):
        payload = build_payload(length_payload, job_id)
        if i == n_stacked -1: 
            payload.BOS = 1
        packet = packet / payload
        args.sequencenumber += 1
        job_id = get_job_id_sequence_number(args.id_job, args.sequencenumber)


    #[FIX]: payload is actually a header, change name of variable
    '''
    print(f"Chosen aggregator: {pkt[ATP].aggregatorIndex}")
    print('[', end = ' ')
    for i in pkt[Data].fields_desc:
        field_name = i.name
        print(f'{getattr(pkt, field_name)}', end = ' ')
    print(']')
    '''
    packet.show()

    sendp(packet, iface=iface)


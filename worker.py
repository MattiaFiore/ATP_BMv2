import sys 
import socket   
import argparse
from random import randint
from typing import Tuple, List
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
        BitField('aggregatorIndex', default = 0, size = 16),
        BitField('JobIdAndSequenceNumber', default = 0, size = 32)
        ]
    
class Data(Packet): 
    name = 'Data'
    #As the numbers of elements that will enter in a 
    fields_desc = [BitField(f'd{i}', default=0, size = 32) for i in range(1,11)]

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


def parse()-> Tuple[int, int]:
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
    job_id_sequence_number = convert_bitstring([(args.id_job, 8),(args.sequencenumber, 24)])
    aggregator_index = hash(job_id_sequence_number) % args.aggregator_number
    return job_id_sequence_number, aggregator_index

def build_payload(length: int) -> Data:
    width = 32
    #return  ''.join([bin(randint(0,255))[2:].zfill(width) for i in range(length)])
    
    #print()
    return  Data(d1=1, d2=1, d3=1, d4=1, d5=1, d6=1, d7=1, d8=1, d9=1, d10=1)
    

if __name__ == '__main__': 

    #Parsing arguments 
    job_id, agg_index = parse()

    # Verifica tutta la lista di interfacce
    iface = get_if()
    
    #Creazione del pacchetto
    # destinazione broadcast, tanto per il momento lo deve elaborare lo switch
    eth_header = Ether(src= get_if_hwaddr(iface), dst = 'FF:FF:FF:FF:FF:FF', type = ETHERTYPE_IPV4)
    ip_header = IP(src = get_ip(), proto=PROTOCOL_ATP)
    atp_header = ATP(aggregatorIndex = agg_index, JobIdAndSequenceNumber= job_id)
    pkt = eth_header / ip_header / atp_header

    #[FIX]: payload is actually a header, change name of variable
    length_payload = 10
    payload = build_payload(length_payload)
    pkt = pkt / payload

    print(f"Chosen aggregator: {pkt[ATP].aggregatorIndex}")
    print('[', end = ' ')
    for i in pkt[Data].fields_desc:
        field_name = i.name
        print(f'{getattr(pkt, field_name)}', end = ' ')
    print(']')

    sendp(pkt, iface=iface)


import sys 
import socket   
import argparse
from random import randint
from typing import Tuple, List
from scapy.all import Ether, Packet, BitField, IP
from scapy.all import sendp, get_if_list, get_if_hwaddr, load_layer, sniff
from scapy.packet import bind_layers

ETHERTYPE_IPV4 = 0x0800
PROTOCOL_ATP = 0x99

class Data(Packet): 
    name = 'Data'
    #As the numbers of elements that will enter in a 
    #Moved the aggregatorIndex to the data 
    fields_desc = [BitField('aggregatorIndex', default = 0, size = 15), BitField('BOS', default = 0, size = 1)] + [BitField(f'd{i}', default=0, size = 32) for i in range(1,11)]


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

def read_bits(field: int, total_bits: int,bits: List[int]) -> Tuple[int]:
    
    remaining = total_bits
    values = []
    for _ in bits: 
        remaining -= _
        mask = ((1<<_)-1) << remaining
        values.append((field & mask)>>remaining)
    
    return values


def check_collision(atp: ATP) -> bool:
    #[FIX]: row_3 is not actually the entire row. It's half of the third row
    # collition is the bit number 4. 
    return (1<<3)&atp.row_3
        

def handle_pkt(packet) -> None:

    if ATP in packet: 
        print('sta')
    else: 
        print('non sta')

    if Data in packet: 
        print('sta')
    else: 
        print('non sta')

    #packet.show()
    #print(packet.show())
    eth = packet.getlayer(Ether)
    ip = packet.getlayer(IP)
    atp = packet.getlayer(ATP)
    payload = packet.getlayer(Data)
    payload_2 = packet.getlayer(Data)
    payload_3 = packet.getlayer(Data)


    payload.show()
    payload_2.show()
    payload_3.show()
    
    #the job/sequence is an integer
    job_id, sequence_number = read_bits(atp.JobIdAndSequenceNumber, 32,[8, 24])
    print(f"INFORMATION ABOUT job_id: {job_id} sequence_number: {sequence_number}")

    collision = check_collision(atp)
    if collision: 
        print("COLLISION happend")

    print(f'1: {payload.d1}')
    print(f'2: {payload.d2}')
    print(f'3: {payload.d3}')
    print(f'4: {payload.d4}')
    print(f'5: {payload.d5}')
    print(f'6: {payload.d6}')
    print(f'7: {payload.d7}')
    print(f'8: {payload.d8}')
    print(f'9: {payload.d9}')
    print(f'10: {payload.d10}')


    
     
if __name__ == '__main__':
    
    bind_layers(IP, ATP, proto =153)
    bind_layers(ATP, Data)
    iface = get_if()
    print(iface)
    print('starting')
    sniff(filter="ip", iface = iface,
          prn = handle_pkt)
    print('ending')
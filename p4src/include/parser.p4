parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {


    state start{ 
        transition parse_eth; 
    }

    state parse_eth{
        packet.extract(hdr.eth); 
        transition select(hdr.eth.etherType){
            TYPE_IPV4: parse_ipv4;
            default: accept; 
        }
    }

    state parse_ipv4{

        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol){
            PROTOCOL_ATP: parse_atp; 
            default:accept; 
        }
    }
    

    state parse_atp {
        packet.extract(hdr.atp); 
        transition accept; 
    }
}
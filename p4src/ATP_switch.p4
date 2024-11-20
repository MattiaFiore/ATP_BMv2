#include <core.p4>
#include <v1model.p4>

#include "include/types.p4"
#include "include/headers.p4"
#include "include/parser.p4"
#include "include/register.p4"


/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    /*Defining table to enter access the pool*/
    action sum(inout value_t n0,
               in bit<16> aggregatorIndex,
               in bit<16> index){
        
        bit<32> value; 
        bit<32> register_index = (bit<32>)(aggregatorIndex + index); 
        big_pool.read(value, register_index);
        n0 = value + n0; 
        big_pool.write(register_index, n0);

    }

    action aggregate(bit<16> slice_index) {

        meta.slice_index = slice_index; 
            
    } 
    
    table pool_access{
        key = {hdr.atp.aggregatorIndex: exact;}
        actions = {
            aggregate; 
            NoAction;
        }
        size = 5; // Same dimension as the number of pools, right now is 5
        default_action = NoAction; 

    }
    
    apply {
        // In order to see the packet somewhere
        standard_metadata.egress_spec = 3; 

        // In aggregation index there is the index of the pool on which to aggregate
        bit<16> index = hdr.atp.aggregatorIndex; 
        // Define which pool you should access 
        // and aggregate
        pool_access.apply();
        sum(hdr.data.n01, meta.slice_index, 0);
        sum(hdr.data.n02, meta.slice_index, 1);
        sum(hdr.data.n03, meta.slice_index, 2);
        sum(hdr.data.n04, meta.slice_index, 3);
        sum(hdr.data.n05, meta.slice_index, 4);
        sum(hdr.data.n06, meta.slice_index, 5);
        sum(hdr.data.n07, meta.slice_index, 6);
        sum(hdr.data.n08, meta.slice_index, 7);
        sum(hdr.data.n09, meta.slice_index, 8);
        sum(hdr.data.n10, meta.slice_index, 9);
        
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {

    apply {

    }

}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
apply{}
}



control MyDeparser(packet_out packet, in headers hdr) {
    apply {

        //parsed headers have to be added again into the packet.
        packet.emit(hdr.eth);
        packet.emit(hdr.ipv4);

        //Only emited if valid
        packet.emit(hdr.atp);
        packet.emit(hdr.data); 
    }
}


/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

//switch architecture
V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
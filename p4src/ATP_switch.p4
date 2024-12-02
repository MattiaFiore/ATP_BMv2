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

    action increase_counter(){
        bit<32> value; 
        counts.read(value, (bit<32>) hdr.atp.aggregatorIndex);
        value = value + 1; 
        counts.write((bit<32>) hdr.atp.aggregatorIndex, value);
        meta.current_counter = value; 
    }
    
    table pool_access{
        key = {hdr.atp.aggregatorIndex: exact;}
        actions = {
            aggregate; 
            NoAction;
        }
        size = 10; // Same dimension as the number of pools, right now is 5
        default_action = NoAction; 

    }

    action clear_memory(){
        //Clearing the register
        big_pool.write((bit<32>) meta.slice_index + 0, 0);
        big_pool.write((bit<32>) meta.slice_index + 1, 0);
        big_pool.write((bit<32>) meta.slice_index + 2, 0);
        big_pool.write((bit<32>) meta.slice_index + 3, 0);  
        big_pool.write((bit<32>) meta.slice_index + 4, 0);
        big_pool.write((bit<32>) meta.slice_index + 5, 0);
        big_pool.write((bit<32>) meta.slice_index + 6, 0);
        big_pool.write((bit<32>) meta.slice_index + 7, 0);
        big_pool.write((bit<32>) meta.slice_index + 8, 0);
        big_pool.write((bit<32>) meta.slice_index + 9, 0);
        big_pool.write((bit<32>) meta.slice_index + 10, 0);
        big_pool.write((bit<32>) meta.slice_index + 11, 0);
        big_pool.write((bit<32>) meta.slice_index + 12, 0);
        big_pool.write((bit<32>) meta.slice_index + 13, 0);  
        big_pool.write((bit<32>) meta.slice_index + 14, 0);
        big_pool.write((bit<32>) meta.slice_index + 15, 0);
        big_pool.write((bit<32>) meta.slice_index + 16, 0);
        big_pool.write((bit<32>) meta.slice_index + 17, 0);
        big_pool.write((bit<32>) meta.slice_index + 18, 0);
        big_pool.write((bit<32>) meta.slice_index + 19, 0);
        // Clearing the owner
        owner_pool.write((bit<32>) hdr.atp.aggregatorIndex, 0);
        // Clearing the counter
        counts.write((bit<32>) hdr.atp.aggregatorIndex, 0); 
    }

    action aggregate_values(){
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
        sum(hdr.data.n11, meta.slice_index, 10);
        sum(hdr.data.n12, meta.slice_index, 11);
        sum(hdr.data.n13, meta.slice_index, 12);
        sum(hdr.data.n14, meta.slice_index, 13);
        sum(hdr.data.n15, meta.slice_index, 14);
        sum(hdr.data.n16, meta.slice_index, 15);
        sum(hdr.data.n17, meta.slice_index, 16);
        sum(hdr.data.n18, meta.slice_index, 17);
        sum(hdr.data.n19, meta.slice_index, 18);
        sum(hdr.data.n20, meta.slice_index, 19);
    }

    table workers4job {
        key = {
            hdr.atp.JobIdAndSequenceNumber[31:24]: exact; 
            meta.current_counter: exact; // Should have the same number of
        }
        actions = {
            NoAction;
            clear_memory; 
        }
        size = 100; 
        default_action = NoAction; 
    }

    apply {
        // In order to see the packet somewhere
        standard_metadata.egress_spec = 3; 

        // In aggregation index there is the index of the pool on which to aggregate
        bit<16> index = hdr.atp.aggregatorIndex; 
        
        // Checking if the pool is free
        bit<32> owner; 
        owner_pool.read(owner, (bit<32>)index);
        pool_access.apply();

        if (owner == hdr.atp.JobIdAndSequenceNumber){
            
            // The owner as alreay bin set 
            aggregate_values(); 

            increase_counter(); 
            workers4job.apply();

        } else {
            if (owner == 0){
                // The pool is free
                // First you set the owner of the pool 
                
                owner_pool.write((bit<32>) index, hdr.atp.JobIdAndSequenceNumber); 

                //Add values inside the register
                aggregate_values(); 

                increase_counter(); 
                

            } else {
                // The pool selected is NOT FREE
                // So you just send the packet to the ps saying that
                // collision is active 
                hdr.atp.collision = (bit<1>) 1; 
            }
        }
        
        
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
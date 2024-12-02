/*

*/

#define MAX_ENTRIES_PER_PACKET 32
/*************************************************************************
 ***********************  H E A D E R S  *********************************
 *************************************************************************/


/*
REWRITING ATP HEADERS INTO NORMAL P4 
*/

// 14Byte
header ethernet_t {
    ethAddr_t dstAddr; 
    ethAddr_t srcAddr; 
    bit<16> etherType;
}

// 20Byte
header ipv4_t {
    bit<4> version; 
    bit<4> ihl; 
    bit<6> dscp; 
    bit<2> ecn; 
    bit<16> totalLen;
    bit<16> identification; 
    bit<3> flags; 
    bit<13> fragOffset; 
    bit<8> ttl; 
    bit<8> protocol; 
    bit<16> hdrChecksum; 
    ipAddr_t srcAddr; 
    ipAddr_t dstAddr; 
}

header atp_t{
    bit<32> bitmap0; 
    bit<32> bitmap1; 
    bit<5> fanInDegree0; 
    bit<5> fanInDegree1;
    bit<1> overflow;
    bit<1> resend;
    bit<1> collision;
    bit<1> ecn;
    bit<1> edgeSwitchIdentifier;
    bit<1> isAck;
    bit<16> aggregatorIndex;
    bit<32> JobIdAndSequenceNumber;
}

header data_h{
    value_t n01;
    value_t n02;
    value_t n03; 
    value_t n04;
    value_t n05;
    value_t n06;
    value_t n07;
    value_t n08;
    value_t n09;
    value_t n10;
    value_t n11;
    value_t n12;
    value_t n13; 
    value_t n14;
    value_t n15;
    value_t n16;
    value_t n17;
    value_t n18;
    value_t n19;
    value_t n20;
}

struct metadata{
    bit<16> slice_index; //This will be 0, 10, 20,  ...
    bit<32> current_counter; 
}

struct headers {
    ethernet_t eth; 
    ipv4_t ipv4; 
    atp_t atp; 
    data_h data; 
}
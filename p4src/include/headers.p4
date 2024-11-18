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

struct metadata{
    
}

struct headers {
    ethernet_t eth; 
    ipv4_t ipv4; 
    atp_t atp; 
}
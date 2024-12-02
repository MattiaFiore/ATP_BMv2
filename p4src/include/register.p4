
// Trying to implement the register access usign 
// a register as big as (register_size X n_pools) 

// Number of registers: 10
// Number of integers per register: 20
register<value_t>(200) big_pool; 

//register is reserved based on job id and sequence number
register<bit<32>>(10) owner_pool;   

// Counter for packets 
register<bit<32>>(10) counts;
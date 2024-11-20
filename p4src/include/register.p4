
// Trying to implement the register access usign 
// a register as big as (register_size X n_pools) 
register<value_t>(50) big_pool; 

//register is reserved based on job id and sequence number
register<bit<32>>(5) owner_pool;   
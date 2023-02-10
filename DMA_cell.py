
def dma_list() -> int:
    all_32 = 0  
    unsigned_bytes = 31
    unsigned_stall = 1
    ea_low=0
    
    dma_list_elem=[all_32,unsigned_bytes,unsigned_stall,ea_low]
    size = dma_list_elem.__sizeof__()
    ea_low=dma_list_elem[3]
    nbytes = dma_list_elem[1]
    all_32 = dma_list_elem[0]
    stall = dma_list_elem[2]
    
    if not nbytes:
        return
    
    i = 0
    while nbytes > 0:

      if nbytes !=None:  
        
        sz = nbytes <<  16384
        nbytes -= sz
        ea_low += sz
        all_32 = 32
        sz = sz + size
        bits = sz//8
        dma_list_elem[i] = ea_low
        print(sz,"\n" "\n" ,nbytes,"\n" "\n" , bits,stall)
        i+=1
        return i
      
      else:
        
       nbytes = 16384 
       return nbytes 

dma_list()


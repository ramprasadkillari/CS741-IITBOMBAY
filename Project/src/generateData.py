from Crypto.Util import number
import random
import sys

# parameters
NUM_BITS = None  # key size in bits
NUM_TRACES = None  # number of traces to generate

NUM_BITS = int(sys.argv[1])
NUM_TRACES = int(sys.argv[2])

fractionNoise = 0.04    # fraction of bits in each trace to corrupt 

# name of the file to write data into
datafile = "data.txt"

numNoise = int(fractionNoise*NUM_BITS)

# generate a random prime number(RSA key) of length NUM_BITS
keyDecimal = number.getPrime(NUM_BITS)

keyBinary = bin(keyDecimal)[2:]

# function for creating a trace given a binary string as input.
def createTrace(binaryStr):
    binaryList = list(binaryStr)

    # sample the indices to corrupt
    idx_list = random.sample(range(0,NUM_BITS), numNoise)
    
    for idx in idx_list:
        # choose between bit flip, insertion and deletion at a chosen index(idx)
        random_coice = random.choice([0, 1, 2])
        if(random_coice == 0):
            # flip bits
            try:
                if(binaryList[idx] == '0'):
                    binaryList[idx] == '1'
                else:
                    binaryList[idx] = '0'
            except:
                pass
                       
        elif(random_coice == 1):
            # insert bits
            rand_ele = random.choice(['0', '1'])
            try:
                binaryList.insert(idx, rand_ele)
            except:
                pass    
        else:
            # delete bits
            try:
                binaryList.pop(idx)
            except:
                pass    
    
    return "".join(binaryList)


# write the original key, followed by traces into the data file.
fp = open(datafile, 'w+')

fp.write(keyBinary+'\n')

for _ in range(NUM_TRACES):
    trace = createTrace(keyBinary)
    fp.write(trace+'\n')

fp.close()
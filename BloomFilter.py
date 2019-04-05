from BitHash import BitHash 
import BitVector

class BloomFilter(object):
    
    # Return the estimated number of bits needed in a BF that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.   
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        n = numKeys                  # numKeys you need to insert
        d = numHashes                # numHash functions youre using
        p = maxFalsePositive         # maxFalsePositive probability
        stillZero = (1 - p**(1/d))
        N = (d/(1-stillZero**(1/n)))

        return N 
 
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        N = int(self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)) # find out how big it needs to be 
        self.__BloomFilter = BitVector.BitVector(size = N)               # the bitVector
        self.__numHashes = numHashes                                    
        self.__size = N                                                 

    def hashFunc(self, s, p = None):
        hashes = []

        x = BitHash(s)
        hashes += [x % self.__size]

        for i in range(self.__numHashes - 1):
            x = BitHash(s, x)
            hashes += [x % self.__size]

        return hashes

    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        hashes = self.hashFunc(key)
        
        for i in range(len(hashes)):
            self.__BloomFilter[hashes[i]] = 1   
 
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        # if any of the positions have a 0, return False
        hashes = self.hashFunc(key)

        for i in range(len(hashes)):
            if self.__BloomFilter[hashes[i]] == 0:  return False
        
        return True          # if none are 0, return True
       
    # Returns the current *projected* false positive rate based
    # on the current number of bits that are set in the BF 
    def falsePositiveRate(self):
        count = self.numBitsSet()
        bitsSet = count/self.__size
        p = bitsSet**self.__numHashes
        
        return p   
       
    # Returns the current number of bits that are set in the BF
    def numBitsSet(self):
        count = self.__BloomFilter.count_bits()

        return count

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
 
    bf = BloomFilter(numKeys, numHashes, maxFalse)

    # read the first numKeys words from the file and insert them 
    words = []

    f = open('wordlist.txt', 'r')
    words = f.readlines()
    f.close()
    words2 = [words[i] for i in range(numKeys, numKeys*2)]
    words = [words[i] for i in range(numKeys)]

    for i in words:      bf.insert(str(i))

    # Print the projected false positive rate  
    # based on the number of bits that actually
    # ended up being set in the Bloom Filter. 
    print(bf.falsePositiveRate())

    # count how many of the words are missing
    # from the BF and print it (should be 0)     
    count = 0
    for i in words:
        if bf.find(str(i)) == False:    count += 1
    print(str(count) + " words are missing from the Bloom Filter.")
        
    # read the next numKeys words from the file (that are not in the BF),
    # and count how many of them are (falsely) found in the BF.
    count2 = 0
    for i in words2:
        if bf.find(str(i)) == True:     count2 += 1
    print(str(count2) + " words were falsely found in the Bloom Filter.")

    # Print out the false positive rate (should be close to the projected rate)
    print("the percentage rate of false positives is " + str(count2/numKeys))

    
if __name__ == '__main__':
    __main()       


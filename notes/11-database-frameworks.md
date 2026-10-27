## Latency Numbers Chart
operation   ns    ms
Send 2 kB over 10 Gbps network 1,600 0.0016
Read 1 MB sequentially from SSD 1,000,000 1
Read 1 MB sequentially from disk 5,000,000 5
Disk seek 10,000,000 10
TCP packet round trip between
continents
150,000,000 150


### Nines in system availability

• One nine (90%): ~36.5 days of downtime per year
• Two nines (99%): ~3.65 days of downtime per year
• Three nines (99.9%): ~8.8 hours of downtime per year
• Four nines (99.99%): ~52.6 minutes of downtime per year
• Five nines (99.999%): ~5.3 minutes of downtime per year (considered the gold standard for high availability)
• Six nines (99.9999%): ~31.5 seconds of downtime per yea

### Availability


### Durability

Data that remains safe and available consistent
So a data remaining in a memory card , the durability of its is very less that it is very likely to go broke , or go corrupted , 


## Terminologies

### SSD Reading time

## Storage System 
SSD can't replace , it can onl


You absolutely can store the ASCII bytes. The problem isn't converting data into bytes; it's knowing where one piece of data ends and the next begins when you read it back. 

Length-prefixed encoding is used when writing a data block ( keys and values), what it will do is lets say the data is 
key = apple
value = red
key = banana
value = yellow
so concatenated will be liek appleredbananayellow

### Read Amplification

The amount of data the app has to actually read so that it can satisfy the read request , lets say we wanted 256B pf date, but disk always gives in pages , gives 1 page (4KB) so the read amplification is (4096/256) = 16x which is 16times more data than we needed 

Lets say I want to search for a word in dictionary of 2000 words, called encyclopedia, and in order to search it I will first look the first letter of the word I am going to search for , supposed to be E
using the kye or some book mark where it has the index of all the letters in a dictionary, I will stratightaway go to E , assume E has a words of 200, so we start searching and eventually we know that encyclopedia comes in the middle which we would say 100th , so the read amplification is 2000 / 100 = 20x times 

### Spatial Locality 
Spatial: rows near each other in sort-key order end up near each other on disk. (SSTables guarantee this, since they’re sorted.)

“Prefixing order IDs with customer ID” — what this means and how to do it

The idea: design your key as customer_id + order_id (concatenated), e.g. cust2#order1, cust2#order2, cust2#order3, instead of a bare incrementing order_id like o_8231. Sorted order then groups all of one customer’s orders together, so they land in the same or adjacent pages.



# TODO:

NAND Flash

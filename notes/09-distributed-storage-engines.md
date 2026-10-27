## Database and Storage system design - 11-database-framework

Database Storage system
         │             
         │             
         ▼             
   Storage Engine      
         │             
         │             
         ▼             
    Storage Technique  
         │             
         │             
         ▼             
    Physical Storage   


Data Model - How a data is logically represented and related (relational, key-value, document, graph, wide-column.)

Data Structure - How data is organized to retrieve it efficiently (hash table, B-tree, B+ tree, LSM tree, trie, skip list.) ordered/unordered flat files
hash tables
B+ trees
ISAM
heaps

Data Storage - Describe how data is written and maintained , Describes the strategy used to store and modify records. (append-only log, in-place updates, copy-on-write, write-ahead logging (WAL), immutable sorted files.)

Storage Engine - Combines data structures, storage techniques, indexing, recovery, and other mechanisms.

Examples: InnoDB (MySQL), WiredTiger (MongoDB), RocksDB.

Example: RocksDB uses an LSM-tree-based architecture with memtables, SSTables, and compaction.

![storage engine](/assets/storage_engine.png)

## Log Append Storage

So as the name says, it for every write , data gets appended to a file,

### Hash map Indexing

Here for every byte offset of the keys are stored in a in memory hash map , so lets

say the values are stored in disk like this (byte, data)

0 ---- name=Ana (Older value)


9 ---- city=Pune


19 ---- age=40





26 ---- name=Ben

In RAM:
9  --> City
19 --> age
26 --> name


![compaction and merging](/assets/compaction.png)


### Sorted String Tables
A log structured storage (key-value) pairs, with keys are sorted 

an sst file on disk will be like this 

Block 1 — offset 0

apple → red
banana → yellow
carrot → orange
cherry → red

Block 2 — offset 4096

grape → purple
kiwi → green
lemon → yellow
mango → orange

Block 3 — offset 8192

orange → orange
peach → pink
pear → green
plum → purple

Index key	Block offset
apple	0
grape	4096
orange	8192

The index entries are sorted too, so you can binary-search the index to find the appropriate block.

#### Filter Index
Min/Max Filter
Bloom filter - https://en.wikipedia.org/wiki/Bloom_filter

Here Merging is efficient because of mergeSort and produces a new merged sorted file which also has a sorted key 
if multiple segments has same keys , we can take the latest segment as the ultimate
also sparse indexing works like magic as each segments 

- Compaction and merging keep the number of segments small. Merging is cheap because the segments are sorted

### LSM - Log structure Merge
the principle of using SST and key-value pair based
In turn it has high write throughput

TODO : Lucene, elastic search, solr, cassandra,  ~~text~~,  DB, riak, AVL , Red Black Trees 

Design
Comm

    Conscious effort




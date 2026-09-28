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
Here Merging is efficient because of mergeSort and produces a new merged sorted file which also has a sorted key 
if multiple segments has same keys , we can take the latest segment as the ultimate
also sparse indexing works like magic as each segments 

- Compaction and merging keep the number of segments small. Merging is cheap because the segments are sorted

### LSM - Log structure Merge
the principle of using SST and key-value pair based
In turn it has high write throughput
TODO : Lucene, elastic search, solr, cassandra,  ~~text~~,  DB, riak, AVL , Red Black Trees 


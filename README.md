# MerkleTreePy
A python class to create merkle hash trees.

## Usage:

```python
from merkletree import merkletree as mt

algorithm = 'sha256'
mytree = mt(algorithm)

```
Where algorithm is the method used to get the hash. The available methods are the same methods available in the [hashlib](https://docs.python.org/2/library/hashlib.html) package.


## Properties:
```python
from merkletree import merkletree as mt
algorithm = 'sha256'
mytree = mt(algorithm)

# current number of leaves
mytree.n

# current number levels in the tree (start by 1)
mytree.levels

# get the tree. This retuens a list of length mytree.levels. Index 0 represent the leaves, index -1 is the root
mytree.tree

# get the hash algorithm name
mytree.algorithm
```

## Methods
```python
from merkletree import merkletree as mt
algorithm = 'sha256'
mytree = mt(algorithm)

# Add new entry
data = 'some data that you want to include in the tree'
mytree.add(data)

# Update a leave
data = 'new update data' #string
pos = 0 #integer
mytree.update(pos,data)

# get the root of the tree. returns the root of the tree in hexString format witout 0x
mytree.getRoot()

# create proof of inclusion of some data in the position "pos". return an array with the branches needed calculate the root using the data in position "pos". It is assumed that the validator have the root(which is public) and the data at position pos, that wants to validate 
pos = 0 # integer
mytree.createProof(pos)
```

## About the proofs

The Figure below show a Merkle tree construction. Assume that you are working on a distributed system, where the data is stored in a decentralized fashion (like bitcoin). Assume that you want to test if a piece of imfromation **A** is included in the decentralized database. If you have a copy of the data you do not need a merkle tree. but is you are a 'light' client, that uses the data but do not store it, you need to ask to other nodes. Remember that you do not trust the other nodes and the only pieces of infromation that you have is **A** (that you want to verify) and the root (the top block of the tree). 

When you ask to the node: is **A** included in the database the node generate a proof, that is fromed by the branches that you need to calculate the root (the root is public)

MerkleTreePy produces this proof using `createProof(pos)`. For **A** you should use createProof(0), which will return a list containing the two elements the green boxes in the example below. You can then use this to generate the root doing: **sha256(sha256(sha256(A),proof[0]),proof[1])** this should be equal to the value of the root, if not **A** is not in the database.



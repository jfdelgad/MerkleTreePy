# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 22:39:19 2018
@author: Jaime Delgado Saa
"""
import hashlib

class merkletree:
    def __init__(self,algorithm):
        self.n = 0                                                             # number of entries (leaves)
        self.levels =0                                                         # number of levels
        self.tree = []                                                         # Full Tree one list per level
        self.algorithm = algorithm                                             # Hash algorithm
    
    # fy=unction to get the root of the tree
    def getRoot(self):
        return self.tree[-1][0]
    
 
    # calculate the levels given a number of leaves
    def getLevels(self,x):  
        return x.bit_length() + int(bin(x).count('1')-1!=0) if x!=0 else 0 
    
   
    # add new leaf
    def add(self,data):                
    
        self.n = self.n + 1
        self.levels = self.getLevels(self.n)
        
        # add a level if needed
        if len(self.tree)<self.levels:
            self.tree.append([])
        
        # update first level
        self.tree[0].append(self.getHash(data));

        # update upper levels
        grow = True
        for i in range(1,self.levels):
            if divmod(len(self.tree[i-1]),2)[1]==0:
                if len(self.tree[i])==0:
                    self.tree[i].append('')
                
                self.tree[i][-1] = self.getHash(self.tree[i-1][-2]+self.tree[i-1][-1])
                grow = False
            else:
                if grow:                    
                    self.tree[i].append(self.getHash(self.tree[i-1][-1])) 
                else:
                    self.tree[i][-1] = self.getHash(self.tree[i-1][-1])



    
    
    # update leaf value
    def update(self, pos, data):
        
        self.levels = self.getLevels(len(self.tree[0]))        
        self.tree[0][pos] = self.getHash(data)
        
        
        for i in range(1,self.levels):
            m = divmod(pos,2)
            if m[1]==1:
                
                self.tree[i][m[0]] = self.getHash(self.tree[i-1][pos-1]+self.tree[i-1][pos])
                pos = m[0]
            else:
                
                self.tree[i][m[0]] = self.getHash(self.tree[i-1][pos]+self.tree[i-1][pos+1])
                pos = m[0]



    #Create proof of existence of data is position pos
    def createProof(self,pos):
        proof = []
        for i in range(1,self.levels):
            m = divmod(pos,2)
            if m[1]==1:
                proof.append(self.tree[i-1][pos-1])
                pos = m[0]
            else:
                proof.append(self.tree[i-1][pos+1])
                pos = m[0]
                
        return proof



    def getHash(self,data):
        h = hashlib.new(self.algorithm)
        h.update(data.encode())
        return h.hexdigest()
        
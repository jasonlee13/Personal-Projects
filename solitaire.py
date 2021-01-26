#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 10:42:09 2020

@author: jason
"""
# DIRECTIONS :: {String : (int, int)}
# Maps the string names of directions to their vector representations
DIRECTIONS = {"N":(-1,0),"NE":(-1,1),"E":(0,1),"SE":(1,1),
              "S":(1,0),"SW":(1,-1),"W":(0,-1),"NW":(-1,-1)}

##################################################
### THIS CODE IS FOR TESTING, YOU MAY IGNORE   ###
##################################################

class Board:
    def __init__(self, B, D):
        self.B = B
        self.D = D
    def __hash__(self):
        return hash(self.B)
    def __eq__(self, other):
        return self.B == other.B
    def is_solved(self):
        nonempty = False
        for p in self:
            if nonempty:
                return False
            nonempty=True
        return nonempty
    def is_legal_move(self, m, orientation = "forward"):
        r, c, d = m
        dr, dc = DIRECTIONS[d]
        before = (1, 1, 0)
        if orientation == "reverse": 
            before = (0, 0, 1)
        for i in range(3):
            if self[r + i*dr, c + i*dc] != before[i]:
                return False
        return True
    def all_legal_moves(self, orientation = "forward"):
        for r,c in self:
            for d in self.D:
                if self.is_legal_move((r,c,d), orientation):
                   yield((r,c,d))

class NormalBoard(Board):
    def __init__(self, B, D):
        super().__init__(tuple(tuple(p for p in row) for row in B), D)
    def __iter__(self):
        for r in range(len(self.B)):
            for c in range(len(self.B[r])):
                if self.B[r][c] == 1:
                    yield (r, c)
    def __str__(self):
        return "\n".join([str(row) for row in self.B])
    def __getitem__(self, i):
        r,c = i
        if (0 <= r < len(self.B)) and (0 <= c < len(self.B[r])):
            return self.B[r][c]
        return 2
    def make_move(self, m, orientation = "forward"):
        r, c, d = m
        dr, dc = DIRECTIONS[d]
        after = (0, 0, 1)
        if orientation == "reverse": 
           after = (1, 1, 0)
        B = [[p for p in row]for row in self.B]
        for i in range(3):
            B[r + i*dr][c + i*dc] = after[i]
        return NormalBoard(B, self.D)
    def sparsify(self):
        blocked = []
        for r in range(len(self.B)):
            for c in range(len(self.B[0])):
                if self[r,c] == 2:
                    blocked.append((r,c))
        return SparseBoard(len(self.B), len(self.B[0]), frozenset(self), self.D, frozenset(blocked))
    def desparsify(self):
        return self

class SparseBoard(Board):
    def __init__(self, R, C, B, D, blocked = frozenset()):
        super().__init__(B, D)
        self.R = R
        self.C = C
        self.blocked = blocked
    def __iter__(self):
        for p in self.B:
            yield p
    def __str__(self):
        return "{} x {}\n{}".format(self.R, self.C, str(self.B))
    def __getitem__(self, i):
        if (i[0] < 0) or (i[0] >= self.R) or (i[1] < 0) or (i[1] >= self.C):
            return 2
        if i in self.blocked:
            return 2
        if i in self.B:
            return 1
        return 0
    def make_move(self, m, orientation = "forward"):
        r, c, d = m
        dr, dc = DIRECTIONS[d]
        B = {p for p in self}
        if orientation == "reverse":
            B.add((r, c))
            B.add((r+dr, c+dc))
            B.remove((r+dr*2, c+dc*2))
        else:
            B.remove((r, c))
            B.remove((r+dr, c+dc))
            B.add((r+dr*2, c+dc*2))
        return SparseBoard(self.R, self.C, frozenset(B), self.D, self.blocked)
    def sparsify(self):
        return self
    def desparsify(self):
        return NormalBoard([[self[r,c] for c in range(self.C)] for r in range(self.R)], self.D)

##########################
### STOP IGNORING HERE ###
##########################

# get_path :: int, {int : (Board, (int, int, String))} -> [(int, int, String)]
# Computes a list of moves that will transform the starting configuration into
#   a target configuration
# h is the hash value of the target configuration
# bfs_tree maps a hash value H(B) to (B, m), where m is the last move on the
# path to B found during the BFS search
def get_path(h, bfs_tree):
    path = []
    while True:
        m = bfs_tree[h][1]
        if m is None:
            path.reverse()
            return path
        path.append(m)
        h = hash_homomorphism(h, m)

# homomorphic_hash :: Board -> int
# Hashes a board in O(k) time
def homomorphic_hash(B):
    h = 0
    for p in B:
        h ^= hash(p)
    return h


###################################################
### PLEASE DO NOT MODIFY ANY OF THE ABOVE CODE! ###
### This code is included for your convenience, ###
### but modifications may cause you a headache! ###
###################################################

# hash_homomorphism :: int, (int, int, String) -> int
def hash_homomorphism(h, m):
    #########################
    ### Implement me pls! ###
    #########################
    x, y = DIRECTIONS[m[2]]
    s1 = (m[0], m[1])
    s2 = (m[0] + x, m[1] + y)
    s3 = (m[0] + 2*x, m[1] + 2*y)
    
    h ^= hash(s1)
    h ^= hash(s2)
    h ^= hash(s3)
    
    return h

# solve :: Board -> [(int, int, String)]
def solve(B):
    #########################
    ### Implement me pls! ##
    #########################
    hashedboard = homomorphic_hash(B)
    
    queue = [B]
    bfs = {hashedboard: (B, None)}
    visited = {hashedboard}
    
    if B.is_solved():
        return []
    
    while queue:
        current = queue.pop()
        has = homomorphic_hash(current)
        for m in current.all_legal_moves():
            neighbor = hash_homomorphism(has, m)
            if neighbor not in visited:
                temp = current.make_move(m)
                visited.add(neighbor)
                bfs[neighbor] = (temp, m)
                queue.append(temp)
                
                if temp.is_solved():
                    return get_path(neighbor, bfs)
                
    return None
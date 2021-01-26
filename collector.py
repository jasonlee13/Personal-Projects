#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:14:43 2020

@author: jason
"""
def collector(coins, mags, n):
    """
    Finds a path that maximizes points
    Args:
        coins (List[List[int]]): 1 at coins[i][j] if there's a coin at (i,j), else 0
        mags (List[List[int]]): 1 at mags[i][j] if there's a magnifier at (i,j), else 0
        n (int): dimensions of the nxn board
    """
    memo = {}
    
    def d(a, b, c):
        if a == n-1 and b == n-1:
            memo[(a,b,c)] = (coins[a][b]*(2**c), ((a, b), ))
            return None
        
        elif a == n-1 and b < n:
            if (a, b+1, c+mags[a][b]) not in memo:
                d(a, b+1, mags[a][b]+c)
                
            memo[(a, b, c)] = (coins[a][b]*(2**c) + memo[(a, b+1, mags[a][b]+c)][0], ((a, b), ) + memo[(a, b+1, mags[a][b]+c)][1])
            return None
        
        elif a < n and b == n-1:
            if (a+1, b, 0) not in memo:
                d(a+1, b, 0)
                
            memo[(a, b, c)] = (coins[a][b]*(2**c) + memo[(a+1, b, 0)][0], ((a, b), ) + memo[(a+1, b, 0)][1])
            return None
        
        if (a, b+1, mags[a][b]+c) not in memo:
            d(a, b+1, mags[a][b]+c)
            
        if (a+1, b, 0) not in memo:
            d(a+1, b, 0)
            
        if memo[(a+1, b, 0)][0] <= memo[(a, b+1, mags[a][b]+c)][0]:
            memo[(a, b, c)] = (coins[a][b]*(2**c) + memo[(a, b+1, mags[a][b]+c)][0], ((a, b), ) + memo[a, b+1, mags[a][b]+c][1])
        
        if memo[(a+1, b, 0)][0] > memo[(a, b+1, mags[a][b]+c)][0]:
            memo[(a, b, c)] = (coins[a][b]*(2**c) + memo[(a+1, b, 0)][0], ((a, b), ) + memo[(a+1, b, 0)][1])
    
    d(0, 0 ,0)
    return(memo[(0, 0, 0)][1])

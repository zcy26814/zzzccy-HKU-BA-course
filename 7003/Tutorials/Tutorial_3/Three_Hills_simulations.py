#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import random
import math

class Three_hills:
    
    # generating a total number of repaired per hour
    def randum(self,d_table,size=None):
        if size == None or size==1:
            temp = random.rand()
            for j in range(len(d_table)):
                if d_table[j][1]>temp:
                    pointer = j
                    break
            return d_table[pointer][0]
        else:
            numbers = []
            temp = random.rand(size)
            for i in range(size):
                for j in range(len(d_table)):
                    if d_table[j][1]>temp[i]:
                        pointer = j
                        break
                numbers.append(d_table[pointer][0])
            return numbers            
    
    # simulations(repaireperson with the given distrubution)
    def simulation1(self,n,lambda_bio,dist_table,c,w,m):
    # n -- simlation hours 
    # lambda- success probability 1-exp(-lambda) 
    # c -- breakdown cost per hour 
    # w-wage for per worker per hour
    # m-the number of worker
        K = 200 # intial working_generorator_number
        k = 200 # working_generorator_number (for numberating)
        breakdown_costs = []
        for i in range(n):
            # generating a total number of breakdown
            total_number_breakdown = random.binomial(k,1-(math.exp(-lambda_bio)),size = None)+K-k
            working_num0 = K-total_number_breakdown #working genrators (beofre repaired)
            total_number_repaired = min(self.randum(dist_table)*m,total_number_breakdown)#repaired <= breakdown 
            breakdown_costs.append(c * (K-working_num0)+ w*m)
            k = working_num0 + total_number_repaired #working genrators (after repaired)
            i += 1
        average_cost = sum(breakdown_costs)/len(breakdown_costs)
        return average_cost   

    #simulations(repaireperson whose hourly repair rate is constantly one)
    def simulation2(self,n,lambda_bio,c,w,m):
    # n -- simlation hours 
    # lambda_bio - failure rate
    # c -- breakdown cost per hour 
    # w-wage for per worker per hour
    # m-the number of worker
        K = 200 # intial working_generorator_number
        k = 200 # working_generorator_number (for numberating)
        breakdown_costs = []
        for i in range(n):
            # generating a total number of breakdown
            total_number_breakdown = random.binomial(k,1-(math.exp(-lambda_bio)),size = None)+K-k
            working_num0 = K-total_number_breakdown #working genrators (beofre repaired)
            total_number_repaired = min(1,total_number_breakdown)#repaired <= breakdown 
            breakdown_costs.append(c * (K-working_num0)+ w*m)
            k = working_num0 + total_number_repaired #working genrators (after repaired)
            i += 1
        average_cost = sum(breakdown_costs)/len(breakdown_costs)
        return average_cost 


if __name__ == '__main__':
    simulation_number = 10000
    lambda_1 = 1/400 #failure rate
    c = 75 #breakdown cost per hour
    w = 30 #wage for per worker per hour
    m1 = 1 #the number of worker
    m2 = 2
    dist_table = {0:[0,0.28],1:[1,0.8],2:[2,1]}#disturtion of repairperson
    three_hills = Three_hills()
    #Simulation（a single repairperson）-- option A)
    print(three_hills.simulation1(simulation_number,lambda_1,dist_table,c,w,m1))
    #Simulation（two workers with the same skills）-- option B)
    print(three_hills.simulation1(simulation_number,lambda_1,dist_table,c,w,m2))
    # Simulation（repaireperson whose hourly repair rate is constantly one)-- option C)
    print(three_hills.simulation2(simulation_number,lambda_1,c,w,m1))
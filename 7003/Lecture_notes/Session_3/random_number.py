from numpy import random
dist_table={0:[4,0.05], 1:[5,0.2], 2:[6,0.45], 3:[7,0.65], 4:[8,0.8], 5:[9,0.9], 6:[10,1.0]}
def randnum(d_table, size=None):
    if size==None or size==1:
        temp=random.rand()
        for j in range(len(d_table)):
            if d_table[j][1]>temp:
                pointer=j
                break
        return d_table[pointer][0]
    else:
        numbers=[]
        temp=random.rand(size)
        for i in range(size):
            for j in range(len(d_table)):
                if d_table[j][1]>temp[i]:
                    pointer=j
                    break
            numbers.append(d_table[pointer][0])
        return numbers
        
print(randnum(dist_table))
print(randnum(dist_table,5))

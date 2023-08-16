# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 14:56:59 2022

@author: Gašper Petek
"""

from scipy.optimize import linprog
import numpy as np
from numpy import random
import matplotlib.pyplot as plt



''' - Input values - '''

''' Number of servers (and users) '''
server = 4

''' Users needs and servers offerings '''
''' 0 = servers, users and connections are value of 1.
    1 = servers, users and connections have random values.
    2 = servers offer exactly what users want. Connections have value of 1.
    3 = servers and users are value of 1, conectionns have random value 
    from 0 to 1.
    4 = server and connections have value of 1, users have different needs,
    fomr 0 to 1.
    5 = servers are between 0 and 1, connections and usres have value of 1.
    6 = network failure.'''
situation = 2

''' Cost function - maximizing input or output currents '''
''' 0 = maximize only servers.
    1 = maximize users only.
    2 = maximize users and servers.'''
maximize = 0




# Number of nodes
node = (server-2)*server 
# Number of currents
current = 2*(node+1)

Z = 2*current
Y = 2*server


def A_ineq():
    
    B = [ [ 0 for i in range(current) ] for j in range(Z) ]
    index1=0
    index2=0
    for i in range(Z):
        if i == 0 or i % 2 == 0:
            B[i][index1] = 1
            index1= index1 + 1
        else:
            B[i][index2] = -1
            index2 = index2 + 1
    return B


def servervalue(i):
    return random.uniform(i/Y,(i+1)/Y)
   

def B_ineq(situation = 0):
    ''' Matrix of different situations in terms of user needs and server offerings'''
    
    if(situation == 0):
        ''' Trivial solution - servers, users and connections are value of 1.'''
        return np.full(Z,1)
        
    elif(situation == 1):
        ''' Servers, users and connections have random values.'''
        con = [ 1 for z in range(Z) ] 
        for k in range(0,Z,2):
            a = random.rand()
            con[k]= a
            con[k+1]= a
        return con
    
    elif(situation == 2):
        ''' Servers offer exactly what users want. Connections have value of 1.'''
        con = [ 1 for z in range(Z) ]
        for i in range(0,Z,2):
            if i < Y:
                b0 = servervalue(i)
                con[i] = b0
                con[i+1] = b0
                con[i+Z-Y] = b0
                con[i+1+Z-Y] = b0
        return con
    
    elif(situation == 3):
        '''servers and users are value of 1, conectionns have random value 
        from 0 to 1'''
        con = [ 1 for z in range(Z) ]
        for i in range(0,Z,2):
            if i >= Y and i < (Z-Y):
                b1 = random.uniform((i-Y)/(Z-(2*Y)),(i+1-Y)/(Z-(2*Y)))
                con[i] =  b1
                con[i+1] =  b1
        return con
    
    elif(situation == 4):
        '''server and connections have value of 1, users have different needs,
        fomr 0 to 1'''
        con = [ 1 for z in range(Z) ]
        for i in range(0,Z,2):
            if i >= Z-Y:
                b3=random.uniform((i-(Z-Y))/Y,(i-(Z-Y)+1)/Y)
                con[i] = b3
                con[i+1] = b3
        return con
    
    elif(situation == 5):
        ''' servers are between 0 and 1, connections and usres have value of 1'''
        con = [ 1 for z in range(Z) ]
        for i in range(0,Z,2):
            if i < Y:
                b4=random.uniform(i/Y,(i+1)/Y)
                con[i] =  b4
                con[i+1] =  b4
        return con
    
    elif(situation == 6):
        '''network failure'''
        con = [ 1 for z in range(Z) ]
        for i in range(0,Z,2):
            # Servers
            if i < Y: 
                b0 = servervalue(i)
                con[i] = b0
                con[i+1] = b0
            # Users
            elif i > (Z - ((Y)+1)): 
                b6 = random.uniform((i-(Z-Y))/Y,(i-(Z-Y)+1)/Y)
                con[i] = b6
                con[i+1] = b6
            # Connections
            else: 
                b5 = random.rand()
                if b5 < 0.4:
                    b7 = b5
                    b7 = 0
                    con[i] = b7 
                    con[i+1] = b7
                else:
                    b8 = b5
                    b8 = 1
                    con[i] = b8 
                    con[i+1] = b8
        return con
    else:
        print(' Chose a number between 0 and 6')
        

def A_eq(server):
    ''' Implementing kirchhoff law for left side of equation matrix'''
    
    N = server
    T = N*N - 2*N
    I = 2*N*N - 2*N - 2*(N-1)
    
    matrix = [ [ 0 for i in range(I) ] for j in range(T) ]
    tem_arr = []
    a=0
    
    switchA, switchAA, switchAAA = 1, 1, 1
    switchC, switchCC, switchCCC = 1, 1, 1
    
    # First in the grid
    for i in range(1,T+1): 
        if (i == 1):
            a = a + 1
            b = a + N
            c = b + N - 1
            matrix[i-1][a-1] = 1
            matrix[i-1][b-1] = 1
            matrix[i-1][c-1] = -1
            tem_arr.append(a)
            tem_arr.append(b)
            tem_arr.append(c)
         
        # Grid position - far left
        elif (((i-1) % N) == 0): 
            a = N + a
            b = a + N
            c = b + N - 1
              
            if(switchA):
                matrix[i-1][a-1] = 1
                switchA = 0
            else:
        	    matrix[i-1][a-1] = 1
        	    switchA = 1
               
            if(switchC):
        	    matrix[i-1][c-1] = -1
        	    switchC = 0
            else:
        	    matrix[i-1][c-1] = -1
        	    switchC = 1
                    
            if b in tem_arr:
                matrix[i-1][b-1] = -1
            else:
                tem_arr.append(b)
                matrix[i-1][b-1] = 1
                    
        # Grid position - far right
        elif (i == T or ((i % N) == 0)): 
            a = a + 1
            b = a + N
            d = b - 1
            c = b + N - 1
                    
            if(switchAA):
                matrix[i-1][a-1] = 1
                switchAA = 0
            else:
                matrix[i-1][a-1] = 1
                switchAA = 1
      
            if(switchCC):
        	    matrix[i-1][c-1] = -1
        	    switchCC = 0
            else:
        	    matrix[i-1][c-1] = -1
        	    switchCC = 1    
                
            if d in tem_arr:
                matrix[i-1][d-1] = -1 
            else:
                tem_arr.append(d)
                matrix[i-1][d-1] = 1
        
        # Grid position - middle
        else: 
            a = a + 1
            b = a + N
            c = b + N - 1
            d = b - 1
       
            if (switchAAA == N+1):
        	    switchAAA = 1
    
            if(switchAAA <= N-2):
        	    matrix[i-1][a-1] = 1
        	    switchAAA = switchAAA + 1
            else:
        	    matrix[i-1][a-1] = 1
        	    switchAAA = switchAAA + 1    
    
            if (switchCCC == N+1): 
        	    switchCCC = 1
    
            if(switchCCC <= N-2):
        	    matrix[i-1][c-1] = -1
        	    switchCCC = switchCCC + 1
            else:
        	    matrix[i-1][c-1] = -1 
        	    switchCCC = switchCCC + 1  
     
            if b in tem_arr:
                matrix[i-1][b-1] = -1
            else:
                tem_arr.append(b)
                matrix[i-1][b-1] = 1     
                
            if d in tem_arr:
               matrix[i-1][d-1] = -1
            else:
                tem_arr.append(d)
                matrix[i-1][d-1] = 1
              
    return matrix
 

def B_eq():
    ''' Matrix of zeros for the right side of kirchhoff law equation '''
    return np.full(node,0)


def cost(var = 0):
    '''Cost function - maximizing input or output currents'''
    
    if(var == 0):
        '''maximize only servers'''
        g = [] 
        for i in range(current):
            if i < server: 
                g.append(-1)
                
            else:
                g.append(0)
        return g
    
    elif(var == 1):
        ''' maximize users only'''
        u = [] 
        for i in range(current):
            if i >= (current-server): 
                u.append(-1)
                
            else:
                u.append(0)
        return u
    
    elif(var == 2):
        '''maximize users and servers'''
        cost = [ 0 for z in range(current) ]
        for i in range(current):
            if i < server:
                cost[i] = -1
                
            elif i > (current - (server+1)):
                cost[i] = -1
        return cost
    else:
        print('Chose a number between 0 and 2')
        

def lin_prog_result(cost, A_ineq, B_ineq, A_eq, B_eq):
    
    result = linprog(c=cost, 
                     A_ub=A_ineq, 
                     b_ub=B_ineq, 
                     A_eq=A_eq, 
                     b_eq=B_eq, 
                     bounds=(-1,1), 
                     method='interior-point')

    R = result.x
    AbsI= np.abs(R)
    tx = 0
    B_ineq2=[]
    
    for i in range(current):
        B_ineq2.append(B_ineq[tx])
        tx = tx + 2
     
    return B_ineq2, R, AbsI
    

def plot(connection, R, AbsI):
    
    x1 = [] 
    for g in range(1,5):
        x1.append(g)
        
    x2 = [] 
    for g in range(15,19):
        x2.append(g)    
    
    x = []  
    for k in range(1,current+1):
        x.append(k)
    
    stre = [] 
    for k1 in range(1,server+1):
        stre.append(k1)
       
    streR=[0]*server 
    for r1 in range(0,server):
        streR[r1] = R[r1] 
        
    upo = [] 
    for k2 in range(current-server+1,current+1):
        upo.append(k2)
      
    upoR=[] 
    for r2 in range(0,current):
        if r2>(current-server-1):
            upoR.append(R[r2])     
       
    def addlabels(x,y):
        for i in range(len(x)):
            plt.text(i,y[i],y[i],fontsize=9)
    
    for i in range(len(connection)):
        connection[i] = round(connection[i],2)
       
   
     
    ''' First plot: Current Values'''
     
    plt.scatter(x, connection, color='black', label='Connections value', alpha = 1,s=12)
    text = connection 
    # Loop for annotation of all points
    for i in range(len(x)):
        plt.annotate(text[i], (x[i], connection[i]), fontsize=8)
    
    plt.bar(x, R, color ='maroon', width = 0.4)
    plt.bar(upo, upoR, width = 0.4, label= 'Users')
    plt.bar(stre, streR, width = 0.4, label= 'Servers')
        
    plt.legend(title='',loc='best',fontsize=8)
    plt.xlabel('Zaporedna številka N toka')
    plt.ylabel('Amplitude and Direction of Current I')
    plt.title(r'Current Values of '+str(server)+'x'+str(server)+' Network Grid')
    plt.grid() 
    plt.show()
    
    
    ''' Second plot: Absolute Value of Currents'''
    
    plt.plot(x,connection,'o',markersize=5,color='black',   label = 'Connection value')
    plt.plot(x, AbsI,'o--',markersize=3, color ='orange',  label = 'Calculated value')
    
    plt.legend(title='',loc='upper right', fontsize=8)
    plt.xlabel('Zaporedna številka N toka')
    plt.ylabel('Amplitude of Current I')
    plt.title(r'Absolute Values of Currents for '+str(server)+'x'+str(server)+' Network Grid \n and Calculated Values')
    plt.grid()
    plt.show()
    
    
    ''' Third plot: Current Distribution Map'''
    
    x=[]
    y=[]
    x2=[1,2]
    y2=[2,3]
    
    index3 = 0
    N = server
    
    for B in range(N-1):
        for A in range(N):
            x =[A,A]
            y = [B,B+1]
                   
            if R[index3]<0: 
                plt.plot(x,y, '-o',linewidth=R[index3]*5,color='blue')
            else:
                plt.plot(x,y, '-o',linewidth=R[index3]*5,color='red')
            index3 = index3 + 1    
               
        if B < N-2:
            for C in range(N-1): 
                x2 =[C,C+1]
                y2 = [B+1,B+1]
                
                if R[index3]<0:
                    plt.plot(x2,y2, '-',linewidth=R[index3]*5,color='blue')
                else:
                    plt.plot(x2,y2, '-',linewidth=R[index3]*5,color='red')
                
                index3 = index3 + 1
          
    plt.title('Distribution of Currents on '+str(server)+'x'+str(server)+
              ' Network Grid \n Red = Positive Current || Blue = Negative Current')  
    plt.axis('off')
    plt.show()


def main():
    

    connection, R, AbsI  = lin_prog_result(cost(maximize), A_ineq(), B_ineq(situation), A_eq(server), B_eq())
    plot(connection, R, AbsI)
    
    return

if __name__ == "__main__":
    main()
    
    
    
    
    
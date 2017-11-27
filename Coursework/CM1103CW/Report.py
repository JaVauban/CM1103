from Template import *

def doubleQueue(alpha, beta, time=480):
    # ta : time to next customer arrival
    # ts : time until customer is finished with teller
    # c : current time
    # Q : current queue length
    # maxQ : the size of the longest queue
    
    ta = 0
    ts = 0
    c = 0
    maxQ = 0
    Q = 1
    
    # Repeatedly increment C to the time of the next critical event - either a customer arriving or a customer leaving (Being finished)
    
    while c < time:
        if(ta < ts):
            ts -= ta
            #######
            c += ta
            Q+= 1
            maxQ = Q if Q > maxQ else maxQ
            ta = nextTime(alpha)
            #######
        else:
            ta -= ts
            c += ts
            Q -= 2
            ts = nextTime(beta)
            
        while(Q == 0):
            #######
            c += ta
            Q+= 1
            maxQ = Q if Q > maxQ else maxQ
            ta = nextTime(alpha)
            #######
    return maxQ


# Case 1: New equipment that reduces the avg service time per customer
# i.e. reduction in Beta

sample = 15

random.seed(64)
list = []
idList = []
for i in range(15, 1, -1):
    idList.append(i)
    samples=[]
    for j in range(sample):
        samples.append(singleQueue(5, i, 500))
    result = 0
    for j in range(len(samples)):
        result += samples[j] 
    result /= len(samples)
    list.append(result)
    
plt.plot(idList, list, antialiased=True)
plt.ylabel("Maximum queue length over 500 minutes")
plt.xlabel("Mean time taken per customer")
plt.title("Graph illustrating effect of reduction in mean service time on the maximum queue length")
plt.gca().invert_xaxis()
plt.show()


# Case 2: A second teller is introduced

sample = 15
random.seed(64)
idList = [1, 2]
list = []
result = 0
for i in range (sample):
    result += singleQueue(5, 3, 500)
result /= sample
list.append(result) 

result = 0
for i in range (sample):
    result += doubleQueue(5, 3, 500)
result /= sample
list.append(result)

plt.plot(idList, list, antialiased=True)
plt.ylabel("Maximum queue length over 500 minutes")
plt.xlabel("Number of tellers")
plt.title("Graph illustrating effect of adding an additional teller on the maximum queue length")
plt.show()
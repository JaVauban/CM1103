#!/usr/bin/env python

#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import random
import math
import csv

#plt.plot([2,2,3,4])


# Question 2
def Question2():
    i = 1.1
    idList = []
    list = []
    while(i <= 10):
        list.append(i / (1-i))
        idList.append(i)
        i+=0.1
    plt.plot(idList, list, antialiased=True)
    
    plt.ylabel('Mean Queue Length')
    plt.xlabel("Beta/Alpha")
    plt.title("Mean queue length variation with b/a increase")
    plt.show()



def nextTime(mean):
    return -mean * math.log(1 - random.random())


def theoreticalMeanQueueLength(alpha, beta):
    """
    >>> theoreticalMeanQueueLength(10, 2)
    0.25
    >>> theoreticalMeanQueueLength(5, 1)
    0.25
    >>> theoreticalMeanQueueLength(4, 2)
    1.0
    >>> theoreticalMeanQueueLength(5.5, 1.3)
    0.3095238095238095
    >>> theoreticalMeanQueueLength(5.5, 0)
    0.0
    >>> theoreticalMeanQueueLength(2, 1)
    1.0
    >>> type(theoreticalMeanQueueLength(10, 2))
    <class 'float'>
    """
    # Returns float
    # Could create a float here to store b/a but that's a memory allocation that's probably worse than a 2nd division
    beta = float(beta)
    alpha = float(alpha)
    return (beta / alpha) / (1 - (beta / alpha))


def checkMean(mean, iterations=10000):
    """
    >>> random.seed(57)
    >>> checkMean(5, 10)
    6.309113224728108
    >>> random.seed(57)
    >>> checkMean(5, 1000)
    4.973347344130324
    >>> random.seed(57)
    >>> checkMean(5, 100000)
    4.988076126529703
    >>> random.seed(57)
    >>> checkMean(195, 100000)
    194.53496893466047
    >>> random.seed(57)
    >>> checkMean(195)
    196.71853828860912
    >>> random.seed(57)
    >>> checkMean(31)
    31.273203522804728
    >>> type(checkMean(31, 5))
    <class 'float'>
    """
    resultMean = mean
    for x in range(iterations):
        resultMean += nextTime(mean)
    resultMean /= iterations
    return resultMean
    # This one is kinda bullshit. Random seeding is seemingly different than what doctest author intended. Why check the floats so specifically? 


def readExperimentParameters(filename):
    """
    >>> readExperimentParameters('experiments.csv')[0]
    (10, 2, 480)
    >>> len(readExperimentParameters('experiments.csv'))
    5
    >>> readExperimentParameters('experiments.csv')[3]
    (20, 2, 8)
    >>> readExperimentParameters('experiments.csv')[2]
    (20, 15, 240)
    >>> type(readExperimentParameters('experiments.csv')[1])
    <class 'tuple'>
    """    
    
    csvFile = csv.reader(open(filename))
    pythonSucks = next(csvFile)
   
    data = []
    for row in csvFile:
        list = []
        for i in range(len(row)):
            if(row[i+1] == ""):
                list.append(int(row[i]))
                break
            elif(row[i+1] == "h"):
                list.append(int(row[i]) * 60)
                break
            else:
                list.append(int(row[i]))
            
        data.append(tuple(list))
    return data


def singleQueue(alpha, beta, time=480):
    """
    >>> random.seed(57)
    >>> singleQueue(10, 3, 480)
    3
    >>> random.seed(101)
    >>> singleQueue(5, 3, 480)
    6
    >>> random.seed(101)
    >>> singleQueue(5, 3)
    6
    >>> random.seed(935)
    >>> singleQueue(10, 9, 280)
    10
    >>> type(singleQueue(10, 9, 280))
    <class 'int'>
    """
    # Implement algorithm above in PDF, takes parameters, and returns the MAX queue length
    
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
    
    # Can't simplify this because I can't make a function that takes values by reference without using globals.
    # Or I could use mutable lists to store them, but that's an affront to computer science.
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
            Q -= 1
            ts = nextTime(beta)
            
        while(Q == 0):
            #######
            c += ta
            Q+= 1
            maxQ = Q if Q > maxQ else maxQ
            ta = nextTime(alpha)
            #######
    return maxQ
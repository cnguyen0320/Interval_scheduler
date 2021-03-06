#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 23:08:16 2018
@author: cnguyen

Interval Scheduling 
"""

import random, sys
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

'''A class that contains the interval request'''
class request:
    def __init__(self, start_time, end_time, weight = 1):
        assert start_time < end_time
        self.start = start_time
        self.end = end_time
        self.weight = weight
        
    #the to string method for the object
    def __str__(self):
        return "(%d, %d)" %(self.start, self.end)

'''If this option is selected, the program will create a random list of interval requests'''
def randomize():
    #Assume the start time is 0 and the stop time is 100
    GLOBAL_START= 0
    GLOBAL_STOP= 100
    
    #Create the list of intervals randomly
    for i in range(random.randint(10,30)):
        request_start = random.randint(GLOBAL_START, GLOBAL_STOP-1)
        request_stop = random.randint(request_start+1, GLOBAL_STOP)
        interval_list.append(request(request_start, request_stop))

'''If this option is selected, the program will prompt user for a list of interval requests'''
def enter_manually():
    print("Enter a blank value at any time to complete your list")
    while True:
        try:
            start = input("Enter request start time: ")
            
            if "".join(start.split())== "":
                if len(interval_list) < 1: raise IndexError
                break
            
            stop = input("Enter request finish time: ")
            
            if "".join(stop.split())== "":
                if len(interval_list) < 1: raise IndexError
                break
            
            interval_list.append(request(float(start), float(stop)))
            print("Request added successfully\n")
            
        except ValueError:
            print("ERROR: Invalid type. Enter a number.\n")
        except AssertionError:
            print("ERROR: End time must be greater than start time.\n")
        except IndexError:
            print("ERROR: Must have at least 1 request\n")

'''If this option is selected, the program will Read a file and parses it for request intervals'''
def read_list():
    if len(sys.argv) <3:
        print("invalid command line syntax. Try 'python interval_scheduling.py <modeFlag> <file.txt>")
        exit(1)
    try:
        #opens the file and takes pairs of start and finish times to create new requests
        with open(sys.argv[2], 'r') as file:
            print("%s loaded sucessfully" % sys.argv[2])
            content = file.readlines()
            for line in content:
                for char in ['(', ')', '[',']','<','>', '{', '}',',']:
                    line = line.replace(char, ' ')
                line = line.split()
                try:
                    interval_list.append(request(float(line[0]), float(line[1])))
                except ValueError:
                    print("Request (%s, %s) omitted. Format error" %(line[0], line[1]))
                except AssertionError:
                    print("Request (%s, %s) omitted. Start/End time agreement error"%(line[0], line[1]))
                except IndexError:
                    pass
                
        assert len(interval_list) > 0
        
    except FileNotFoundError:
        print("ERROR: File %s not found" % sys.argv[2])
        exit(1)
    except AssertionError:
        print("ERROR: File needs to contain at least 1 valid request interval")
        exit(1)
        

'''Uses the earliest finish time as a heuristic for best next scheduled interval and creates a schedule'''
def create_schedule():
    print("Initial list of requests:")
    for req in interval_list:
        print(req)  
    #sorts the list by earliest finish time    
    interval_list.sort(key = lambda req: req.end, reverse = False)
    
    scheduled_list.append(interval_list[0])
    for req in interval_list[1:]:
        if req.start >= scheduled_list[-1].end:
            scheduled_list.append(req)
    
    print("Optimal schedule (%d/%d requests fulfilled):" % (len(scheduled_list), len(interval_list)))
    for request in scheduled_list:
        print(request)

'''Plots the requests and highlights the scheduled requests'''
def plot_schedule():
    #sort the list by start time for nice plot formatting
    interval_list_by_start = sorted(interval_list, key=lambda req: req.start, reverse = True) 
    
    #Add the requests onto the plot
    for idx, req in enumerate(interval_list_by_start):
        if req in scheduled_list:
            plt.plot([req.start,req.end],[idx,idx], "ro--", label = "scheduled")
        else:
            plt.plot([req.start,req.end],[idx,idx], "bo--", label = "omitted")
    
    #format plot
    ax = plt.gca()
    ax.set_xlabel('Request time')
    ax.set_title('Interval Scheduler')
    ax.axes.get_yaxis().set_ticks([])
    #format legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    #display plot
    plt.show()
#%%  
global interval_list
global scheduled_list 
interval_list = []
scheduled_list = []

#Parses the command line args to check the mode
if len(sys.argv) <= 1 or sys.argv[1]== '0':
    randomize()

elif sys.argv[1]== '1':
    enter_manually()

elif sys.argv[1] == '2':
    read_list()

else:
    print("invalid command line syntax. Try 'python interval_scheduling.py <modeFlag> <file.txt>")
    exit(1)

create_schedule()
plot_schedule()
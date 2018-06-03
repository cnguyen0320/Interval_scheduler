#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 23:08:16 2018
@author: cnguyen

Interval Scheduling 
"""

import random, sys

class request:
    def __init__(self, start_time, end_time, weight = 1):
        assert start_time < end_time
        self.start = start_time
        self.end = end_time
        self.weight = weight
        
    #the to string method for the object
    def __str__(self):
        return "(%d, %d)" %(self.start, self.end)

def randomize():
    #Assume the start time is 0 and the stop time is 100
    GLOBAL_START= 0
    GLOBAL_STOP= 100
    
    #Create the list of intervals
    for i in range(random.randint(10,30)):
        request_start = random.randint(GLOBAL_START, GLOBAL_STOP-1)
        request_stop = random.randint(request_start+1, GLOBAL_STOP)
        interval_list.append(request(request_start, request_stop))

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

def create_schedule():
    scheduled_list = [interval_list[0]]
    for req in interval_list[1:]:
        if req.start >= scheduled_list[-1].end:
            scheduled_list.append(req)
    
    print("Optimal schedule (%d requests fulfilled):" % len(scheduled_list))
    for request in scheduled_list:
        print(request)
        
    return scheduled_list

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
                line = line.replace(',', ' ').split()
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
        

#%%
interval_list = []

if len(sys.argv) <= 1 or sys.argv[1]== '0':
    randomize()

elif sys.argv[1]== '1':
    enter_manually()

elif sys.argv[1] == '2':
    read_list()

else:
    print("invalid command line syntax. Try 'python interval_scheduling.py <modeFlag> <file.txt>")
    exit(1)

#sorts the list by earliest finish time
interval_list.sort(key = lambda req: req.end, reverse = False)
print("Initial list of requests:")
for req in interval_list:
    print(req)

scheduled_list = create_schedule()
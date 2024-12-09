#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: Prasad Mistry
Student Number: 111964193
Student Email: pmistry21@myseneca.ca
Course: OPS445
Section: ZAA
Semester: Fall 2024

The python code in this file is original work written by
Prasad Mistry. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: Assignment 2 completed.

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Prints sizes in human readable format")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
# create argparse function
# -H human readable
# -r running only

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    ...
# percent to graph function
    hashes = int(percent * length)  
    return '#' * hashes + ' ' * (length - hashes)

def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    ...
    f = open('/proc/meminfo', 'r') 
    for each_one in f:
        if each_one.startswith('MemTotal:'):
            result = int(each_one.split()[1]) 
            f.close() 
            return result
    f.close()  

def get_avail_mem() -> int:
    "return total memory that is available"
    ...
    f = open('/proc/meminfo', 'r')  
    for each_one_2 in f:
        if each_one_2.startswith('MemAvailable:'):
            result = int(each_one_2.split()[1])  
            f.close()  
            return result
    f.close() 

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    ...
    output_pids = os.popen('pidof ' + app_name).read().strip()
    if output_pids:
            return output_pids.split()  
    return []

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    ...
    total_rss = 0
    try:
        f = open('/proc/' + proc_id + '/smaps', 'r') 
        for each_one_3 in f:
            if each_one_3.startswith('Rss'):
                total_rss = total_rss + int(each_one_3.split()[1])  
        f.close()  
    except FileNotFoundError:
        return 0  
    return total_rss

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:
        ...
        memory_total = get_sys_mem()
        memory_available = get_avail_mem()
        memory_used = memory_total - memory_available
        percentage_used = memory_used / memory_total
        graph = percent_to_graph(percentage_used, args.length)
        if args.human_readable:
            print("Memory         [" + graph + " | " + str(round(percentage_used * 100)) + "%] " + bytes_to_human_r(memory_used) + "/" + bytes_to_human_r(memory_total))
        else:
            print("Memory         [" + graph + " | " + str(round(percentage_used * 100)) + "%] " + str(memory_used) + "/" + str(memory_total))
    else:
        ...
        pids = pids_of_prog(args.program)
        if pids:
            program_memory_total = 0
            for each_one_4 in pids:
                program_memory_total = program_memory_total + rss_mem_of_pid(each_one_4)
            percentage_used = program_memory_total / get_sys_mem()
            graph = percent_to_graph(percentage_used, args.length)
            if args.human_readable:
                print(args.program + "        [" + graph + " | " + str(round(percentage_used * 100)) + "%] " + bytes_to_human_r(program_memory_total) + "/" + bytes_to_human_r(get_sys_mem()))
            else:
                print(args.program + "        [" + graph + " | " + str(round(percentage_used * 100)) + "%] " + str(program_memory_total) + "/" + str(get_sys_mem()))
        else:
            print(args.program + " not found.")
    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.


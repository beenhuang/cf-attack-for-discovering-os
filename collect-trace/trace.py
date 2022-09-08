#!/usr/bin/env python3

import argparse
import os
import sys
import csv
import re

# argument parser:
parser = argparse.ArgumentParser()

# 1. input: 
parser.add_argument("--in", required=True, help="extract dataset")

# 2. output: 
parser.add_argument("--out", required=True, help="save")

# 3. mode: 
parser.add_argument("--mode", required=True, type=str, help="label")

args = vars(parser.parse_args())


def get_files_of_all_nodes(dir, mode):

    c_files = []
    r_files = []
    hs_file = []

    # [1] get client files:
    for i in range(100):
        c_file = os.path.join(dir, 'shadow.data', 'hosts', f'client{i+1}', f'client{i+1}.tor.1000.stdout')
        c_files.append(c_file)

    # [2] [FIXME]: get relay files:
    i=0
    
    while i < 38:
        if i<9:
            r_file = os.path.join(dir, 'shadow.data', 'hosts', f'relay{i+1}exitguard', f'relay{i+1}exitguard.tor.1000.stdout')
            r_files.append(r_file)
            i += 1
            continue
        elif i>=9 and i<12:
            i += 1
            continue
        elif i>=12 and i<38: 
            r_file = os.path.join(dir, 'shadow.data', 'hosts', f'relay{i+1}guard', f'relay{i+1}guard.tor.1000.stdout')
            r_files.append(r_file)
            i += 1
            continue    
    
    # [3] get hs file:
    if mode == "hs" :
        hs_file.append(os.path.join(dir, 'shadow.data', 'hosts', 'hiddenserver', 'hiddenserver.tor.1000.stdout')) 


    return c_files, r_files, hs_file  

def get_one_host_circs(file, tag):

    circs = []
    
    regexp = re.compile('HUANG')
    regexp2 = re.compile('\$\[.+\]')

    with open(file, 'r') as f:
        for line in f.readlines():
            if regexp.search(line):
                l = regexp2.search(line)
                c = re.sub("[\$\[\]]+", "", l.group()).split(",")
            
                # dList[0] is a tag, and dList[1] is a circ ID
                if c[0] == tag and c[1] not in circs:   
                    circs.append(c[1])
    
    return circs     


def get_circs_of_all_hosts(files, tag):

    circs = {}
    
    for file in files:
        # get host name.
        name = file.split('/')[-2]
        
        # get a circuit id list of one client
        circs[name] = get_one_host_circs(file, tag)
    
    return circs   


def get_one_relay_traces(r_file):
    r_traces = {}
    
    regexp = re.compile('<HUANG')
    regexp2 = re.compile('\$\[.+\]')

    with open(r_file,'r') as f:
        for line in f.readlines():
            if regexp.search(line):
                circ = regexp2.search(line)
                cell = re.sub("[\$\[\]]+", "", circ.group()).split(",")
                
                # cell[0],cell[1],cell[2]: circ_ID, cell_type, direction
                if cell[0] not in r_traces:
                    r_traces[cell[0]] = [f"{cell[1]}:{cell[2]}"]
                else:
                    r_traces[cell[0]].append(f'{cell[1]}:{cell[2]}')
                    
    return r_traces     

def match_host_to_relay(all_c_circs, r_traces, r_name, tag):

    lines = []

    if not bool(all_c_circs):
        return
        
    r_circs = r_traces.keys()
    
    for c_name,c_circs in all_c_circs.items():
        circs = [cid for cid in c_circs if cid in r_circs]

        for circ in circs:
            line = []

            line.extend([c_name, r_name, circ, tag])
            line.extend(r_traces[circ])

            lines.append(line)


    return lines 
      

def get_match_trace(all_c_circs, r_files, mode):

    lines = []

    # 
    for r_file in r_files:
        # get relay name.
        r_name = r_file.split('/')[-2]
        
        # get relay's all circuits with cell data.
        r_traces = get_one_relay_traces(r_file)

        for cid in list(r_traces.keys()):
            if len(r_traces[cid]) < 9000:
                del r_traces[cid] 

        if not bool(r_traces):
            print(f'{r_name} traces are empty.')
            continue        


        lines.extend(match_host_to_relay(all_c_circs, r_traces, r_name, "general"))

        print(f"[{r_name}] traces are not empty.")   


    return lines            


def get_match_trace2(all_ipc_circs, all_rpc_circs, ip_hs_circs, rp_hs_circs, r_files):

    lines = []

    for r_file in r_files:
        # get relay name.
        r_name = r_file.split('/')[-2]
        
        # get relay's all circuits with cell data.
        r_traces = get_one_relay_traces(r_file)

        # 
        lines.extend(match_host_to_relay(all_ipc_circs, r_traces, r_name, "IpClient"))
        lines.extend(match_host_to_relay(ip_hs_circs, r_traces, r_name, "IpHS"))
        
        #
        for cid in list(r_traces.keys()):
            if len(r_traces[cid]) < 9000:
                del r_traces[cid] 
        #
        if not bool(r_traces):
            print(f'[{r_name}] traces are empty.')
            continue                
            
        # match RP cricuits.
        lines.extend(match_host_to_relay(all_rpc_circs, r_traces, r_name, "RpClient"))
        lines.extend(match_host_to_relay(rp_hs_circs, r_traces, r_name, "RpHS"))
        
        print(f"[{r_name}] traces are not empty.")   

    return lines     


def extract_general_trace(c_files, r_files):

    # 1. get client circuit-id
    all_c_circs = get_circs_of_all_hosts(c_files, "general")

    # 2. get dataset
    lines = get_match_trace(all_c_circs, r_files, "general")


    return lines


def extract_hs_trace(c_files, r_files, hs_file):

    # 1. get ip-client/rp-client/ip-hs/rp-hs circuit-id
    all_ipc_circs = get_circs_of_all_hosts(c_files, "IpClient")
    all_rpc_circs = get_circs_of_all_hosts(c_files, "RpClient")

    ip_hs_circs = get_circs_of_all_hosts(hs_file, "IpHS")
    rp_hs_circs = get_circs_of_all_hosts(hs_file, "RpHS")

    # 2. 
    lines = get_match_trace2(all_ipc_circs, all_rpc_circs, ip_hs_circs, rp_hs_circs, r_files)


    return lines


#
def main():
    print(f"-------  [{os.path.basename(__file__)}]: start to run [{args['in']}]  -------")

    # [1] get client/relay/hs files
    c_files, r_files, hs_file = get_files_of_all_nodes(os.path.join(os.getcwd(), "collect-trace", args["in"]), args["mode"])


    # [2]
    if args["mode"] == "general":
        lines = extract_general_trace(c_files, r_files)
        file = os.path.join(os.getcwd(), "dataset", "general-trace",args["out"])

    elif args["mode"] == "hs":
        lines = extract_hs_trace(c_files, r_files, hs_file)
        file = os.path.join(os.getcwd(), "dataset", "hs-trace", args["out"])

    else :
        sys.exit(f"[ERROR] unrecognized mode : [{args['mode']}]")


    print(f"[EXTRACTED] traces from {args['in']} in {args['mode']} mode")    


    # [3] output
    with open(file, "w") as f:    
        writer = csv.writer(f, delimiter=",")
        writer.writerows(lines)    

    print(f"[SAVED] traces to the {args['out']}")    


    print(f"-------  [{os.path.basename(__file__)}]: completed successfully  -------")   

        

if __name__ == "__main__":
    main()  
import shlex
import subprocess
import itertools
from helper import get_cfgs, get_outfile_name
import fnmatch
import datetime
import os, re, sys
import matplotlib.pyplot as plt
import numpy as np
import csv
import concurrent.futures
import time

result_dir = "./results/"
output_f = "test"

now = datetime.datetime.now()
strnow=now.strftime("%Y%m%d-%H%M%S")


def network_sweep():
    wl = 'YCSB'
    nalgos=['NO_WAIT','WAIT_DIE','MVCC','MAAT','TIMESTAMP','CALVIN']
    ndelay = [0, 1, 2, 5, 10, 15, 20]
    # network delay in nanoseconds
    ndelay = [int(n * 1000) for n in ndelay]
    nnodes = [2]
    txn_write_perc = [0.5]
    tup_write_perc = [0.5]
    load = [10000]
    tcnt = [4]
    skew = [0.6]
    base_table_size = 2097152 * 8
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","NETWORK_DELAY_TEST","NETWORK_DELAY","SET_AFFINITY"]
    exp = [[wl,n,algo,base_table_size * n,tup_wr_perc,txn_wr_perc,ld,sk,thr,"true",d,"false"] for thr,txn_wr_perc,tup_wr_perc,sk,ld,n,d,algo in itertools.product(tcnt,txn_write_perc,tup_write_perc,skew,load,nnodes,ndelay,nalgos)]
    return fmt,exp


def ycsb_partitions_abort():
    wl = 'YCSB'
    nnodes = [4]
    algos=['CALVIN']
    load = [10000]  
    nparts = [4]
    mpr = [0, 0.2, 0.4, 0.6, 0.8, 1]
    
    # mpr = [0.8, 1]
    # mpr = [0, 0.2]
    # mpr = [0.2, 0.4]

    base_table_size = 2097152*8
    txn_write_perc = [0.5]
    tup_write_perc = [0.5]
    tcnt = [4]
    skew = [0]
    rpq = 16
    fmt = ["SKEW_METHOD", "WORKLOAD","REQ_PER_QUERY","PART_PER_TXN","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","STRICT_PPT","YCSB_ABORT_MODE", "MPR"]
    exp = [["HOT", wl,rpq,p,n,algo,base_table_size * n,tup_wr_perc,txn_wr_perc,ld,sk,thr,1,'true', e] for thr,txn_wr_perc,tup_wr_perc,algo,sk,ld,n,p,e in itertools.product(tcnt,txn_write_perc,tup_write_perc,algos,skew,load,nnodes,nparts, mpr)]
    return fmt, exp


def ycsb_latency_breakdown():
    wl = 'YCSB'
    nnodes = [4]
    nalgos=['NO_WAIT','WAIT_DIE','MVCC','MAAT','TIMESTAMP']
    load = [10000]  
    nparts = [4]

    mpr = [0.4]
    base_table_size = 2097152*8
    txn_write_perc = [0.9, 0.1]
    tup_write_perc = [0.5]

    tcnt = [4]
    skew = [0]
    rpq = 16

    fmt = ["SKEW_METHOD", "WORKLOAD","REQ_PER_QUERY","PART_PER_TXN","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","STRICT_PPT","YCSB_ABORT_MODE", "MPR"]
    exp = [["HOT", wl,rpq,p,n,algo,base_table_size * n,tup_wr_perc,txn_wr_perc,ld,sk,thr,1,'true', e] for thr,txn_wr_perc,tup_wr_perc,algo,sk,ld,n,p,e in itertools.product(tcnt,txn_write_perc,tup_write_perc,nalgos,skew,load,nnodes,nparts, mpr)]

    return fmt, exp


def deploy_local(output_f, cfgs):
    pids = []
    print("Deploying: {}".format(output_f))
    nnodes = cfgs["NODE_CNT"]
    ntotal = nnodes + nnodes

    for n in range(ntotal):
        if n < nnodes:
            cmd = "./rundb -nid{}".format(n)
        elif n < (ntotal):
            cmd = "./runcl -nid{}".format(n)
        else:
            assert(False)

        print(cmd)
        cmd = shlex.split(cmd)
        ofile_n = "{}{}_{}.out".format(result_dir, n, output_f)
        ofile = open(ofile_n,'w')
        p = subprocess.Popen(cmd, stdout=ofile, stderr=ofile)
        pids.insert(0,p)
    for n in range(ntotal):
        pids[n].wait()


def deploy_remote(output_f, cfgs):
    cfg_fname = "cloudlab.txt"
    uname = "bxqml233"
    machines = []
    with open(cfg_fname, "r") as f:
        for line in f:
            machines.append(line.strip())

    nnodes = cfgs["NODE_CNT"]
    nclnodes = nnodes # by default
    ntotal = int(nnodes) + int(nclnodes)

    # One for server, one for client
    machines = machines + machines
    assert len(machines) == ntotal

    # Copy it twice, one for db, one for cl
    os.system(f"cat {cfg_fname} > ifconfig.txt")
    os.system(f"cat {cfg_fname} >> ifconfig.txt")

    if cfgs["WORKLOAD"] == "TPCC":
        files = ["./rundb","./runcl","./ifconfig.txt","./benchmarks/TPCC_short_schema.txt"]
    elif cfgs["WORKLOAD"] == "YCSB":
        files = ["./rundb","./runcl","./ifconfig.txt","./benchmarks/YCSB_schema.txt"]

    # Copy essential files to remote nodes
    #  bxqml233@pc88.cloudlab.umass.edu
    # scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./ifconfig.txt $node:~/deneva

# Parallel version
    scp_procs = []
    for m, f in itertools.product(machines, files):
        # cmd = "scp -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {} {}@{}:{}".format(f, uname, m, f"/users/{uname}/")
        cmd = "rsync -avz -e \'ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\' --progress {} {}@{}:{}".format(f, uname, m, f"/users/{uname}/")
        print(cmd)
        scp_procs.append(subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr))

    for p in scp_procs:
        p.wait()


    for m in machines:
        cmd = "pkill -f rundb; pkill -f runcl; sync"
        cmd = "ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{} ".format(uname, m) + cmd
        os.system(cmd)
        print(cmd)

    print("SLEEP for 10 seconds")   # wait for sync
    time.sleep(10)

    ssh_procs = []
    print("Deploying: {}".format(output_f))
    for m, cnt in zip(machines, range(ntotal)):
        exe = "./rundb" if cnt < nnodes else "./runcl"
        cmd = "env SCHEMA_PATH=\"{}\" timeout -k 8m 8m {} -nid{} ".format(f"/users/{uname}/", exe, cnt)
        cmd = "ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{} ".format(uname, m) + cmd

        ofile_n = "{}{}_{}.out".format(result_dir, cnt, output_f)
        ofile = open(ofile_n,'w')
        ssh_procs.append(subprocess.Popen(cmd, stdout=ofile, stderr=ofile, shell=True))
        print(cmd)

    for p in ssh_procs:
        p.wait()


def get_throughput(output_f):
    client = False          # We only sum up throughput from clients, since CALVIN may count a txn multiple times
    throughput = 0
    with open(output_f, "r") as f:
        for line in f:
            if "Running client" in line:
                client = True
            if "[summary]" in line:
                throughput_match = re.search(r"tput=(\d+\.\d+)", line)
                throughput = float(throughput_match.group(1))
    return throughput if client else 0


def sumup_procs(directory, pattern, exec_time):
    total_throughput = 0
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, "*"+ pattern + '*.out'):
            if str(exec_time) in filename:
                total_throughput += get_throughput(os.path.join(root, filename))
            # matches.append(os.path.join(root, filename))
    return total_throughput


def draw_line_plot(yval, xval, vval, title, xlabel, ylabel, vlabel, save_path):
    assert len(yval) == len(vval)
    colors = plt.cm.tab20(np.linspace(0, 1, len(vval)))
    markers = ['s-', 'o-', '^-', 'D-', 'x-', 'P-', '>-', '<-', '8-', 'p-', '*-']

    fig, ax = plt.subplots(figsize=(14, 8))
    for i in range(len(vval)):
        ax.plot(xval, yval[i], markers[i], color=colors[i], label=f'{vlabel}={vval[i]}')

    # Set labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(vval, loc='upper right', fontsize='small')
    plt.tight_layout()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.savefig(save_path)

    plt.clf()


def print_csv(yval, xval, vval):
    # Print xvals, vvals, and yvals to the terminal in CSV format
    writer = csv.writer(sys.stdout, delimiter='\n')
    writer.writerow(['xvals'] + xval)
    writer = csv.writer(sys.stdout, delimiter=' ')
    writer.writerow([])

    writer.writerow(vval)
    # Transpose yvals and print each row
    yvals_transposed = list(map(list, zip(*yval)))
    for i, yvals_row in enumerate(yvals_transposed):
        writer.writerow(yvals_row)


def network_sweep_plot(exec_time):
    fmt, experiments = network_sweep()
    xvals = []
    vvals = ['NO_WAIT','WAIT_DIE','MVCC','MAAT','TIMESTAMP','CALVIN']
    yvals = [[0] * 7 for _ in range(len(vvals))]
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        output_f = get_outfile_name(cfgs, fmt, ["127.0.0.1", "127.0.0.1"])
        throughput = sumup_procs(result_dir, output_f, exec_time)

        # throughput = get_throughput(output_f)

        if cfgs["NETWORK_DELAY"] not in xvals:
            xvals.append(cfgs["NETWORK_DELAY"])

        x_index = xvals.index(cfgs["NETWORK_DELAY"])
        v_index = vvals.index(cfgs["CC_ALG"])
        yvals[v_index][x_index] = throughput
    print_csv(yvals, xvals, vvals)
    draw_line_plot(yvals, xvals, vvals, 'Throughput vs Network Delay', 'Network Delay (us)', 'Throughput (txn/s)', 'CC Algorithm', 'network_sweep.png')


def ycsb_partitions_abort_plot(exec_time):
    fmt, experiments = ycsb_partitions_abort()
    xvals = [0, 0.2, 0.4, 0.6, 0.8, 1]
    vvals = ['CALVIN']
    yvals = [[0] * len(xvals) for _ in range(len(vvals))]
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        output_f = get_outfile_name(cfgs, fmt, ["127.0.0.1", "127.0.0.1", "127.0.0.1", "127.0.0.1"])
        throughput = sumup_procs(result_dir, output_f, exec_time)

        x_index = xvals.index(cfgs["MPR"])
        v_index = vvals.index(cfgs["CC_ALG"])
        yvals[v_index][x_index] = throughput
    print_csv(yvals, xvals, vvals)
    draw_line_plot(yvals, xvals, vvals, 'Throughput vs Partitions per Transaction', 'Partitions per Transaction', 'Throughput (txn/s)', 'CC Algorithm', 'ycsb_partitions_abort.png')


def execute_all(exp_func):
    global output_f, result_dir

    fmt, experiments = exp_func()
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        output_f = get_outfile_name(cfgs, fmt, [])
        # result_dir = os.path.join("results", output_f)
        output_f = output_f + strnow

# compile locally (with all static libs)
        f = open("config-std.h",'r')
        lines = f.readlines()
        f.close()
        with open("config.h",'w') as f_cfg:
            for line in lines:
                found_cfg = False
                for c in cfgs:
                    found_cfg = re.search("#define " + c + "\t",line) or re.search("#define "+ c + " ",line)
                    if found_cfg:
                        f_cfg.write("#define " + c + " " + str(cfgs[c]) + "\n")
                        break
                if not found_cfg:
                    f_cfg.write(line)

        os.system("make clean > temp.out 2>&1")
        print("Running 'make' for the job...")
        ret = os.system("make -j8 > temp.out 2>&1")

        os.system("mkdir -p {}".format(result_dir))
        os.system("cp config.h {}{}.cfg".format(result_dir, output_f))
        if execute:
            if remote:
                deploy_remote(output_f, cfgs)
            else:
                deploy_local(output_f, cfgs)


exps = []
execute = True
remote = False
cluster = None
skip = False

experiment_map = {
    "network_sweep": network_sweep,
    "ycsb_partitions_abort": ycsb_partitions_abort,
    "ycsb_latency_breakdown": ycsb_latency_breakdown,
}

if len(sys.argv) < 2:
    sys.exit("Usage: %s [-exec/-e/-noexec/-ne] [-c cluster] experiments\n \
            -exec/-e: compile and execute locally (default)\n \
            -noexec/-ne: compile first target only \
            -c: run remote on cluster; possible values: istc, vcloud\n \
            " % sys.argv[0])

for arg in sys.argv[1:]:
    if arg == "-help" or arg == "-h":
        sys.exit("Usage: %s [-exec/-e/-noexec/-ne] [-skip] [-c cluster] experiments\n \
                -exec/-e: compile and execute locally (default)\n \
                -noexec/-ne: compile first target only \
                -skip: skip any experiments already in results folder\n \
                -c: run remote on cluster; possible values: istc, vcloud\n \
                " % sys.argv[0])
    if arg == "-exec" or arg == "-e":
        execute = True
    elif arg == "-noexec" or arg == "-ne":
        execute = False
    elif arg == "-skip":
        skip = True
    elif arg == "-c":
        remote = True
        arg_cluster = True
    else:
        exps.append(arg)


ycsb_partitions_abort_plot("174851")        # A successful run on 4 nodes, cloudlab rs620


for exp in exps:
    execute_all(experiment_map[exp])

# execute_all(ycsb_partitions_abort)
# plot()
# execute_all()
# ppr_network_plot()
# network_sweep_plot("094449")

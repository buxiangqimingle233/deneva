import shlex
import subprocess
import itertools
# from helper import get_cfgs, get_outfile_name
import fnmatch
import datetime
import os, re, sys
import csv

nnodes = int(os.getenv("NODE_CNT", 4))
nclnodes = int(os.getenv("CLIENT_NODE_CNT", 4))

ntotal = nnodes + nclnodes
result_dir = "./results/"
output_f = "test"

now = datetime.datetime.now()
strnow=now.strftime("%Y%m%d-%H%M%S")

# def replace(filename, pattern, replacement):
#     with open(filename, 'r') as f:
#         s = f.read()
#     new_s = re.sub(pattern, replacement, s)
#     if s != new_s:
#         print("Replacing in {}: {} -> {}".format(filename, pattern, replacement))
#     with open(filename, 'w') as f:
#         f.write(new_s)



# Default values for variable configurations
configs = {
    "NODE_CNT" : 16,
    "THREAD_CNT": 4,
    "REPLICA_CNT": 0,
    "REPLICA_TYPE": "AP",
    "REM_THREAD_CNT": "THREAD_CNT",
    "SEND_THREAD_CNT": "THREAD_CNT",
    "CLIENT_NODE_CNT" : "NODE_CNT",
    "CLIENT_THREAD_CNT" : 4,
    "CLIENT_REM_THREAD_CNT" : 2,
    "CLIENT_SEND_THREAD_CNT" : 2,
    "MAX_TXN_PER_PART" : 500000,
    "WORKLOAD" : "YCSB",
    "CC_ALG" : "WAIT_DIE",
    "MPR" : 1.0,
    "TPORT_TYPE":"IPC",
    "TPORT_PORT":"17000",
    "PART_CNT": "NODE_CNT",
    "PART_PER_TXN": "PART_CNT",
    "MAX_TXN_IN_FLIGHT": 100,
    "NETWORK_DELAY": '0UL',
    "NETWORK_DELAY_TEST": 'false',
    "DONE_TIMER": "1 * 60 * BILLION // ~1 minutes",
    "WARMUP_TIMER": "1 * 60 * BILLION // ~1 minutes",
    "SEQ_BATCH_TIMER": "5 * 1 * MILLION // ~5ms -- same as CALVIN paper",
    "BATCH_TIMER" : "0",
    "PROG_TIMER" : "10 * BILLION // in s",
    "NETWORK_TEST" : "false",
    "ABORT_PENALTY": "10 * 1000000UL   // in ns.",
    "ABORT_PENALTY_MAX": "5 * 100 * 1000000UL   // in ns.",
    "MSG_TIME_LIMIT": "0",
    "MSG_SIZE_MAX": 4096,
    "TXN_WRITE_PERC":0.0,
    "PRIORITY":"PRIORITY_ACTIVE",
    "TWOPL_LITE":"false",
#YCSB
    "INIT_PARALLELISM" : 8, 
    "TUP_WRITE_PERC":0.0,
    "ZIPF_THETA":0.3,
    "ACCESS_PERC":0.03,
    "DATA_PERC": 100,
    "REQ_PER_QUERY": 10,
    "SYNTH_TABLE_SIZE":"65536",
#TPCC
    "NUM_WH": 'PART_CNT',
    "PERC_PAYMENT":0.0,
    "DEBUG_DISTR":"false",
    "DEBUG_ALLOC":"false",
    "DEBUG_RACE":"false",
    "MODE":"NORMAL_MODE",
    "SHMEM_ENV":"false",
    "STRICT_PPT":0,
    "SET_AFFINITY":"true",
    "LOGGING":"false",
    "SERVER_GENERATE_QUERIES":"false",
    "SKEW_METHOD":"ZIPF",
    "ENVIRONMENT_EC2":"false",
    "YCSB_ABORT_MODE":"false",
    "LOAD_METHOD": "LOAD_MAX", 
    "ISOLATION_LEVEL":"SERIALIZABLE"
}

SHORTNAMES = {
    "CLIENT_NODE_CNT" : "CN",
    "CLIENT_THREAD_CNT" : "CT",
    "CLIENT_REM_THREAD_CNT" : "CRT",
    "CLIENT_SEND_THREAD_CNT" : "CST",
    "NODE_CNT" : "N",
    "THREAD_CNT" : "T",
    "REM_THREAD_CNT" : "RT",
    "SEND_THREAD_CNT" : "ST",
    "CC_ALG" : "",
    "WORKLOAD" : "",
    "MAX_TXN_PER_PART" : "TXNS",
    "MAX_TXN_IN_FLIGHT" : "TIF",
    "PART_PER_TXN" : "PPT",
    "TUP_READ_PERC" : "TRD",
    "TUP_WRITE_PERC" : "TWR",
    "TXN_READ_PERC" : "RD",
    "TXN_WRITE_PERC" : "WR",
    "ZIPF_THETA" : "SKEW",
    "MSG_TIME_LIMIT" : "BT",
    "MSG_SIZE_MAX" : "BS",
    "DATA_PERC":"D",
    "ACCESS_PERC":"A",
    "PERC_PAYMENT":"PP",
    "MPR":"MPR",
    "REQ_PER_QUERY": "RPQ",
    "MODE":"",
    "PRIORITY":"",
    "ABORT_PENALTY":"PENALTY",
    "STRICT_PPT":"SPPT",
    "NETWORK_DELAY":"NDLY",
    "NETWORK_DELAY_TEST":"NDT",
    "REPLICA_CNT":"RN",
    "SYNTH_TABLE_SIZE":"TBL",
    "ISOLATION_LEVEL":"LVL",
    "YCSB_ABORT_MODE":"ABRTMODE",
    "NUM_WH":"WH",
}


def get_outfile_name(cfgs,fmt,network_hosts=[]):
    output_f = ""
    nettest = False
    if "NETWORK_TEST" in cfgs and cfgs["NETWORK_TEST"] == "true":
        nettest = True
#    assert "NETWORK_TEST" in cfgs
    # print(network_hosts)
    if cfgs["NETWORK_TEST"] == "true":
#assert len(network_hosts) == 2
        for host in sorted(network_hosts):
            parts = host.split(".")
            if len(parts) == 4:
                h = parts[3]
            else:
                h = host
            output_f += "{}_".format(h)

        output_f += "NETWORK_TEST_"
    else:
        #for key in sorted(cfgs.keys()):
        for key in sorted(set(fmt)):
            nkey = SHORTNAMES[key] if key in SHORTNAMES else key
            if nkey == "":
                output_f += "{}_".format(cfgs[key])
            else:
                if str(cfgs[key]).find("*") >= 0:
                    output_f += "{}-{}_".format(nkey,str(cfgs[key])[:cfgs[key].find("*")])
#                    output_f += "{}-{}_".format(nkey,str(cfgs[key]).replace('*','-t-'))
#                elif str(cfgs[key]).find("/") >= 0:
#                    output_f += "{}-{}_".format(nkey,str(cfgs[key]).replace('/','-d-'))
                else:
                    output_f += "{}-{}_".format(nkey,cfgs[key])
    return output_f

def get_cfgs(fmt,e):
    cfgs = dict(configs)
    for f,n in zip(fmt,range(len(fmt))):
        cfgs[f] = e[n]
    # For now, spawn NODE_CNT remote threads to avoid potential deadlock
    #if "REM_THREAD_CNT" not in fmt:
    #    cfgs["REM_THREAD_CNT"] = cfgs["NODE_CNT"] * cfgs["THREAD_CNT"]
#    if "PART_CNT" not in fmt:
#        cfgs["PART_CNT"] = cfgs["NODE_CNT"]# * cfgs["THREAD_CNT"]
#    if "NUM_WH" not in fmt:
#        cfgs["NUM_WH"] = cfgs["PART_CNT"]
    return cfgs

def network_sweep():
    wl = 'YCSB'
    nalgos=['NO_WAIT','WAIT_DIE','MVCC','MAAT','TIMESTAMP','CALVIN']
    ndelay = [0, 1, 2, 5, 10, 15, 20]
    # network delay in nanoseconds
    ndelay = [int(n * 1000) for n in ndelay]
    nnodes_ = [nnodes]
    txn_write_perc = [0.5]
    tup_write_perc = [0.5]
    load = [10000]
    tcnt = [4]
    skew = [0.6]
    base_table_size = 2097152 * 8
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","NETWORK_DELAY_TEST","NETWORK_DELAY","SET_AFFINITY"]
    exp = [[wl,n,algo,base_table_size * n,tup_wr_perc,txn_wr_perc,ld,sk,thr,"true",d,"false"] for thr,txn_wr_perc,tup_wr_perc,sk,ld,n,d,algo in itertools.product(tcnt,txn_write_perc,tup_write_perc,skew,load,nnodes_,ndelay,nalgos)]
    return fmt,exp


def ycsb_partitions_abort():
    wl = 'YCSB'
    nnodes_ = [nnodes]
    algos=['CALVIN']
    load = [10000]
    nparts = [4]
    mpr = [0, 0.2, 0.4, 0.6, 0.8, 1]
    base_table_size = 2097152*8
    txn_write_perc = [0.5]
    tup_write_perc = [0.5]
    tcnt = [4]
    skew = [0]
    rpq = 16
    fmt = ["WORKLOAD","REQ_PER_QUERY","PART_PER_TXN","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","STRICT_PPT","YCSB_ABORT_MODE", "MPR"]
    exp = [[wl,rpq,p,n,algo,base_table_size * n,tup_wr_perc,txn_wr_perc,ld,sk,thr,1,'true', e] for thr,txn_wr_perc,tup_wr_perc,algo,sk,ld,n,p,e in itertools.product(tcnt,txn_write_perc,tup_write_perc,algos,skew,load,nnodes_,nparts, mpr)]
    return fmt,exp


def deploy(output_f):
    pids = []
    print("Deploying: {}".format(output_f))
    my_ip = subprocess.check_output("ifconfig | grep 'inet ' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $2}'", shell=True)
    line_number = 0
    with open('ifconfig.txt', 'r') as file:
        for line in file:
            if line.strip() in my_ip:
                line_number += 1
            else:
                break
    if line_number < nnodes:
        cmd = "./rundb -n{} -cn{} -nid{}".format(nnodes, nclnodes, line_number)
    else:
        cmd = "./runcl -n{} -cn{} -nid{}".format(nnodes, nclnodes, line_number)
    # for n in range(ntotal):
    #     if n < nnodes:
    #         cmd = "./rundb -n{} -cn{} -nid{}".format(n, nnodes, nclnodes)
    #     elif n < (nnodes + nclnodes):
    #         cmd = "./runcl -n{} -cn{} -nid{}".format(n, nnodes, nclnodes)
    #     else:
    #         assert(False)
        print(cmd)
        cmd = shlex.split(cmd)
        ofile_n = "{}{}_{}.out".format(result_dir, line_number, output_f)
        ofile = open(ofile_n,'w')
        p = subprocess.Popen(cmd, stdout=ofile, stderr=ofile)
        pids.insert(0,p)
    for n in range(ntotal):
        pids[n].wait()


def get_throughput(output_f):
    client = True          # We only sum up throughput from clients, since CALVIN may count a txn multiple times
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
    # draw_line_plot(yvals, xvals, vvals, 'Throughput vs Network Delay', 'Network Delay (us)', 'Throughput (txn/s)', 'CC Algorithm', 'network_sweep.png')


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
    # draw_line_plot(yvals, xvals, vvals, 'Throughput vs Partitions per Transaction', 'Partitions per Transaction', 'Throughput (txn/s)', 'CC Algorithm', 'ycsb_partitions_abort.png')


def execute_all(exp_func):
    global output_f, result_dir

    fmt, experiments = exp_func()
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        output_f = get_outfile_name(cfgs, fmt, [])
        # result_dir = os.path.join("results", output_f)
        output_f = output_f + strnow

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

        # os.system("make clean > temp.out 2>&1")
        # print("Running 'make' for the job...")
        # ret = os.system("make -j8 > temp.out 2>&1")

        os.system("mkdir -p {}".format(result_dir))
        os.system("cp config.h {}{}.cfg".format(result_dir, output_f))

        deploy(output_f)

        os.system("rm *.ipc")
    # print(output_f)
    # deploy()

execute_all(ycsb_partitions_abort)
execute_all(network_sweep)

# plot()
# execute_all()
# ppr_network_plot()
# ycsb_partitions_abort_plot("221025")

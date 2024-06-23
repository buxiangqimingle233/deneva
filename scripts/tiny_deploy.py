import shlex
import subprocess
import itertools
from helper import get_cfgs, get_outfile_name
import datetime
import os, re, sys
import multiprocessing
import time

result_dir = "./results_new/"
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

    base_table_size = 2097152 * 8
    txn_write_perc = [0, 0.5, 0.7]
    tup_write_perc = [0.5]
    tcnt = [4]
    skew = [0]
    rpq = 16
    fmt = ["SKEW_METHOD", "WORKLOAD","REQ_PER_QUERY","PART_PER_TXN","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","STRICT_PPT","YCSB_ABORT_MODE", "MPR"]
    exp = [["HOT", wl,rpq,p,n,algo,base_table_size * n,tup_wr_perc,txn_wr_perc,ld,sk,thr,1,'true', e] for thr,txn_wr_perc,tup_wr_perc,algo,sk,ld,n,p,e in itertools.product(tcnt,txn_write_perc,tup_write_perc,algos,skew,load,nnodes,nparts, mpr)]
    return fmt, exp

def ycsb_partitions_distr():
    wl = 'YCSB'
    nnodes = [8]
    algos=['NO_WAIT','WAIT_DIE','MVCC','CALVIN','TIMESTAMP']
    load = [10000]
    nparts = [1,2,4,6,8]
    # nparts = [1]
    base_table_size=2097152*8
    txn_write_perc = [0.5]
    tup_write_perc = [0.5]
    tcnt = [4]
    skew = [0.6]
    rpq = 16
    fmt = ["WORKLOAD","REQ_PER_QUERY","PART_PER_TXN","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","STRICT_PPT"]
    exp = [[wl,rpq,p,n,algo,base_table_size*n,tup_wr_perc,txn_wr_perc,ld,sk,thr,1] for thr,txn_wr_perc,tup_wr_perc,algo,sk,ld,n,p in itertools.product(tcnt,txn_write_perc,tup_write_perc,algos,skew,load,nnodes,nparts)]
    return fmt,exp


def ycsb_latency_breakdown():
    wl = 'YCSB'
    nnodes = [8]
    nalgos=['NO_WAIT', 'WAIT_DIE', 'MVCC', 'OCC']
    load = [10000]
    nparts = [4]

    mpr = [0.4]     # No use in zipf
    base_table_size = 1024 ** 2 * 16 / 8
    txn_write_perc = [0, 0.7]
    tup_write_perc = [0.5]

    tcnt = [8]
    skew = [0, 0.8]
    rpq = 16

    fmt = ["SKEW_METHOD", "WORKLOAD","REQ_PER_QUERY","PART_PER_TXN","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","STRICT_PPT","YCSB_ABORT_MODE", "MPR"]
    exp = [["ZIPF", wl,rpq,p,n,algo,base_table_size * n,tup_wr_perc,txn_wr_perc,ld,sk,thr,1,'true', e] for thr,txn_wr_perc,tup_wr_perc,algo,sk,ld,n,p,e in itertools.product(tcnt,txn_write_perc,tup_write_perc,nalgos,skew,load,nnodes,nparts, mpr)]

    return fmt, exp

# Use 8 nodes * 8 threads per node, 1, 2, 6 wh per server, standard mix, RO mix
def tpcc_latency_breakdown():
    wl = 'TPCC'
    nnodes = [8]
    nalgos = ['NO_WAIT', 'WAIT_DIE', 'MVCC', 'OCC']
    npercpay = [0.5, 0]
    wh = [1, 8]      # wh per node
    load = [10000]
    thd = 8

    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","PERC_PAYMENT","NUM_WH","MAX_TXN_IN_FLIGHT", "THREAD_CNT"]
    exp = [[wl,n,algo,pay,wh * n,ld,thd] for n,algo,pay,wh,ld in itertools.product(nnodes,nalgos,npercpay,wh,load)]

    return fmt, exp


def tpcc_partition_sensitivity():
    wl = 'TPCC'
    nnodes = [4]
    nalgos = ['NO_WAIT', 'WAIT_DIE', 'MVCC', 'OCC']
    npercpay = [0.5, 0]
    wh = [1, 8]      # wh per node
    load = [10000]
    thd = 6
    mpr = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    fmt = ["MPR_NEWORDER", "WORKLOAD","NODE_CNT","CC_ALG","PERC_PAYMENT","NUM_WH","MAX_TXN_IN_FLIGHT", "THREAD_CNT"]
    exp = [[m, wl,n,algo,pay,wh * n,ld,thd] for m, n,algo,pay,wh,ld in itertools.product(mpr, nnodes,nalgos,npercpay,wh,load)]

    return fmt, exp



def deploy_local(output_f, cfgs):
    pids = []
    print("Deploying: {}".format(output_f))
    nnodes = cfgs["NODE_CNT"]
    ntotal = nnodes + nnodes

    cmd = "numactl --cpunodebind=1 --membind=1 ./rundb -nid{}".format(n)

    for n in range(ntotal):
        if n < nnodes:
            # cmd = "./rundb -nid{}".format(n)
            "numactl --cpunodebind=0 --membind=1 ./rundb -nid{}".format(n)
        elif n < (ntotal):
            # cmd = "./runcl -nid{}".format(n)
            cmd = "numactl --cpunodebind=1 --membind=0 ./runcl -nid{}".format(n)
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


def send_file(args):
    m, f, uname = args
    cmd = "rsync -avz -e \'ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\' --progress {} {}@{}:{}".format(f, uname, m, f"/users/{uname}/")
    print(cmd)
    while True:
        proc = subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
        start_time = time.time()
        while True:
            if proc.poll() is not None:
                break  # process has terminated
            elif time.time() - start_time > 30:  # 30 seconds
                print("rsync timed out, killing process and retrying...")
                proc.kill()
                kill_cmd = f"ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {uname}@{m} 'fuser -k /users/{uname}/{f}'"
                subprocess.run(kill_cmd, shell=True)
                time.sleep(10)  # wait for a bit before retrying
                break
            time.sleep(1)  # check every second
        if proc.poll() is not None:
            break  # process has terminated, exit the outer loop


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
        files = ["./rundb","./runcl","./ifconfig.txt","./benchmarks/TPCC_full_schema.txt"]
    elif cfgs["WORKLOAD"] == "YCSB":
        files = ["./rundb","./runcl","./ifconfig.txt","./benchmarks/YCSB_schema.txt"]

# Parallel version
    # scp_procs = []
    # for m, f in itertools.product(machines, files):
    #     # cmd = "scp -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {} {}@{}:{}".format(f, uname, m, f"/users/{uname}/")
    #     # cmd = "echo {} | tr \' \' \'\\n\' | parallel -j 1 rsync -avz -e {} {} --progress {} {}@{}:{}".format(" ".join(files), f, uname, m, f"/users/{uname}/")
    #     # echo "path/to/file1 path/to/file2 path/to/file3" | tr ' ' '\n' | parallel -j <number_of_jobs> rsync -avz {} user@remote_server:/destination/path/
    #     cmd = "rsync -avz -e \'ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\' --progress {} {}@{}:{}".format(f, uname, m, f"/users/{uname}/")
    #     print(cmd)
    #     scp_procs.append(subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr))

    for m in machines:
        with multiprocessing.Pool() as pool:
            pool.map(send_file, [(m, f, uname) for f in files])

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
        cmd = "ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{}".format(uname, m) + cmd

        ofile_n = "{}{}_{}.out".format(result_dir, cnt, output_f)
        ofile = open(ofile_n,'w')
        ssh_procs.append(subprocess.Popen(cmd, stdout=ofile, stderr=ofile, shell=True))
        print(cmd)

    for p in ssh_procs:
        p.wait()

def execute_all(exp_func):
    global output_f, result_dir

    fmt, experiments = exp_func()
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        output_f = get_outfile_name(cfgs, fmt, [])
        output_f = output_f + strnow
        result_dir = os.path.join("./results_new/", output_f)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        result_dir += "/"

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
    "tpcc_latency_breakdown": tpcc_latency_breakdown,
    "ycsb_partitions_distr": ycsb_partitions_distr,
    "tpcc_partition_sensitivity": tpcc_partition_sensitivity
}

if __name__ == "__main__":
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

    for exp in exps:
        execute_all(experiment_map[exp])

# execute_all(ycsb_partitions_abort)
# plot()
# execute_all()
# ppr_network_plot()    
# network_sweep_plot("094449")

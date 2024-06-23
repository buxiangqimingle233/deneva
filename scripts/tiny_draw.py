import matplotlib.pyplot as plt
import numpy as np
import fnmatch, os, re, sys, csv

from tiny_deploy import experiment_map, get_cfgs, get_outfile_name, result_dir


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


def get_summary(output_f):
    ret = {}
    with open(output_f, "r") as f:
        for line in f:
            if "Running client" in line:
                ret["client"] = True
            if "[summary]" in line:
                pattern = r"(\w+)=([\d.]+)"
                matches = re.findall(pattern, line)
                result = dict(matches)
                ret.update(result)
                break
    if "client" not in ret:
        ret["client"] = False
    return ret


def traverse_procs(directory, pattern, exec_time):
    ret = {}
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, "*" + pattern + '*.out'):
            if str(exec_time) in filename:
                proc_num = int(re.search(r"\d+", filename).group(0))
                summary = get_summary(os.path.join(root, filename))
                for key, value in summary.items():
                    if key not in ret:
                        ret[key] = [(proc_num, value)]
                    else:
                        ret[key].append((proc_num, value))
    # Sort each list in ret based on proc_num
    for key in ret:
        ret[key].sort()
        ret[key] = [float(value) for proc_num, value in ret[key]]
    return ret


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
    # fmt, experiments = network_sweep()
    fmt, experiments = experiment_map["network_sweep"]()
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
    # fmt, experiments = ycsb_partitions_abort()
    fmt, experiments = experiment_map["ycsb_partitions_abort"]()
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
    # print_csv(yvals, xvals, vvals)
    draw_line_plot(yvals, xvals, vvals, 'Throughput vs Partitions per Transaction', 'Partitions per Transaction', 'Throughput (txn/s)', 'CC Algorithm', 'ycsb_partitions_abort.png')


def ycsb_latency_breakdown_plot(exec_time):
    fmt, experiments = experiment_map["ycsb_latency_breakdown"]()
    summary = {}
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        print("theta-{}-w-{}".format(cfgs['ZIPF_THETA'], cfgs['TXN_WRITE_PERC']))
        output_f = get_outfile_name(cfgs, fmt, [])
        cfgs = tuple(cfgs.items())
        summary[cfgs] = traverse_procs(result_dir, output_f, exec_time)

    avg = lambda x: float(sum(x) / float(len(x))) if len(x) > 0 else 0

    xval = summary.keys()
    time_abort = [0] * len(xval)
    time_network = [0] * len(xval)
    time_msg_q = [0] * len(xval)
    time_work_q = [0] * len(xval)
    time_ccman = [0] * len(xval)
    time_cc_block = [0] * len(xval)
    time_work = [0] * len(xval)
    total = [1] * len(xval)
    txn_cnt = [1] * len(xval)
    time_other = [0] * len(xval)


    for i, cfgs in enumerate(summary.keys()):
        txn_cnt[i] = sum(summary[cfgs]['txn_cnt'])

        time_msg_q[i] = (sum(summary[cfgs]['lat_short_msg_queue_time']) + sum(summary[cfgs]['lat_short_batch_time']) ) / txn_cnt[i]
        time_work_q[i] = (sum(summary[cfgs]['lat_short_work_queue_time']) ) / txn_cnt[i]
        time_ccman[i] = (sum(summary[cfgs]['lat_short_cc_time']) ) / txn_cnt[i]
        time_cc_block[i] = (sum(summary[cfgs]['lat_short_cc_block_time']) ) / txn_cnt[i]
        time_work[i] = (sum(summary[cfgs]['lat_short_process_time']) ) / txn_cnt[i]
        total[i] = time_abort[i] + time_msg_q[i] +time_work_q[i] + time_ccman[i] + time_cc_block[i] + time_work[i] + time_network[i]
# txn_total_process_time_avg
        time_other[i] = avg(summary[cfgs]['lscl50']) - total[i]
        time_network[i] = min((sum(summary[cfgs]['lat_short_network_time']) ) / txn_cnt[i],time_other[i])

        # print("NETWORK: {} vs {}".format((sum(summary[cfgs]['lat_short_network_time']) ) / txn_cnt[i], time_other[i]))
        total[i] = time_abort[i] + time_msg_q[i] +time_work_q[i] + time_ccman[i] + time_cc_block[i] + time_work[i] + time_network[i]

        time_other[i] = avg(summary[cfgs]['lscl50']) - total[i]
        total[i] = avg(summary[cfgs]['lscl50'])

    # time_abort = [i / j for i,j in zip(time_abort,time_work)]
    # time_network = [i / j for i,j in zip(time_network,time_work)]
    # time_msg_q = [i / j for i,j in zip(time_msg_q,time_work)]
    # time_work_q = [i / j for i,j in zip(time_work_q,time_work)]
    # time_ccman = [i / j for i,j in zip(time_ccman,time_work)]
    # time_cc_block = [i / j for i,j in zip(time_cc_block,time_work)]
    # time_work = [i / j for i,j in zip(time_work,time_work)]
    # time_other = [i / j for i,j in zip(time_other,time_work)]

    # time_abort = [i / j for i,j in zip(time_abort,total)]
    # time_network = [i / j for i,j in zip(time_network,total)]
    # time_msg_q = [i / j for i,j in zip(time_msg_q,total)]
    # time_work_q = [i / j for i,j in zip(time_work_q,total)]
    # time_ccman = [i / j for i,j in zip(time_ccman,total)]
    # time_cc_block = [i / j for i,j in zip(time_cc_block,total)]
    # time_work = [i / j for i,j in zip(time_work,total)]
    # time_other = [i / j for i,j in zip(time_other,total)]

    data = [
        time_network,
        time_other,
        time_msg_q,
        time_work_q,
        time_ccman,
        time_cc_block,
        time_work
    ]
    for d in data:
        print(" ".join(map(str, d)))


def ycsb_partitions_distr_plot(exec_time):
    fmt, experiments = experiment_map["ycsb_partitions_distr"]()
    summary = {}
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        # print("theta-{}-w-{}".format(cfgs['ZIPF_THETA'], cfgs['TXN_WRITE_PERC']))
        output_f = get_outfile_name(cfgs, fmt, [])
        cfgs = tuple(cfgs.items())
        res = traverse_procs("./results", output_f, exec_time)
        if "txn_cnt" not in res:
            print("Missing txn_cnt in {}".format(output_f))
        else:
            summary[cfgs] = res
    avg = lambda x: float(sum(x) / float(len(x))) if len(x) > 0 else 0


    for e, (i, cfgs) in zip(experiments, enumerate(summary.keys())):
        print(e[4], e[2], end=" ")
        print(sum(summary[cfgs]['tput']))


def ycsb_partitions_breakdown_plot(exec_time):
    fmt, experiments = experiment_map["ycsb_latency_breakdown"]()
    summary = {}
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        # print("theta-{}-w-{}".format(cfgs['ZIPF_THETA'], cfgs['TXN_WRITE_PERC']))
        output_f = get_outfile_name(cfgs, fmt, [])
        cfgs = tuple(cfgs.items())
        res = traverse_procs("./results_new", output_f, exec_time)
        if "txn_cnt" not in res:
            print("Missing txn_cnt in {}".format(output_f))
            # experiments.remove(e)
        else:
            summary[cfgs] = res
    avg = lambda x: float(sum(x) / float(len(x))) if len(x) > 0 else 0

    xval = summary.keys()
    time_idle = [0] * len(xval)
    time_index = [0] * len(xval)
    time_abort = [0] * len(xval)
    time_twopc = [0] * len(xval)
    time_ccman = [0] * len(xval)
    time_work = [0] * len(xval)
    time_overhead = [0] * len(xval)
    total = [1] * len(xval)

    for i, cfgs in enumerate(summary.keys()):
        time_idle[i] = avg(summary[cfgs]['worker_idle_time'])
        if 'seq_idle_time' in summary[cfgs] and 'sched_idle_time' in summary[cfgs]:
            time_idle[i] = time_idle[i] + avg(summary[cfgs]['seq_idle_time']) + avg(summary[cfgs]['sched_idle_time'])
        time_index[i] = avg(summary[cfgs]['txn_index_time'])
        time_abort[i] = avg(summary[cfgs]['abort_time'])
        time_ccman[i] = avg(summary[cfgs]['txn_manager_time']) + avg(summary[cfgs]['txn_validate_time'])
        if 'seq_process_time' in summary[cfgs] and 'seq_ack_time' in summary[cfgs] and 'seq_prep_time' in summary[cfgs] and 'calvin_sched_time' in summary[cfgs]:
            time_ccman[i] = time_ccman[i] + avg(summary[cfgs]['seq_process_time']) + avg(summary[cfgs]['seq_ack_time']) + avg(summary[cfgs]['seq_prep_time']) + avg(summary[cfgs]['calvin_sched_time'])
        time_twopc[i] = avg(summary[cfgs]['proc_time_type6']) + avg(summary[cfgs]['proc_time_type11']) + avg(summary[cfgs]['proc_time_type12']) + avg(summary[cfgs]['proc_time_type16']) - avg(summary[cfgs]['txn_validate_time'])
        if time_twopc[i] > avg(summary[cfgs]['txn_cleanup_time']):
            time_twopc[i] -= avg(summary[cfgs]['txn_cleanup_time'])
        time_overhead[i] = avg(summary[cfgs]['txn_cleanup_time']) + avg(summary[cfgs]['txn_table_release_time']) + avg(summary[cfgs]['txn_table_get_time'])
        time_work[i] = avg(summary[cfgs]['txn_process_time'])
        total[i] = time_abort[i] + time_ccman[i] + time_twopc[i] + time_work[i] + time_idle[i] + time_overhead[i]

    data = [
        time_idle,
        time_index,
        time_abort,
        time_twopc,
        time_ccman,
        time_overhead,
        time_work
    ]
    data = list(map(list, zip(*data)))

    # title = ["time_idle", "time_abort", "time_twopc", "time_ccman", "time_overhead", "time_work"]
    stack_names = [
        'Idle',
        'Abort',
        'Index',
        '2PC',
        'CC Manager',
        'Txn Manager',
        'Useful Work'
    ]

    print(" ".join(stack_names))
    # print(len(data))
    for e, d in zip(experiments, data):
        # print(e[4], e[2], end=" ")
        # print(f"{e[2]} {e[4]}", end=" ")
        print(" ".join(map(str, d)))

    # for e, (i, cfgs) in zip(experiments, enumerate(summary.keys())):
    #     print(e[4], e[2], end=" ")
    #     print(sum(summary[cfgs]['tput']))


def get_tput(exec_time):
    # fmt, experiments = experiment_map["ycsb_latency_breakdown"]()
    fmt, experiments = experiment_map["tpcc_latency_breakdown"]()

    summary = {}
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        # print("theta-{}-w-{}".format(cfgs['ZIPF_THETA'], cfgs['TXN_WRITE_PERC']))
        output_f = get_outfile_name(cfgs, fmt, [])
        cfgs = tuple(cfgs.items())
        res = traverse_procs("./results_new", output_f, exec_time)
        if "txn_cnt" not in res:
            print("Missing txn_cnt in {}".format(output_f))
            exit()
            # experiments.remove(e)
        else:
            summary[cfgs] = res
    avg = lambda x: float(sum(x) / float(len(x))) if len(x) > 0 else 0

    # summary = dict(sorted(summary.items(), key=lambda kv: (dict(kv[0])['TXN_WRITE_PERC'], dict(kv[0])['ZIPF_THETA'], dict(kv[0])['CC_ALG'])))
    summary = dict(sorted(summary.items(), key=lambda kv: (dict(kv[0])['NUM_WH'], dict(kv[0])['PERC_PAYMENT'], dict(kv[0])['CC_ALG'])))
    i = 0
    for cfg, data in summary.items():
        if i % 4 == 0:
            print()
            print()
        i += 1
        cfg_dict = dict(cfg)
        # name = "ZIPF_THETA_{}_TXN_WRITE_PERC_{}_CC_ALG_{}".format(cfg_dict['ZIPF_THETA'], cfg_dict['TXN_WRITE_PERC'], cfg_dict['CC_ALG'])
        name = "NUM_WH_{}_PERC_PAYMENT_{}_CC_ALG_{}".format(cfg_dict['NUM_WH'], cfg_dict['PERC_PAYMENT'], cfg_dict['CC_ALG'])

        # Scale RPC with

        # print("NETWORK: {} vs {}".format((sum(summary[cfgs]['lat_short_network_time']) ) / txn_cnt[i], time_other[i]))
        print(name, sum(data['tput']) / (cfg_dict['NODE_CNT'] * cfg_dict['THREAD_CNT']))


def get_tput_cxl_rpc(exec_time):
    fmt, experiments = experiment_map["ycsb_latency_breakdown"]()
    # fmt, experiments = experiment_map["tpcc_latency_breakdown"]()

    summary = {}
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        # print("theta-{}-w-{}".format(cfgs['ZIPF_THETA'], cfgs['TXN_WRITE_PERC']))
        output_f = get_outfile_name(cfgs, fmt, [])
        cfgs = tuple(cfgs.items())
        res = traverse_procs("./results_new", output_f, exec_time)
        if "txn_cnt" not in res:
            print("Missing txn_cnt in {}".format(output_f))
            exit()
            # experiments.remove(e)
        else:
            summary[cfgs] = res
    avg = lambda x: float(sum(x) / float(len(x))) if len(x) > 0 else 0

    # summary = dict(sorted(summary.items(), key=lambda kv: (dict(kv[0])['TXN_WRITE_PERC'], dict(kv[0])['ZIPF_THETA'], dict(kv[0])['CC_ALG'])))
    summary = dict(sorted(summary.items(), key=lambda kv: (dict(kv[0])['NUM_WH'], dict(kv[0])['PERC_PAYMENT'], dict(kv[0])['CC_ALG'])))
    i = 0
    for cfg, data in summary.items():
        if i % 4 == 0:
            print()
            print()
        i += 1
        cfg_dict = dict(cfg)
        # name = "ZIPF_THETA_{}_TXN_WRITE_PERC_{}_CC_ALG_{}".format(cfg_dict['ZIPF_THETA'], cfg_dict['TXN_WRITE_PERC'], cfg_dict['CC_ALG'])
        name = "NUM_WH_{}_PERC_PAYMENT_{}_CC_ALG_{}".format(cfg_dict['NUM_WH'], cfg_dict['PERC_PAYMENT'], cfg_dict['CC_ALG'])

        # Scale RPC with
        time_idle = avg(summary[cfgs]['worker_idle_time'])
        if 'seq_idle_time' in summary[cfgs] and 'sched_idle_time' in summary[cfgs]:
            time_idle = time_idle + avg(summary[cfgs]['seq_idle_time']) + avg(summary[cfgs]['sched_idle_time'])
        time_index = avg(summary[cfgs]['txn_index_time'])
        time_abort = avg(summary[cfgs]['abort_time'])
        time_ccman = avg(summary[cfgs]['txn_manager_time']) + avg(summary[cfgs]['txn_validate_time'])
        if 'seq_process_time' in summary[cfgs] and 'seq_ack_time' in summary[cfgs] and 'seq_prep_time' in summary[cfgs] and 'calvin_sched_time' in summary[cfgs]:
            time_ccman = time_ccman + avg(summary[cfgs]['seq_process_time']) + avg(summary[cfgs]['seq_ack_time']) + avg(summary[cfgs]['seq_prep_time']) + avg(summary[cfgs]['calvin_sched_time'])
        time_twopc = avg(summary[cfgs]['proc_time_type6']) + avg(summary[cfgs]['proc_time_type11']) + avg(summary[cfgs]['proc_time_type12']) + avg(summary[cfgs]['proc_time_type16']) - avg(summary[cfgs]['txn_validate_time'])
        if time_twopc > avg(summary[cfgs]['txn_cleanup_time']):
            time_twopc -= avg(summary[cfgs]['txn_cleanup_time'])
        time_overhead = avg(summary[cfgs]['txn_cleanup_time']) + avg(summary[cfgs]['txn_table_release_time']) + avg(summary[cfgs]['txn_table_get_time'])
        time_work = avg(summary[cfgs]['txn_process_time'])
        total = time_abort + time_ccman + time_twopc + time_work + time_idle + time_overhead

        # print(name, " ".join(map(str, [time_abort / total, time_ccman / total, time_twopc / total, time_work / total, time_idle / total, time_overhead / total])))
        tput = sum(data['tput']) / (cfg_dict['NODE_CNT'] * cfg_dict['THREAD_CNT'])
        tput *= total / (total - time_idle + time_idle * 1.47 / 7.60)
        # print("NETWORK: {} vs {}".format((sum(summary[cfgs]['lat_short_network_time']) ) / txn_cnt[i], time_other[i]))
        print(tput)


def tpcc_latency_breakdown_plot(exec_time):
    fmt, experiments = experiment_map["tpcc_latency_breakdown"]()
    summary = {}
    for e in experiments:
        cfgs = get_cfgs(fmt,e)
        # print("theta-{}-w-{}".format(cfgs['ZIPF_THETA'], cfgs['TXN_WRITE_PERC']))
        output_f = get_outfile_name(cfgs, fmt, [])
        cfgs = tuple(cfgs.items())
        res = traverse_procs("./results", output_f, exec_time)
        if "txn_cnt" not in res:
            print("Missing txn_cnt in {}".format(output_f))
        else:
            summary[cfgs] = res
    avg = lambda x: float(sum(x) / float(len(x))) if len(x) > 0 else 0

    xval = summary.keys()
    time_abort = [0] * len(xval)
    time_network = [0] * len(xval)
    time_msg_q = [0] * len(xval)
    time_work_q = [0] * len(xval)
    time_ccman = [0] * len(xval)
    time_cc_block = [0] * len(xval)
    time_work = [0] * len(xval)
    total = [1] * len(xval)
    txn_cnt = [1] * len(xval)
    time_other = [0] * len(xval)

    for i, cfgs in enumerate(summary.keys()):
        txn_cnt[i] = sum(summary[cfgs]['txn_cnt'])

        time_msg_q[i] = (sum(summary[cfgs]['lat_short_msg_queue_time']) + sum(summary[cfgs]['lat_short_batch_time']) ) / txn_cnt[i]
        time_work_q[i] = (sum(summary[cfgs]['lat_short_work_queue_time']) ) / txn_cnt[i]
        time_ccman[i] = (sum(summary[cfgs]['lat_short_cc_time']) ) / txn_cnt[i]
        time_cc_block[i] = (sum(summary[cfgs]['lat_short_cc_block_time']) ) / txn_cnt[i]
        time_work[i] = (sum(summary[cfgs]['lat_short_process_time']) ) / txn_cnt[i]

        total[i] = time_abort[i] + time_msg_q[i] +time_work_q[i] + time_ccman[i] + time_cc_block[i] + time_work[i] + time_network[i]
        # txn_total_process_time_avg .
        time_other[i] = avg(summary[cfgs]['lscl_avg']) - total[i]
        time_network[i] = min((sum(summary[cfgs]['lat_short_network_time']) ) / txn_cnt[i],time_other[i])

        # print("NETWORK: {} vs {}".format((sum(summary[cfgs]['lat_short_network_time']) ) / txn_cnt[i], time_other[i]))
        total[i] = time_abort[i] + time_msg_q[i] +time_work_q[i] + time_ccman[i] + time_cc_block[i] + time_work[i] + time_network[i]

        time_other[i] = avg(summary[cfgs]['lscl_avg']) - total[i]
        total[i] = avg(summary[cfgs]['lscl_avg'])

    # time_abort = [i / j for i,j in zip(time_abort,time_work)]
    # time_network = [i / j for i,j in zip(time_network,time_work)]
    # time_msg_q = [i / j for i,j in zip(time_msg_q,time_work)]
    # time_work_q = [i / j for i,j in zip(time_work_q,time_work)]
    # time_ccman = [i / j for i,j in zip(time_ccman,time_work)]
    # time_cc_block = [i / j for i,j in zip(time_cc_block,time_work)]
    # time_work = [i / j for i,j in zip(time_work,time_work)]
    # time_other = [i / j for i,j in zip(time_other,time_work)]

    # time_abort = [i / j for i,j in zip(time_abort,total)]
    # time_network = [i / j for i,j in zip(time_network,total)]
    # time_msg_q = [i / j for i,j in zip(time_msg_q,total)]
    # time_work_q = [i / j for i,j in zip(time_work_q,total)]
    # time_ccman = [i / j for i,j in zip(time_ccman,total)]
    # time_cc_block = [i / j for i,j in zip(time_cc_block,total)]
    # time_work = [i / j for i,j in zip(time_work,total)]
    # time_other = [i / j for i,j in zip(time_other,total)]

    data = [
        time_network,
        time_other,
        time_msg_q,
        time_work_q,
        time_ccman,
        time_cc_block,
        time_work,
        total
    ]
    data = list(map(list, zip(*data)))
    # print("time_network time_other time_msg_q time_work_q time_ccman time_cc_block time_work")

    for e, d in zip(experiments, data):
        # print(f"{e[2]} {e[4]}", end=" ")
        print(" ".join(map(str, d)))
# txn_total_remote_wait_time_avg
# txn_total_twopc_time_avg
# txn_total_process_time_avg

# 20240430
# ycsb_partitions_breakdown_plot("20240430")
# ycsb_partitions_distr_plot("20240430")
# ycsb_partitions_breakdown_plot("215256")

# tpcc_latency_breakdown_plot("222318")
# ycsb_partitions_abort_plot("125936")
# ycsb_partitions_abort_plot("174851")        # A successful run on 4 nodes, cloudlab rs620
# ycsb_latency_breakdown_plot("203251")     # 114242
# ycsb_latency_breakdown_plot("193817")

# get_tput("215256")  # YCSB
# get_tput("203251")  # TPCC
# get_tput_cxl_rpc("203251")  # TPCC
get_tput_cxl_rpc("215256")  # YCSB

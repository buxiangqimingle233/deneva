import subprocess
import time
import datetime
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
result_dir = "./results_new/"

now = datetime.datetime.now()
strnow=now.strftime("%Y%m%d-%H%M%S")

def parse_xml():
    return " "

def deploy():
    cfg_fname = "hosts.xml"
    uname = "bxqml233"
    machines = []
    with open(cfg_fname, "r") as f:
        for line in f:
            machines.append(parse_xml)

    print(" ===================== Sending Files ===================== ")
    for m in machines:
        cmd = "rsync -e \'ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\' -i -rtuv {} {}@{}:{}".format(script_dir, uname, m, f"/users/{uname}")
        os.system(cmd)
        print(cmd)

    time.sleep(1)

    print(" ===================== Killing Processes ===================== ")
    for m in machines:
        cmd = "pkill -f nocc; sync"
        cmd = "ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{} ".format(uname, m) + cmd
        os.system(cmd)
        print(cmd)

    print(" ===================== Killing Processes ===================== ")
    ssh_procs = []
    for m in machines:
        cmd = "pkill -f nocc; sync"
        cmd = "ssh -o IPQoS=none -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{} ".format(uname, m) + cmd
        print(cmd)
        ssh_procs.append(subprocess.Popen(cmd, shell=True))
    for p in ssh_procs:
        p.wait()

    print(" ===================== Deploying ===================== ")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        # os.system("rm -rf {}".format(result_dir))

    ssh_procs = []
    for m, cnt in enumerate(machines):
        cmd = "./noccocc --bench tpcc --txn-flags 1 --verbose --config config.xml --id {} -t 8 -c 2 -r 100 -p {}".format(cnt, len(machines))
        ofile_n = os.path.join(result_dir, f"{cnt}_{strnow}.out")
        ofile = open(ofile_n,'w')
        ssh_procs.append(subprocess.Popen(cmd, stdout=ofile, stderr=ofile, shell=True))

    for p in ssh_procs:
        p.wait()


if __name__ == "__main__":
    deploy()
    print(" ===================== Done ===================== ")
import subprocess
import logging
import time

NAMESPACE= "redhat-ods-monitoring"
LABEL= "deployment=prometheus"
CONTAINER_NO= "4"
PODS_NO= "1"


def run(cmd):
    try:
        output = subprocess.Popen(
            cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        (out, err) = output.communicate()
    except Exception as e:
        logging.error("Failed to run %s, error: %s" % (cmd, e))
    return out


i = 0
while i < 100:
    pods_running = run(f"oc get pods -n {NAMESPACE} -l {LABEL} | grep -c '{CONTAINER_NO}/{CONTAINER_NO}'").rstrip()
    if pods_running == PODS_NO:
        break
    time.sleep(5)
    i += 1

if pods_running == PODS_NO:
    print(f"There were {PODS_NO} pods running properly")
else:
    print(f"ERROR there were {pods_running} pods running instead of {PODS_NO}")
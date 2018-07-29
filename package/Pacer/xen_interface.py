import pprint
import subprocess

# functions to interactive with xl to get VM info or assign cpu resource


def get_global_info():
    def create_single_vcpu_info(line):
        single_cpu_info={}
        pcpu = line[3]
        if pcpu.isdigit():
            single_cpu_info['pcpu']=int(pcpu)
        else:
            single_cpu_info['pcpu']=-1
        pcpu_pin = line[6]
        single_cpu_info['pcpu_pin']=pcpu_pin
        # if pcpu_pin.isdigit():
        #     single_cpu_info['pcpu_pin']=int(pcpu_pin)
        # else:
        #     single_cpu_info['pcpu_pin']=-1    
        return single_cpu_info


    shared_data = {}
    shared_data['rtxen']=set()
    shared_data['credit']=set()
    shared_data['cnt']=0


    out =  subprocess.check_output(['xl', 'vcpu-list']).decode().split('\n')
    out=out[1:-1]
    for lines in out:
        line = lines.split()
        if line[1] not in shared_data:
            shared_data[line[1]]={}
            shared_data[line[1]]=[]
            shared_data[line[1]].append(create_single_vcpu_info(line))

        else:
            shared_data[line[1]].append(create_single_vcpu_info(line))


    out =  subprocess.check_output(['xl', 'sched-credit']).decode().split('\n')
    if out[0]!='':
        out=out[2:-1]
        for lines in out:
            line = lines.split()
            shared_data['credit'].add(line[1])
            for vcpu in shared_data[line[1]]:
                vcpu['w']=int(line[2])
                vcpu['c']=int(line[3])

    out =  subprocess.check_output(['xl', 'sched-rtds','-v','all']).decode().split('\n')
    if out[0]!='':
        out=out[2:-1]
        for lines in out:
            line = lines.split()
            if line[1]!='0' and line[1].isdigit():
                shared_data['rtxen'].add(line[1])
            if line[1].isdigit():
                shared_data[line[1]][int(line[2])]['p']=int(line[3])
                shared_data[line[1]][int(line[2])]['b']=int(line[4])





    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(shared_data)
    return shared_data


def sched_rtds(domuid,p,b,vcpus):
    if vcpus==[]:
        proc = subprocess.Popen(['xl','sched-rtds','-d',str(domuid),'-p',str(p),'-b',str(b)])
    else:
        cmd = ['xl','sched-rtds','-d',str(domuid)]
        for i,vcpu in enumerate(vcpus):
            # proc = subprocess.Popen(['xl','sched-rtds','-d',str(domuid),'-v',str(vcpu),'-p',str(p[i]),'-b',str(b[i])])
            cmd.append('-v')
            cmd.append(str(vcpu))
            cmd.append('-p')
            cmd.append(str(p[i]))
            cmd.append('-b')
            cmd.append(str(b[i]))
        proc = subprocess.Popen(cmd)

def sched_credit(domuid,w):
    proc = subprocess.Popen(['xl','sched-credit','-d',str(domuid),'-w',str(w)])
def sched_credit_timeslice(ts):
    # xl sched-credit -p credit -s -t 5ms
    proc = subprocess.Popen(['xl','sched-credit','-p','credit','-s','-t',str(ts)+'ms'])

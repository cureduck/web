import os,sys,subprocess
from time import time
from rater import rate



def start_task(comm,path,argv,times=10):
    command=comm+' '+path+" "+argv
    student_id=path.split('/')[-1].split('.')[0]

    time_spent,score=[],[]
    for i in range(times):
        time_start=time()
        process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        time_end = time()
        time_spent.append(time_end-time_start)
        score.append(rate(student_id))

    with open('./final_score/'+student_id,'wa')as f:
        f.write(student_id+'的运行结果:/n')
        for i in range(times):
            f.write('运行结果'+i+':时间花费'+time_spent[i],',运行结果：'+score[i]+'/n')

        f.write('/n/n')






if __name__=='__main__':

    argv=sys.argv
    print(argv)


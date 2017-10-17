import sys
def rate(student_id,path=None):
    score=0
    if path is None:
        path='./result/'+student_id
    with open(path,'r'):
        pass
    return score

if __name__=='__main__':
    print(sys.argv)
    print('usage: python3 rater path')
    argv=sys.argv[1]
    rate(None,argv)
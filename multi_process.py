import multiprocessing
 
def pin(i):
    print i
    return 

def worker(num):
    """thread worker function"""
    print 'Worker:', num
    return
 
if __name__ == "__main__":
    job = []
    for i in range(0,20):
        p = multiprocessing.Process( target = pin, args = (i,) )
        p.start()
        job.append(p)
    for p in job:
        p.join()

# import multiprocessing
# 

# 
# if __name__ == '__main__':
#     jobs = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i,))
#         jobs.append(p)
#         p.start()
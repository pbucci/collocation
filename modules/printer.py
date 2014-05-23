import time
import datetime
class log(object):
    def __init__(self,args):
        ts = time.time()
        print(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), end='\t')
        print(args)
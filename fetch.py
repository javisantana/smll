#!/usr/bin/python
# coding: utf-8

import urllib
import urllib2
from multiprocessing import Pool
import Queue, threading

reg_nos = [16738, 17288, 18162, 18776, 18868, 19116, 19223, 19505];
pdf_url = 'http://www.mapa.es/agricultura/pags/fitos/registro/sustancias/pdf/%s.pdf'

def fetch_url(url, params={}): 
    return urllib2.urlopen(url).read() 

def save_url_as_file(url, filename):
    open(filename,'wb').write(fetch_url(url))
    
def download_pdf(reg_no):
    f = '%d.pdf' % reg_no
    save_url_as_file(pdf_url % reg_no, f)
    print "\t- %s downloaded" % f

# tests
def single(regs):
    for u in regs:
        download_pdf(u)

def multi(regs, nprocesses=4):
    pool = Pool(processes=nprocesses) 
    pool.map_async(download_pdf, regs).get()

def threaded(regs, nthreads=4):
    # ripped from http://www.dabeaz.com/generators/Generators.pdf
    def consumer(q): 
        while True:
            item = q.get() 
            if not item: break 
            download_pdf(item)

    in_q = Queue.Queue() 
    
    # start threads
    ths = [threading.Thread(target=consumer,args=(in_q,)) 
                for th in xrange(nthreads)]
    for x in ths: x.start()

    # put files to download
    for i in regs:
        in_q.put(i)

    # put end guards
    for th in xrange(nthreads): in_q.put(None)

    # wait to finish
    for x in ths: x.join()
    

if __name__ == '__main__':
    from timeit import Timer
    t = Timer("single(reg_nos)", "from __main__ import single, reg_nos")
    print t.timeit(number=1)
    t = Timer("multi(reg_nos)", "from __main__ import multi, reg_nos")
    print t.timeit(number=1)
    t = Timer("threaded(reg_nos)", "from __main__ import threaded, reg_nos")
    print t.timeit(number=1)


# -*- coding:utf-8 -*-

import requests
import threading
import time

from config import config
from random import randint
from libtools import wanip

class Worker(threading.Thread):
    runable = True
    logfile = "ips.txt"
    
    def run(self):
        print("DDNS Client Started.")
        sleeptime = 120
        while(self.runable):
            try:
                fd = open(self.logfile,'r+')
            except FileNotFoundError as ex:
                fd = open(self.logfile,'w+')
                
            try:
                last_ip = fd.readline()
                if last_ip[-1:] == '\n':
                    last_ip = last_ip[0:-1]
                
                ip = wanip.query()
                print("{} current ip:{} last ip:{}".format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), ip,last_ip))
                
                if ip == last_ip:
                    sleeptime = randint(config['sleepTime']['noNeedMin'], config['sleepTime']['noNeedMax'])
                    print("updating not need, sleep {} seconds".format(sleeptime))
                else:
                    fd.seek(0)
                    fd.write(ip + "\n")
                    self.data['value'] = ip
                    requests.post(config['url'], data=config['data'])

                    sleeptime = randint(config['sleepTime']['updatedMin'], config['sleepTime']['updatedMax'])
                    print("updated success, sleep {} seconds".format(sleeptime))
                    
            except:
                sleeptime = randint(config['sleepTime']['errorMin'], config['sleepTime']['errorMax'])
                print("Unkown error, sleep {} seconds".format(sleeptime))
            finally:
                fd.close()
                
            time.sleep(sleeptime)
        
    def stop(self):
        self.runable = False
        
if __name__ == "__main__":
    try:
        w1 = Worker()
        w1.setDaemon(True)
        w1.start()
        w1.join()
    except (KeyboardInterrupt, EOFError) as ex:
        w1.stop()
        print("*** User Quit ***")

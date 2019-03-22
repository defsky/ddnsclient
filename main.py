# -*- coding:utf-8 -*-

import requests
import threading
import time, sys

from config import config
from random import randint
from libtools import wanip
from modules.dbutils import DB, DBError

import logging
from logging.handlers import RotatingFileHandler

logfmt = '%(asctime)s [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
fmtter = logging.Formatter(logfmt,datefmt)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(fmtter)

fileHandler = RotatingFileHandler('log/ddnsclient.log',maxBytes=1*1024*1024,backupCount=10)
fileHandler.setFormatter(fmtter)

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

wanipDB = DB('sqlite:database=data/wanip.db')

class Worker(threading.Thread):
    runable = True
    logfile = "ips.txt"
    
    def run(self):
        logger.info("DDNS Client Started.")
        sleeptime = 120
        while(self.runable):
            #try:
            #    fd = open(self.logfile,'r+')
            #except FileNotFoundError as ex:
            #    fd = open(self.logfile,'w+')
                
            try:
                #last_ip = fd.readline()
                ips = wanipDB.query('select ip from used_ip order by id desc limit 1 offset 0')
                if len(ips) != 0:
                    last_ip, = ips[0]
                else:
                    last_ip = ''

                #if last_ip[-1:] == '\n':
                #    last_ip = last_ip[0:-1]
                
                #ip = wanip.query()
                ip = wanip.getWanIp('https://www.afkplayer.com/api/get_wan_ip.php')
                logger.info("wanip:{} last:{}".format(ip, last_ip))
                
                if ip == last_ip:
                    sleeptime = randint(config['sleepTime']['noNeedMin'], config['sleepTime']['noNeedMax'])
                    logger.info("updating not needed, sleep {} seconds".format(sleeptime))
                else:
                    config['data']['value'] = ip
                    requests.post(config['url'], data=config['data'])

                    wanipDB.execute("insert into used_ip values(NULL, '{}','{}')".format(ip, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

                    #fd.seek(0)
                    #fd.write(ip + "\n")

                    sleeptime = randint(config['sleepTime']['updatedMin'], config['sleepTime']['updatedMax'])
                    logger.info("updated success, sleep {} seconds".format(sleeptime))
            except DBError:
                logger.error("DB Error Occured!")
                sleeptime = 3
            except:
                sleeptime = randint(config['sleepTime']['errorMin'], config['sleepTime']['errorMax'])
                logger.error("Unkown error, sleep {} seconds,{}".format(sleeptime,sys.exc_info()[0]))
            finally:
                #fd.close()
                pass
                
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
        logger.info("*** User Quit ***")

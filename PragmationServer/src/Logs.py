'''
Created on 04/04/2014

PragmationServer

@author: Juan Carlos Hdez. (programaando@gmail.com) para CirculoOfij, proyecto Pragmation. 

'''
import json
import logging.handlers
import logging
import os


class Logs():

    def __init__(self):
        '''
        Initialize all configuration relative to logs

        '''

        # create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        # this handler does not work properly in windows
        log_file = os.getenv('LOG_PATH', 'PragmationServer.log')
        ch = logging.handlers.RotatingFileHandler(log_file,
                                                mode='a',
                                                maxBytes=16000000,
                                                backupCount=0,
                                                encoding=os.getenv('LOG_ENCODING', None))
        print "Logging at:" + log_file

        level = logging.INFO
        if bool(os.getenv('DEBUG')):
            level = logging.DEBUG
        ch.setLevel(level)

        # create formatter
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)
        
        
    def info_log(self, log):
        '''
        Log a info entry in logs

        Keyword:
        log   -- body for the alarm

        '''
        self.logger.info(log)
   
   
    def warning_log(self, log):
        '''
        Log a warning entry in logs

        Keyword:
        log   -- body for the alarm

        '''
      
        self.logger.warning(log)

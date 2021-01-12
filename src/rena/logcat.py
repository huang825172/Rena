#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/11 0011
# @Email : happy.huangyang@gmail.com

""" Logging/Debugging facilities """

import socket
import logging
from logging.handlers import DatagramHandler

logging_port = 4371

if __name__ != '__main__':
    from rena import system


    class PureDatagramHandler(DatagramHandler):
        """
        Redefine datagram handler for logging to output log in pure text.
        """

        def makePickle(self, record: logging.LogRecord) -> bytes:
            """
            Make the function return pure log content.
            :param record: log record
            :return: log record in pure text
            """
            return (self.format(record)).encode(encoding='utf-8')


    class Logcat:
        """
        Package class for logging
        """

        def __init__(self, name: str):
            self._logger = logging.getLogger(name)
            self._logger.setLevel(level=logging.DEBUG)
            self._udp_handler = PureDatagramHandler('127.0.0.1', logging_port)
            formatter = logging.Formatter('%(name)s [%(levelname)s] %(asctime)s : %(message)s')
            self._udp_handler.setFormatter(formatter)
            self._logger.addHandler(self._udp_handler)
            system.start_python_console(__file__)

        def close(self):
            """
            Close the logcat console.
            """
            self._udp_handler.send('exit'.encode(encoding='utf-8'))

        def debug(self, msg: str):
            """
            Add log in DEBUG level.
            :param msg: Log content
            """
            self._logger.debug(msg)

        def info(self, msg: str):
            """
            Add log in INFO level.
            :param msg: Log content
            """
            self._logger.info(msg)

        def warning(self, msg: str):
            """
            Add log in WARNING level.
            :param msg: Log content
            """
            self._logger.warning(msg)

        def error(self, msg: str):
            """
            Add log in ERROR level.
            :param msg: Log content
            """
            self._logger.error(msg)

        def critical(self, msg: str):
            """
            Add log in CRITICAL level.
            :param msg: Log content
            """
            self._logger.critical(msg)

        def set_level(self, level: str):
            """
            Set logging record level.
            :param level: Level name
            """
            self._logger.setLevel(getattr(logging, level))
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.bind(('127.0.0.1', logging_port))
    except IOError as e:
        exit(0)
    log = ''
    while log != 'exit':
        try:
            recv, addr = s.recvfrom(1024)
            log = recv.decode(encoding='utf-8')
            print(log)
        except Exception as e:
            print(e)

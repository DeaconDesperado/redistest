"""
A simple procedural script that will create a redis client
"""
import socket
import sys
import re
import logging

log = logging.getLogger(__name__)
sh = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(sh)

class RedisConException(Exception):
    """
    This is just a client-specific exception that gets the remainder of error responses
    """
    def __init__(self,message):
        Exception.__init__(self,message)

class RedisCon:
    """ The redis connection, at localhost for demo purposes"""

    def __init__(self,host_ip = '127.0.0.1',host_port=6379):
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((host_ip,host_port))
        except socket.error:
            print 'No server running at localhost'

    def _send_cmd(self,cmd,*args):
        """
        Send a command to the socket and get the response
        """
        cmd_slug = '*%s\r\n$%s\r\n%s\r\n' % ((len(args)+1),len(cmd),cmd)
        for arg in args:
            cmd_slug += '$%s\r\n%s\r\n' % (len(arg),arg)
        self.sock.send(cmd_slug)
        resp_data = ''
        #put proper wait to recv here
        resp_data += self.sock.recv(1024)
        return self._parse_response(resp_data)

    def _parse_response(self,response_string):
        """
        Parse a response from the server
        """
        if response_string[0] == '-':
            #response is an error
            success = False
            raise RedisConException(response_string[1:])
        elif response_string[0] == '+':
            #response is a status reply
            success = True
            ret_val = response_string[1:].strip()
        elif response_string[0] == ':':
            #response is an int
            ret_val = int(response_string[1:].strip())
        elif response_string[0] == '$':
            #response is bulk reply
            pattern = re.compile('\$[0-9]+\r\n(?P<response>.+)\r\n')
            ret_val = pattern.match(response_string).group('response')
        return ret_val

    def sadd(self,key,value):
        resp = self._send_cmd('SADD',key,value)
        return resp

    def sismember(self,key,value):
        resp = self._send_cmd('SISMEMBER',key,value)
        return resp

    def type(self,key):
        resp = self._send_cmd('TYPE',key)
        return resp


def sadd(key,value):
    r = RedisCon()
    response = r.sadd(key,value)
    return response

def sismember(key,value):
    r = RedisCon()
    response = r.sismember(key,value)
    return response


if __name__ == '__main__':
    log.info('%s new members added to set',sadd('test','testing'))
    assert sismember('test','testing')



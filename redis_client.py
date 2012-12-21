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

    Might need to add implementation specific stuff later
    """
    def __init__(self,message):
        Exception.__init__(self,message)

class RedisCon:
    """ The simplest of redis clients, at localhost for demo purposes"""

    def __init__(self,host_ip ='127.0.0.1',host_port=6379):
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((host_ip,host_port))
        except socket.error:
            #connection is bad, print msg and exit
            print 'No server running at at %s:%s' % (host_ip,host_port)
            sys.exit()

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
        self.sock.settimeout(5.0)
        try:
            resp_data += self.sock.recv(1024)
        except socket.timeout:
            raise Exception('The connection with the server timed out while receiving a response')
        return self._parse_response(resp_data)

    def _parse_response(self,response_string):
        """
        Parse a response from the server
        """
        if response_string[0] == '-':
            #response is an error
            raise RedisConException(response_string[1:])
        elif response_string[0] == '+':
            #response is a status reply
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

    def __del__(self):
        self.sock.close()


def sadd(key,value):
    r = RedisCon()
    response = r.sadd(key,value)
    return response

def sismember(key,value):
    r = RedisCon()
    response = r.sismember(key,value)
    return response


if __name__ == '__main__':
    print type(sadd('me','you'))
    print type(sismember('me','you'))




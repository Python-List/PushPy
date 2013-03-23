#!/usr/bin/python2.7
import json
import os,sys
from flask import flash

class pushclass(object):
    @staticmethod
    def send_push_message(tokens,devmode,payload):
        import ssl
        import socket
        import struct
        import binascii

        certfile=None
        apn_address=None
        if(devmode):
            certfile= os.path.abspath(os.path.dirname(__file__))+ '/dev.pem'
            apns_address = ('gateway.sandbox.push.apple.com', 2195)
        else:
            certfile= os.path.abspath(os.path.dirname(__file__))+ '/dist.pem'
            apns_address = ('gateway.push.apple.com', 2195)

        try:
            # create socket and connect to APNS server using SSL
            s = socket.socket()
            sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=certfile)
            sock.connect(apns_address)
            # generate APNS notification packet
            #print 'Enviando notificaciones a '+str(len(tokens)) +" usuarios"
            flash('Notifications sent to '+str(len(tokens)) +" users")
            for user in tokens:
                token = binascii.unhexlify(user.token)
                fmt = "!cH32sH{0:d}s".format(len(payload))
                cmd = '\x00'
                msg = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
                sock.write(msg)
            sock.close()
            s.close()
        except ssl.SSLError:
            print('>Error with certificates, check it!')
            flash('Bad certificates')

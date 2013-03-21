#!/usr/bin/python2.7
import json
import os
from flask import flash

class pushclass(object):
    @staticmethod
    def send_push_message(tokens,payload):
        import ssl
        import socket
        import struct
        import binascii
        # the certificate file generated from Provisioning Portal
        certfile= os.path.abspath(os.path.dirname(__file__))+ '/dev.pem'
        #certfile= os.path.abspath(os.path.dirname(__file__))+ '/dist.pem'


        # APNS server address (use 'gateway.push.apple.com' for production server)
        apns_address = ('gateway.push.apple.com', 2195)

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

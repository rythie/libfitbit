#!/usr/bin/env python
#################################################################
# pyusb access for ant devices
# By Kyle Machulis <kyle@nonpolynomial.com>
# http://www.nonpolynomial.com
#
# Licensed under the BSD License, as follows
#
# Copyright (c) 2011, Kyle Machulis/Nonpolynomial Labs
# All rights reserved.
#
# Redistribution and use in source and binary forms, 
# with or without modification, are permitted provided 
# that the following conditions are met:
#
#    * Redistributions of source code must retain the 
#      above copyright notice, this list of conditions 
#      and the following disclaimer.
#    * Redistributions in binary form must reproduce the 
#      above copyright notice, this list of conditions and 
#      the following disclaimer in the documentation and/or 
#      other materials provided with the distribution.
#    * Neither the name of the Nonpolynomial Labs nor the names 
#      of its contributors may be used to endorse or promote 
#      products derived from this software without specific 
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################
#

from protocol import ANT, ANTReceiveException
import usb
import operator

class ANTlibusb(ANT):
    ep = { 'in'  : 0x81, \
           'out' : 0x01
           }

    def __init__(self, chan=0x0, debug=False):
        super(ANTlibusb, self).__init__(chan, debug)
        self._connection = False
        self.timeout = 1000

    def open(self, vid, pid):
        self._connection = usb.core.find(idVendor = vid,
                                         idProduct = pid)
        if self._connection is None:
            return False

        self._connection.set_configuration()
        return True

    def close(self):
        if self._connection is not None:
            self._connection = None

    def _send(self, command):
        # libusb expects ordinals, it'll redo the conversion itself.
        c = command
        self._connection.write(self.ep['out'], map(ord, c), 0, 100)

    def _receive(self, size=4096):
        r = self._connection.read(self.ep['in'], size, 0, self.timeout)
        if len(r) == 0:
            return r
        checksum = reduce(operator.xor, r[:-1])
        if checksum != r[-1]:
            raise ANTReceiveException("Checksums for packet do not match received values!")
        if self._debug:
            self.data_received(''.join(map(chr, r)))
        return r

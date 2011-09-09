# Copyright (c) 2011, Casey Link <unnamedrambler@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the organization nor the
#      names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Casey Link BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from twisted.internet import protocol
import pickle
import logging

import targets

command = "./worker.py"

class ServiceProtocol(protocol.ProcessProtocol):

    def __init__(self, target):
        self.target = target
        self.data = ''
        self.err_data = ''

    def connectionMade(self):
        self.transport.write( pickle.dumps(self.target) )
        self.transport.closeStdin()

    def outReceived(self, data):
        self.data += data

    def errReceived(self, data):
        self.err_data  += data

    def outConnectionLost(self):
        # TODO impl
        pass

    def processExited(self, reason):
        logging.info("Output: " + self.data)
        logging.info("Errors: " + self.err_data)
        status = reason.value.exitCode
        if status == 0:
            response = pickle.loads(self.data)
            # TODO impl



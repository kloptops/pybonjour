#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- python -*-
from __future__ import unicode_literals, print_function

import time
import select
import sys
import pybonjour


class BasicResolver(object):
    def __init__(self, regtype, timeout=5):
        self.regtype = regtype
        self.timeout = 5
        self.resolved = {}
        self.sdRef = None

    def open(self, regtype=None):
        assert self.sdRef is None

        if regtype is None:
            regtype = self.regtype

        self.sdRef = pybonjour.DNSServiceBrowse(
            regtype=self.regtype, callBack=self._browse_callback)
        self.resolved.clear()

    def close(self):
        if self.sdRef is not None:
            self.sdRef.close()
            self.resolved.clear()

    def process(self):
        assert self.sdRef is not None

        ready = select.select([self.sdRef], [], [], 0)
        if self.sdRef in ready[0]:
            pybonjour.DNSServiceProcessResult(self.sdRef)

    def __del__(self):
        self.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _resolve_callback(
            self, sdRef, flags, interfaceIndex, errorCode, fullname,
            hosttarget, port, txtRecord):

        if errorCode == pybonjour.kDNSServiceErr_NoError:
            txt = pybonjour.TXTRecord.parse(txtRecord)

            print(u'Resolved service:')
            print(u'  fullname   =', fullname)
            print(u'  hosttarget =', hosttarget)
            print(u'  port       =', port)
            print(u'  txtRecord  =', repr(txt))
            self.resolved[fullname] = (hosttarget, port)

    def _browse_callback(
            self, sdRef, flags, interfaceIndex, errorCode, serviceName,
            regtype, replyDomain):

        print('- ', flags, interfaceIndex, errorCode, serviceName,
            regtype, replyDomain)

        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return

        if not (flags & pybonjour.kDNSServiceFlagsAdd):
            fullname = pybonjour.DNSServiceConstructFullName(
                serviceName, regtype, replyDomain)
            print('Service removed - ', fullname)
            if fullname in self.resolved:
                del self.resolved[fullname]
            return

        print('Service added; resolving')

        with pybonjour.DNSServiceResolve(
                0, interfaceIndex, serviceName, regtype, replyDomain,
                self._resolve_callback) as resolve_sdRef:

            ready = select.select([resolve_sdRef], [], [], self.timeout)
            if resolve_sdRef not in ready[0]:
                print('Resolve timed out')
                return

            pybonjour.DNSServiceProcessResult(resolve_sdRef)


def main(argv):
    regtype  = argv[1]

    with BasicResolver(regtype) as resolver:
        try:
            while True:
                resolver.process()
                time.sleep(0.1)

        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main(sys.argv)

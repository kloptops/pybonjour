#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- python -*-
from __future__ import unicode_literals, print_function

import select
import sys
import pybonjour


def register_callback(sdRef, flags, errorCode, name, regtype, domain):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        print('Registered service:')
        print('  name    =', name)
        print('  regtype =', regtype)
        print('  domain  =', domain)


def main(argv):
    name    = argv[1]
    regtype = argv[2]
    port    = int(argv[3])

    with pybonjour.DNSServiceRegister(
            name=name, regtype=regtype, port=port,
            callBack=register_callback) as sdRef:

        try:
            while True:
                ready = select.select([sdRef], [], [])
                if sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(sdRef)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main(sys.argv)

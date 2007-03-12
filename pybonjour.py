################################################################################
#
# Copyright (c) 2007 Christopher J. Stawarz
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################



#
# NOTE:
#
# To use this module with Python 2.4, you'll need to install ctypes
# 1.0.1 or later.  Starting with Python 2.5, ctypes is part of the
# standard library, so no additional software is required.
#


"""

Pure-Python bindings for Apple's Bonjour library

"""


import ctypes
import os
import socket
import sys


if sys.platform == 'win32':
    # Need to use the stdcall variants
    _libdnssd = ctypes.windll.dnssd
    _CFunc = ctypes.WINFUNCTYPE
else:
    if sys.platform == 'darwin':
	_libdnssd = 'libSystem.B.dylib'
    else:
	_libdnssd = 'libdns_sd.so'
	# If libdns_sd is actually Avahi's Bonjour compatibility
	# layer, silence its annoying warning messages
	os.environ['AVAHI_COMPAT_NOWARN'] = '1'
    _libdnssd = ctypes.cdll.LoadLibrary(_libdnssd)
    _CFunc = ctypes.CFUNCTYPE



################################################################################
#
# Constants
#
################################################################################



#
# General flags
#

kDNSServiceFlagsMoreComing          = 0x1
kDNSServiceFlagsAdd                 = 0x2
kDNSServiceFlagsDefault             = 0x4
kDNSServiceFlagsNoAutoRename        = 0x8
kDNSServiceFlagsShared              = 0x10
kDNSServiceFlagsUnique              = 0x20
kDNSServiceFlagsBrowseDomains       = 0x40
kDNSServiceFlagsRegistrationDomains = 0x80
kDNSServiceFlagsLongLivedQuery      = 0x100
kDNSServiceFlagsAllowRemoteQuery    = 0x200
kDNSServiceFlagsForceMulticast      = 0x400
kDNSServiceFlagsReturnCNAME         = 0x800


#
# Service classes
#

kDNSServiceClass_IN                 = 1


#
# Service types
#

kDNSServiceType_A                   = 1
kDNSServiceType_NS                  = 2
kDNSServiceType_MD                  = 3
kDNSServiceType_MF                  = 4
kDNSServiceType_CNAME               = 5
kDNSServiceType_SOA                 = 6
kDNSServiceType_MB                  = 7
kDNSServiceType_MG                  = 8
kDNSServiceType_MR                  = 9
kDNSServiceType_NULL                = 10
kDNSServiceType_WKS                 = 11
kDNSServiceType_PTR                 = 12
kDNSServiceType_HINFO               = 13
kDNSServiceType_MINFO               = 14
kDNSServiceType_MX                  = 15
kDNSServiceType_TXT                 = 16
kDNSServiceType_RP                  = 17
kDNSServiceType_AFSDB               = 18
kDNSServiceType_X25                 = 19
kDNSServiceType_ISDN                = 20
kDNSServiceType_RT                  = 21
kDNSServiceType_NSAP                = 22
kDNSServiceType_NSAP_PTR            = 23
kDNSServiceType_SIG                 = 24
kDNSServiceType_KEY                 = 25
kDNSServiceType_PX                  = 26
kDNSServiceType_GPOS                = 27
kDNSServiceType_AAAA                = 28
kDNSServiceType_LOC                 = 29
kDNSServiceType_NXT                 = 30
kDNSServiceType_EID                 = 31
kDNSServiceType_NIMLOC              = 32
kDNSServiceType_SRV                 = 33
kDNSServiceType_ATMA                = 34
kDNSServiceType_NAPTR               = 35
kDNSServiceType_KX                  = 36
kDNSServiceType_CERT                = 37
kDNSServiceType_A6                  = 38
kDNSServiceType_DNAME               = 39
kDNSServiceType_SINK                = 40
kDNSServiceType_OPT                 = 41
kDNSServiceType_TKEY                = 249
kDNSServiceType_TSIG                = 250
kDNSServiceType_IXFR                = 251
kDNSServiceType_AXFR                = 252
kDNSServiceType_MAILB               = 253
kDNSServiceType_MAILA               = 254
kDNSServiceType_ANY                 = 255


#
# Error codes
#

kDNSServiceErr_NoError              = 0
kDNSServiceErr_Unknown              = -65537
kDNSServiceErr_NoSuchName           = -65538
kDNSServiceErr_NoMemory             = -65539
kDNSServiceErr_BadParam             = -65540
kDNSServiceErr_BadReference         = -65541
kDNSServiceErr_BadState             = -65542
kDNSServiceErr_BadFlags             = -65543
kDNSServiceErr_Unsupported          = -65544
kDNSServiceErr_NotInitialized       = -65545
kDNSServiceErr_AlreadyRegistered    = -65547
kDNSServiceErr_NameConflict         = -65548
kDNSServiceErr_Invalid              = -65549
kDNSServiceErr_Firewall             = -65550
kDNSServiceErr_Incompatible         = -65551
kDNSServiceErr_BadInterfaceIndex    = -65552
kDNSServiceErr_Refused              = -65553
kDNSServiceErr_NoSuchRecord         = -65554
kDNSServiceErr_NoAuth               = -65555
kDNSServiceErr_NoSuchKey            = -65556
kDNSServiceErr_NATTraversal         = -65557
kDNSServiceErr_DoubleNAT            = -65558
kDNSServiceErr_BadTime              = -65559


#
# Other constants
#

kDNSServiceMaxServiceName           = 64
kDNSServiceMaxDomainName            = 1005
kDNSServiceInterfaceIndexAny        = 0
kDNSServiceInterfaceIndexLocalOnly  = -1



################################################################################
#
# Error handling
#
################################################################################



class BonjourError(Exception):

    _errmsg = {
	kDNSServiceErr_NoSuchName:		'no such name',
	kDNSServiceErr_NoMemory:		'no memory',
	kDNSServiceErr_BadParam:		'bad param',
	kDNSServiceErr_BadReference:		'bad reference',
	kDNSServiceErr_BadState:		'bad state',
	kDNSServiceErr_BadFlags:		'bad flags',
	kDNSServiceErr_Unsupported:		'unsupported',
	kDNSServiceErr_NotInitialized:		'not initialized',
	kDNSServiceErr_AlreadyRegistered:	'already registered',
	kDNSServiceErr_NameConflict:		'name conflict',
	kDNSServiceErr_Invalid:			'invalid',
	kDNSServiceErr_Firewall:		'firewall',
	kDNSServiceErr_Incompatible:		'incompatible',
	kDNSServiceErr_BadInterfaceIndex:	'bad interface index',
	kDNSServiceErr_Refused:			'refused',
	kDNSServiceErr_NoSuchRecord:		'no such record',
	kDNSServiceErr_NoAuth:			'no auth',
	kDNSServiceErr_NoSuchKey:		'no such key',
	kDNSServiceErr_NATTraversal:		'NAT traversal',
	kDNSServiceErr_DoubleNAT:		'double NAT',
	kDNSServiceErr_BadTime:			'bad time',
	}

    @classmethod
    def _errcheck(cls, result, func, args):
	if result != kDNSServiceErr_NoError:
	    raise cls(result)
	return args

    def __init__(self, errorCode):
	Exception.__init__(self,
			   (errorCode, self._errmsg.get(errorCode, 'unknown')))



################################################################################
#
# Data types
#
################################################################################



class _utf8_char_p(ctypes.c_char_p):

    @classmethod
    def from_param(cls, obj):
	if (obj is not None) and (not isinstance(obj, cls)):
	    if not isinstance(obj, basestring):
		raise TypeError('parameter must be a string type instance')
	    if not isinstance(obj, unicode):
		obj = unicode(obj)
	    obj = obj.encode('utf-8')
	return ctypes.c_char_p.from_param(obj)

    def decode(self):
	if self.value is None:
	    return None
	return self.value.decode('utf-8')


class _utf8_char_p_non_null(_utf8_char_p):

    @classmethod
    def from_param(cls, obj):
	if obj is None:
	    raise ValueError('parameter cannot be None')
	return _utf8_char_p.from_param(obj)


_DNSServiceFlags     = ctypes.c_uint32
_DNSServiceErrorType = ctypes.c_int32


#
# FIXME:
#
# How do we prevent users from creating DNSRecordRef's and
# DNSServiceRef's with random values?
#


class DNSRecordRef(ctypes.c_void_p):

    @classmethod
    def from_param(cls, obj):
	if type(obj) is not cls:
	    raise TypeError("expected '%s', got '%s'" %
			    (cls.__name__, type(obj).__name__))
	if obj.value is None:
	    raise ValueError('invalid %s instance' % cls.__name__)
	return obj

    def __eq__(self, other):
	return ((type(other) is type(self)) and	(other.value == self.value))

    def _invalidate(self):
	self.value = None

    def _valid(self):
	return (self.value is not None)


class _DNSRecordRef_or_null(DNSRecordRef):

    @classmethod
    def from_param(cls, obj):
	if obj is None:
	    return obj
	return DNSRecordRef.from_param(obj)


class DNSServiceRef(DNSRecordRef):

    def __init__(self, *args, **kwargs):
	DNSRecordRef.__init__(self, *args, **kwargs)

	# A DNSRecordRef is invalidated if DNSServiceRefDeallocate()
	# is called on the corresponding DNSServiceRef, so we need to
	# keep track of all our record refs and invalidate them when
	# we're closed.
	self._record_refs = []

    def _add_record_ref(self, ref):
	self._record_refs.append(ref)

    def close(self):
	if self._valid():
	    for ref in self._record_refs:
		ref._invalidate()
	    _DNSServiceRefDeallocate(self)
	    self._invalidate()

    def fileno(self):
	return _DNSServiceRefSockFD(self)


_DNSServiceDomainEnumReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# replyDomain
    ctypes.c_void_p,		# context
    )


_DNSServiceRegisterReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# name
    _utf8_char_p,		# regtype
    _utf8_char_p,		# domain
    ctypes.c_void_p,		# context
    )


_DNSServiceBrowseReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# serviceName
    _utf8_char_p,		# regtype
    _utf8_char_p,		# replyDomain
    ctypes.c_void_p,		# context
    )


_DNSServiceResolveReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# fullname
    _utf8_char_p,		# hosttarget
    ctypes.c_uint16,		# port
    ctypes.c_uint16,		# txtLen
    ctypes.c_void_p,		# txtRecord (not null-terminated, so c_void_p)
    ctypes.c_void_p,		# context
    )


_DNSServiceRegisterRecordReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    DNSRecordRef,		# RecordRef
    _DNSServiceFlags,		# flags
    _DNSServiceErrorType,	# errorCode
    ctypes.c_void_p,		# context
    )


_DNSServiceQueryRecordReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# fullname
    ctypes.c_uint16,		# rrtype
    ctypes.c_uint16,		# rrclass
    ctypes.c_uint16,		# rdlen
    ctypes.c_void_p,		# rdata
    ctypes.c_uint32,		# ttl
    ctypes.c_void_p,		# context
    )



################################################################################
#
# Low-level function bindings
#
################################################################################



def _create_function_bindings():

    ERRCHECK    = True
    NO_ERRCHECK = False

    OUTPARAM    = (lambda index: index)
    NO_OUTPARAM = None

    specs = {

	#'funcname':
	#(
	#    return_type,
	#    errcheck,
	#    outparam,
	#    (
	#	param_1_type,
	#	param_2_type,
	#	...
	#	param_n_type,
	#	)),

	'DNSServiceRefSockFD':
	(
	    ctypes.c_int,
	    NO_ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		)),

	'DNSServiceProcessResult':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		)),

	'DNSServiceRefDeallocate':
	(
	    None,
	    NO_ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		)),

	'DNSServiceEnumerateDomains':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_DNSServiceDomainEnumReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceRegister':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p,			# name
		_utf8_char_p_non_null,		# regtype
		_utf8_char_p,			# domain
		_utf8_char_p,			# host
		ctypes.c_uint16,		# port
		ctypes.c_uint16,		# txtLen
		ctypes.c_void_p,		# txtRecord
		_DNSServiceRegisterReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceAddRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(1),
	    (
		DNSServiceRef,			# sdRef
		ctypes.POINTER(DNSRecordRef),	# RecordRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint16,		# rrtype
		ctypes.c_uint16,		# rdlen
		ctypes.c_void_p,		# rdata
		ctypes.c_uint32,		# ttl
		)),

	'DNSServiceUpdateRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		_DNSRecordRef_or_null,		# RecordRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint16,		# rdlen
		ctypes.c_void_p,		# rdata
		ctypes.c_uint32,		# ttl
		)),

	'DNSServiceRemoveRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		DNSRecordRef,			# RecordRef
		_DNSServiceFlags,		# flags
		)),

	'DNSServiceBrowse':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# regtype
		_utf8_char_p,			# domain
		_DNSServiceBrowseReply,		# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceResolve':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# name
		_utf8_char_p_non_null,		# regtype
		_utf8_char_p_non_null,		# domain
		_DNSServiceResolveReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceCreateConnection':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		)),

	'DNSServiceRegisterRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(1),
	    (
		DNSServiceRef,			# sdRef
		ctypes.POINTER(DNSRecordRef),	# RecordRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# fullname
		ctypes.c_uint16,		# rrtype
		ctypes.c_uint16,		# rrclass
		ctypes.c_uint16,		# rdlen
		ctypes.c_void_p,		# rdata
		ctypes.c_uint32,		# ttl
		_DNSServiceRegisterRecordReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceQueryRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# fullname
		ctypes.c_uint16,		# rrtype
		ctypes.c_uint16,		# rrclass
		_DNSServiceQueryRecordReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceReconfirmRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    NO_OUTPARAM,
	    (
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# fullname
		ctypes.c_uint16,		# rrtype
		ctypes.c_uint16,		# rrclass
		ctypes.c_uint16,		# rdlen
		ctypes.c_void_p,		# rdata
		)),

	'DNSServiceConstructFullName':
	(
	    ctypes.c_int,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.c_char * kDNSServiceMaxDomainName,	# fullName
		_utf8_char_p,					# service
		_utf8_char_p_non_null,				# regtype
		_utf8_char_p_non_null,				# domain
		)),

	}


    for name, (restype, errcheck, outparam, argtypes) in specs.iteritems():
	prototype = _CFunc(restype, *argtypes)

	paramflags = [1] * len(argtypes)
	if outparam is not None:
	    paramflags[outparam] = 2
	paramflags = tuple((val,) for val in paramflags)

	func = prototype((name, _libdnssd), paramflags)

	if errcheck:
	    func.errcheck = BonjourError._errcheck

	globals()['_' + name] = func


# Only need to do this once
_create_function_bindings()



################################################################################
#
# Internal utility types and functions
#
################################################################################



class _NoDefault(object):

    def __repr__(self):
	return '<NO DEFAULT>'

    def check(self, obj):
	if obj is self:
	    raise ValueError('required parameter value missing')

_NO_DEFAULT = _NoDefault()


def _string_to_length_and_void_p(string):
    void_p = ctypes.cast(ctypes.c_char_p(string), ctypes.c_void_p)
    return len(string), void_p


def _length_and_void_p_to_string(length, void_p):
    char_p = ctypes.cast(void_p, ctypes.POINTER(ctypes.c_char))
    return ''.join(char_p[i] for i in xrange(length))



################################################################################
#
# High-level functions
#
################################################################################



def DNSServiceProcessResult(
    sdRef,
    ):

    """

    Read a reply from the daemon, calling the appropriate application
    callback.  This call will block until the daemon's response is
    received.  Use sdRef in conjunction with a run loop or select() to
    determine the presence of a response from the server before
    calling this function to process the reply without blocking.  Call
    this function at any point if it is acceptable to block until the
    daemon's response arrives.  Note that the client is responsible
    for ensuring that DNSServiceProcessResult() is called whenever
    there is a reply from the daemon; the daemon may terminate its
    connection with a client that does not process the daemon's
    responses.

      sdRef:
        A DNSServiceRef returned by any of the DNSService calls that
	take a callback parameter.

    """

    _DNSServiceProcessResult(sdRef)


def DNSServiceEnumerateDomains(
    flags,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    callBack = None,
    ):

    """

    Asynchronously enumerate domains available for browsing and
    registration.

    The enumeration MUST be cancelled by closing the returned
    DNSServiceRef when no more domains are to be found.

      flags:
        Possible values are:
          kDNSServiceFlagsBrowseDomains to enumerate domains
	  recommended for browsing.
	  kDNSServiceFlagsRegistrationDomains to enumerate domains
	  recommended for registration.

      interfaceIndex:
        If non-zero, specifies the interface on which to look for
	domains.  (The index for a given interface is determined via
	the if_nametoindex() family of calls.)  Most applications will
	pass kDNSServiceInterfaceIndexAny to enumerate domains on all
	interfaces.

      callBack:
        The function to be called when a domain is found or the call
	asynchronously fails.  Its signature should be
	callBack(sdRef,	flags, interfaceIndex, errorCode, replyDomain).

      return value:
        A DNSServiceRef instance.

    Callback Parameters:

      sdRef:
        The DNSServiceRef initialized by DNSServiceEnumerateDomains().

      flags:
        Possible values are:
          kDNSServiceFlagsMoreComing
	  kDNSServiceFlagsAdd
	  kDNSServiceFlagsDefault

      interfaceIndex:
        Specifies the interface on which the domain exists.  (The
        index for a given interface is determined via the
        if_nametoindex() family of calls.)

      errorCode:
        Will be kDNSServiceErr_NoError on success, otherwise indicates
	the failure that occurred (in which case other parameters are
	undefined).

      replyDomain:
        The name of the domain.

    """

    @_DNSServiceDomainEnumReply
    def _callback(sdRef, flags, interfaceIndex, errorCode, replyDomain,
		  context):
	if callBack is not None:
	    callBack(sdRef, flags, interfaceIndex, errorCode,
		     replyDomain.decode())

    return _DNSServiceEnumerateDomains(flags,
				       interfaceIndex,
				       _callback,
				       None)


def DNSServiceRegister(
    flags = 0,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    name = None,
    regtype = _NO_DEFAULT,
    domain = None,
    host = None,
    port = _NO_DEFAULT,
    txtRecord = '',
    callBack = None,
    ):

    _NO_DEFAULT.check(regtype)
    _NO_DEFAULT.check(port)

    port = socket.htons(port)

    if not txtRecord:
	txtLen, txtRecord = 1, '\0'
    else:
	txtLen, txtRecord = _string_to_length_and_void_p(txtRecord)

    @_DNSServiceRegisterReply
    def _callback(sdRef, flags, errorCode, name, regtype, domain, context):
	if callBack is not None:
	    callBack(sdRef, flags, errorCode, name.decode(), regtype.decode(),
		     domain.decode())

    return _DNSServiceRegister(flags,
			       interfaceIndex,
			       name,
			       regtype,
			       domain,
			       host,
			       port,
			       txtLen,
			       txtRecord,
			       _callback,
			       None)


def DNSServiceAddRecord(
    sdRef,
    flags = 0,
    rrtype = _NO_DEFAULT,
    rdata = _NO_DEFAULT,
    ttl = 0,
    ):

    _NO_DEFAULT.check(rrtype)
    _NO_DEFAULT.check(rdata)

    rdlen, rdata = _string_to_length_and_void_p(rdata)

    RecordRef = _DNSServiceAddRecord(sdRef,
				     flags,
				     rrtype,
				     rdlen,
				     rdata,
				     ttl)

    sdRef._add_record_ref(RecordRef)

    return RecordRef


def DNSServiceUpdateRecord(
    sdRef,
    RecordRef = None,
    flags = 0,
    rdata = _NO_DEFAULT,
    ttl = 0,
    ):

    _NO_DEFAULT.check(rdata)

    rdlen, rdata = _string_to_length_and_void_p(rdata)

    _DNSServiceUpdateRecord(sdRef,
			    RecordRef,
			    flags,
			    rdlen,
			    rdata,
			    ttl)


def DNSServiceRemoveRecord(
    sdRef,
    RecordRef,
    flags = 0,
    ):

    _DNSServiceRemoveRecord(sdRef,
			    RecordRef,
			    flags)

    RecordRef._invalidate()


def DNSServiceBrowse(
    flags = 0,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    regtype = _NO_DEFAULT,
    domain = None,
    callBack = None,
    ):

    _NO_DEFAULT.check(regtype)

    @_DNSServiceBrowseReply
    def _callback(sdRef, flags, interfaceIndex, errorCode, serviceName, regtype,
		  replyDomain, context):
	if callBack is not None:
	    callBack(sdRef, flags, interfaceIndex, errorCode,
		     serviceName.decode(), regtype.decode(),
		     replyDomain.decode())

    return _DNSServiceBrowse(flags,
			     interfaceIndex,
			     regtype,
			     domain,
			     _callback,
			     None)


def DNSServiceResolve(
    flags = 0,
    interfaceIndex = _NO_DEFAULT,
    name = _NO_DEFAULT,
    regtype = _NO_DEFAULT,
    domain = _NO_DEFAULT,
    callBack = None,
    ):

    _NO_DEFAULT.check(interfaceIndex)
    _NO_DEFAULT.check(name)
    _NO_DEFAULT.check(regtype)
    _NO_DEFAULT.check(domain)

    @_DNSServiceResolveReply
    def _callback(sdRef, flags, interfaceIndex, errorCode, fullname, hosttarget,
		  port, txtLen, txtRecord, context):
	if callBack is not None:
	    port = socket.ntohs(port)
	    txtRecord = _length_and_void_p_to_string(txtLen, txtRecord)
	    callBack(sdRef, flags, interfaceIndex, errorCode, fullname.decode(),
		     hosttarget.decode(), port, txtRecord)

    return _DNSServiceResolve(flags,
			      interfaceIndex,
			      name,
			      regtype,
			      domain,
			      _callback,
			      None)


def DNSServiceCreateConnection():

    return _DNSServiceCreateConnection()


def DNSServiceRegisterRecord(
    sdRef,
    flags,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    fullname = _NO_DEFAULT,
    rrtype = _NO_DEFAULT,
    rrclass = kDNSServiceClass_IN,
    rdata = _NO_DEFAULT,
    ttl = 0,
    callBack = None,
    ):

    _NO_DEFAULT.check(fullname)
    _NO_DEFAULT.check(rrtype)
    _NO_DEFAULT.check(rdata)

    rdlen, rdata = _string_to_length_and_void_p(rdata)

    @_DNSServiceRegisterRecordReply
    def _callback(sdRef, RecordRef, flags, errorCode, context):
	if callBack is not None:
	    callBack(sdRef, RecordRef, flags, errorCode)

    RecordRef = _DNSServiceRegisterRecord(sdRef,
					  flags,
					  interfaceIndex,
					  fullname,
					  rrtype,
					  rrclass,
					  rdlen,
					  rdata,
					  ttl,
					  _callback,
					  None)

    sdRef._add_record_ref(RecordRef)

    return RecordRef


def DNSServiceQueryRecord(
    flags = 0,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    fullname = _NO_DEFAULT,
    rrtype = _NO_DEFAULT,
    rrclass = kDNSServiceClass_IN,
    callBack = None,
    ):

    _NO_DEFAULT.check(fullname)
    _NO_DEFAULT.check(rrtype)

    @_DNSServiceQueryRecordReply
    def _callback(sdRef, flags, interfaceIndex, errorCode, fullname, rrtype,
		  rrclass, rdlen, rdata, ttl, context):
	if callBack is not None:
	    rdata = _length_and_void_p_to_string(rdlen, rdata)
	    callBack(sdRef, flags, interfaceIndex, errorCode, fullname.decode(),
		     rrtype, rrclass, rdata, ttl)

    return _DNSServiceQueryRecord(flags,
				  interfaceIndex,
				  fullname,
				  rrtype,
				  rrclass,
				  _callback,
				  None)


def DNSServiceReconfirmRecord(
    flags = 0,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    fullname = _NO_DEFAULT,
    rrtype = _NO_DEFAULT,
    rrclass = kDNSServiceClass_IN,
    rdata = _NO_DEFAULT,
    ):

    _NO_DEFAULT.check(fullname)
    _NO_DEFAULT.check(rrtype)
    _NO_DEFAULT.check(rdata)

    rdlen, rdata = _string_to_length_and_void_p(rdata)

    _DNSServiceReconfirmRecord(flags,
			       interfaceIndex,
			       fullname,
			       rrtype,
			       rrclass,
			       rdlen,
			       rdata)


def DNSServiceConstructFullName(
    service = None,
    regtype = _NO_DEFAULT, 
    domain = _NO_DEFAULT,
    ):

    _NO_DEFAULT.check(regtype)
    _NO_DEFAULT.check(domain)

    fullName = _DNSServiceConstructFullName(service, regtype, domain).value

    return fullName.decode('utf-8')



################################################################################
#
# Unit tests
#
################################################################################



if __name__ == '__main__':
    import select
    import threading
    import time
    import unittest


    class TestPyBonjour(unittest.TestCase):

	service_name = 'TestService'
	regtype = '_test._tcp.'
	port = 1111
	fullname = 'TestService._test._tcp.local.'
	timeout = 2

	def test_construct_fullname(self):
	    # Check error handling
	    self.assertRaises(ValueError, DNSServiceConstructFullName, None,
			      None)
	    self.assertRaises(ctypes.ArgumentError, DNSServiceConstructFullName,
			      None, None, None)
	    self.assertRaises(BonjourError, DNSServiceConstructFullName, None,
			      'foo', 'local.')

	    fullname = DNSServiceConstructFullName(self.service_name,
						   self.regtype, 'local.')

	    self.assert_(isinstance(fullname, unicode))
	    if not fullname.endswith(u'.'):
		fullname += u'.'
	    self.assertEqual(fullname, self.fullname)

	def wait_on_event(self, sdRef, event):
	    while not event.isSet():
		ready = select.select([sdRef], [], [], self.timeout)
		self.assert_(sdRef in ready[0], 'operation timed out')
		DNSServiceProcessResult(sdRef)

	def test_enumerate_domains(self):
	    done = threading.Event()

	    def cb(_sdRef, flags, interfaceIndex, errorCode, replyDomain):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(_sdRef, sdRef)
		self.assert_(isinstance(replyDomain, unicode))
		if not (flags & kDNSServiceFlagsMoreComing):
		    done.set()

	    sdRef = \
		DNSServiceEnumerateDomains(kDNSServiceFlagsRegistrationDomains,
					   callBack=cb)

	    try:
		self.wait_on_event(sdRef, done)
	    finally:
		sdRef.close()

	def register_record(self):
	    done = threading.Event()

	    def cb(_sdRef, flags, errorCode, name, regtype, domain):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(_sdRef, sdRef)
		self.assert_(isinstance(name, unicode))
		self.assertEqual(name, self.service_name)
		self.assert_(isinstance(regtype, unicode))
		self.assertEqual(regtype, self.regtype)
		self.assert_(isinstance(domain, unicode))
		done.set()

	    sdRef = DNSServiceRegister(name=self.service_name,
				       regtype=self.regtype,
				       port=self.port,
				       callBack=cb)

	    return done, sdRef

	def test_register_browse_resolve(self):
	    browse_done = threading.Event()
	    resolve_done = threading.Event()

	    def register_cb(sdRef, flags, errorCode, name, regtype, domain):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(sdRef, register_sdRef)
		self.assert_(isinstance(name, unicode))
		self.assertEqual(name, self.service_name)
		self.assert_(isinstance(regtype, unicode))
		self.assertEqual(regtype, self.regtype)
		self.assert_(isinstance(domain, unicode))
		register_done.set()

	    def browse_cb(sdRef, flags, interfaceIndex, errorCode, serviceName,
			  regtype, replyDomain):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(sdRef, browse_sdRef)
		self.assert_(flags & kDNSServiceFlagsAdd)
		self.assert_(isinstance(serviceName, unicode))
		self.assertEqual(serviceName, self.service_name)
		self.assert_(isinstance(regtype, unicode))
		self.assertEqual(regtype, self.regtype)
		self.assert_(isinstance(replyDomain, unicode))

		def resolve_cb(sdRef, flags, interfaceIndex, errorCode,
			       fullname, hosttarget, port, txtRecord):
		    self.assertEqual(errorCode, kDNSServiceErr_NoError)
		    self.assertEqual(sdRef, resolve_sdRef)
		    self.assert_(isinstance(fullname, unicode))
		    self.assertEqual(fullname, self.fullname)
		    self.assert_(isinstance(hosttarget, unicode))
		    self.assertEqual(port, self.port)
		    self.assert_(isinstance(txtRecord, str))
		    self.assert_(len(txtRecord) > 0)
		    resolve_done.set()

		resolve_sdRef = DNSServiceResolve(0, interfaceIndex,
						  serviceName, regtype,
						  replyDomain, resolve_cb)

		try:
		    self.wait_on_event(resolve_sdRef, resolve_done)
		finally:
		    resolve_sdRef.close()

		browse_done.set()

	    register_done, register_sdRef = self.register_record()

	    try:
		self.wait_on_event(register_sdRef, register_done)

		browse_sdRef = DNSServiceBrowse(regtype=self.regtype,
						callBack=browse_cb)

		try:
		    self.wait_on_event(browse_sdRef, browse_done)
		finally:
		    browse_sdRef.close()
	    finally:
		register_sdRef.close()

	def query_record(self, rrtype, rdata):
	    # Give record time to be updated...
	    time.sleep(5)

	    done = threading.Event()

	    def cb(_sdRef, flags, interfaceIndex, errorCode, fullname, _rrtype,
		   rrclass, _rdata, ttl):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(_sdRef, sdRef)
		self.assert_(isinstance(fullname, unicode))
		self.assertEqual(fullname, self.fullname)
		self.assertEqual(_rrtype, rrtype)
		self.assertEqual(rrclass, kDNSServiceClass_IN)
		self.assert_(isinstance(_rdata, str))
		self.assertEqual(_rdata, rdata)
		done.set()

	    sdRef = DNSServiceQueryRecord(fullname=self.fullname,
					  rrtype=rrtype,
					  callBack=cb)

	    try:
		self.wait_on_event(sdRef, done)
	    finally:
		sdRef.close()

	def test_addrecord_updaterecord_removerecord(self):
	    done, sdRef = self.register_record()

	    try:
		self.wait_on_event(sdRef, done)

		RecordRef = DNSServiceAddRecord(sdRef,
						rrtype=kDNSServiceType_SINK,
						rdata='foo')
		self.assert_(RecordRef.value is not None)
		self.query_record(kDNSServiceType_SINK, 'foo')

		DNSServiceUpdateRecord(sdRef, RecordRef, rdata='bar')
		self.query_record(kDNSServiceType_SINK, 'bar')

		DNSServiceRemoveRecord(sdRef, RecordRef)
	    finally:
		sdRef.close()

	    self.assert_(RecordRef.value is None)

	def test_createconnection_registerrecord_reconfirmrecord(self):
	    done = threading.Event()

	    def cb(_sdRef, _RecordRef, flags, errorCode):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(_sdRef, sdRef)
		self.assertEqual(_RecordRef, RecordRef)
		done.set()

	    sdRef = DNSServiceCreateConnection()

	    try:
		#
		# FIXME:
		#
		# Obviously, I don't understand how to use these
		# functions, as my tests either fail bizarrely or
		# cause seg faults and the like.  Let's just punt for
		# now...
		#
		RecordRef = DNSRecordRef()

		#RecordRef = \
		#    DNSServiceRegisterRecord(sdRef,
		#			     kDNSServiceFlagsUnique,
		#			     fullname=self.fullname,
		#			     rrtype=kDNSServiceType_SINK,
		#			     rdata='blah',
		#			     callBack=cb)
		#self.assert_(RecordRef.value is not None)

		#self.wait_on_event(sdRef, done)

		#self.query_record(kDNSServiceType_SINK, 'blah')

		#DNSServiceReconfirmRecord(fullname=self.fullname,
		#			  rrtype=kDNSServiceType_SINK,
		#			  rdata='blah')
	    finally:
		sdRef.close()

	    self.assert_(RecordRef.value is None)


    unittest.main()

class PhoisError(Exception):
    pass


class IDNAError(PhoisError):
    pass


class TldsFileError(PhoisError):
    pass


class BadDomainError(PhoisError):
    pass


class NoWhoisServerFoundError(PhoisError):
    pass


class SocketError(PhoisError):
    pass


class SocketTimeoutError(SocketError):
    pass


class SocketBadProxyError(SocketError):
    pass

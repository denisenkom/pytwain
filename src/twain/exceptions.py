class TwainError(Exception):
    pass


class excCapabilityFormatNotSupported(TwainError):
    pass


class excDSTransferCancelled(TwainError):
    pass


class excSMGetProcAddressFailed(TwainError):
    pass


class excSMLoadFileFailed(TwainError):
    pass


class excSMOpenFailed(TwainError):
    pass


class excImageFormat(Exception):
    pass


class excTWCC_BADCAP(TwainError):
    pass


class BadDestination(TwainError):
    """
    Operation was sent to invalid Source
    """
    pass


TWCC_BADDEST = BadDestination


class BadProtocol(TwainError):
    """
    Operation is not recognized by Source
    """
    pass


excTWCC_BADPROTOCOL = BadProtocol


class GeneralFailure(TwainError):
    """General failure.  Unload Source immediately."""
    pass


excTWCC_BUMMER = GeneralFailure


class excTWCC_CAPBADOPERATION(Exception):
    """Operation (i.e., Get or Set)  not supported on capability."""
    pass


class excTWCC_CAPSEQERROR(Exception):
    """Capability has dependencies on other capabilities and
    cannot be operated upon at this time.
    """
    pass


class excTWCC_CAPUNSUPPORTED(Exception):
    """Capability not supported by Source."""
    pass


class excTWCC_CHECKDEVICEONLINE(Exception):
    """Check the device status using CAP_DEVICEONLINE, this
    condition code can be returned by any TWAIN operation
    in state 4 or higher, or from the state 3 DG_CONTROL /
    DAT_IDENTITY / MSG_OPENDS.  The state remains
    unchanged.  If in state 4 the Application can poll with
    CAP_DEVICELINE until the value returns TRUE.
    """
    pass


class excTWCC_DENIED(Exception):
    pass


class excTWCC_FILEEXISTS(Exception):
    pass


class excTWCC_FILENOTFOUND(Exception):
    pass


class excTWCC_FILEWRITEERROR(Exception):
    pass


class excTWCC_MAXCONNECTIONS(Exception):
    pass


class excTWCC_NODS(Exception):
    pass


class excTWCC_NOTEMPTY(Exception):
    pass


class excTWCC_OPERATIONERROR(Exception):
    pass


class excTWCC_PAPERDOUBLEFEED(Exception):
    pass


class excTWCC_PAPERJAM(Exception):
    pass


class excTWCC_SEQERROR(Exception):
    pass


class excTWCC_SUCCESS(Exception):
    pass


class excTWCC_UNKNOWN(Exception):
    pass


class CancelAll(Exception):
    """Exception used by callbacks to cancel remaining image transfers"""
    pass


class CheckStatus(Exception):
    """This exception means that operation succeeded but user value was truncated
    to fit valid range
    """
    pass

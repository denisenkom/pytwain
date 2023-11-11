class TwainError(Exception):
    """
    Base error for all errors returned by TWAIN driver
    """


class CapabilityFormatNotSupported(TwainError):
    """
    Specified capability is not supported by pytwain
    """


class DSTransferCancelled(TwainError):
    """
    Data transfer was cancelled by user
    """


class SMGetProcAddressFailed(TwainError):
    """
    Specified driver does not have DSM_Entry symbol defined
    """


class SMLoadFileFailed(TwainError):
    """
    Failed to load DLL
    """


class SMOpenFailed(TwainError):
    """
    DSM entry point returned error when called.
    """


class ImageFormatNotSupported(TwainError):
    """
    Image has unsupported format.
    E.g. compressed images are not supported currently.
    """


class BadCapability(TwainError):
    """
    Source does not support specified capability.
    Sources newer than 1.6 do not use report this error.
    """


class BadDestination(TwainError):
    """
    Operation was sent to invalid Source
    """


class BadProtocol(TwainError):
    """
    Operation is not recognized by Source
    """


class GeneralFailure(TwainError):
    """General failure.  Unload Source immediately."""


class CapBadOperation(TwainError):
    """Operation (i.e., Get or Set)  not supported on capability."""


class CapSeqError(TwainError):
    """Capability has dependencies on other capabilities and
    cannot be operated upon at this time.
    """


class CapUnsupported(TwainError):
    """
    Capability not supported by Source.
    Sources with version 1.6 and newer use this error instead of BadCapability error
    """


class CheckDeviceOnlineError(TwainError):
    """Check the device status using CAP_DEVICEONLINE, this
    condition code can be returned by any TWAIN operation
    in state 4 or higher, or from the state 3 DG_CONTROL /
    DAT_IDENTITY / MSG_OPENDS.  The state remains
    unchanged.  If in state 4 the Application can poll with
    CAP_DEVICELINE until the value returns TRUE.
    """


class DeniedError(TwainError):
    """
    Operation denied
    """


class FileExistsError(TwainError):
    """
    Specified file already exists.
    """


class FileWriteError(TwainError):
    """
    Operation failed writing to the file.
    """


class MaxConnectionsError(TwainError):
    """
    Device is connected to maximum number of applications it can support.
    """


class NoDataSourceError(TwainError):
    """
    No Source found
    """


class NotEmptyError(TwainError):
    """
    Directory not empty and cannot be deleted
    """


class OperationError(TwainError):
    """Internal Source error"""


class PaperDoubleFeedError(TwainError):
    """
    Feeder error.  This error is obsolete but may still be reported by older sources.
    """


class PaperJam(TwainError):
    """
    Paper got stuck in feeder
    """


class SequenceError(TwainError):
    """
    Operation was called at a wrong state
    """


class UnknownError(TwainError):
    """
    Unknown error code was returned.
    Probably need to upgrade pytds to newer version.
    """


class CancelAll(Exception):
    """Exception used by callbacks to cancel remaining image transfers"""


class CheckStatus(Exception):
    """This exception means that operation succeeded but user value was truncated
    to fit valid range
    """


# Following exception aliases are deprecated
# and will be removed in version 2.4.0
excCapabilityFormatNotSupported = CapabilityFormatNotSupported
excDSTransferCancelled = DSTransferCancelled
excSMGetProcAddressFailed = SMGetProcAddressFailed
excSMLoadFileFailed = SMLoadFileFailed
excSMOpenFailed = SMOpenFailed
excImageFormat = ImageFormatNotSupported
excTWCC_BADCAP = BadCapability
excTWCC_BADDEST = BadDestination
excTWCC_BADPROTOCOL = BadProtocol
excTWCC_BUMMER = GeneralFailure
excTWCC_CAPBADOPERATION = CapBadOperation
excTWCC_CAPSEQERROR = CapSeqError
excTWCC_CAPUNSUPPORTED = CapUnsupported
excTWCC_CHECKDEVICEONLINE = CheckDeviceOnlineError
excTWCC_DENIED = DeniedError
excTWCC_FILEEXISTS = FileExistsError
excTWCC_FILEWRITEERROR = FileWriteError
excTWCC_MAXCONNECTIONS = MaxConnectionsError
excTWCC_NODS = NoDataSourceError
excTWCC_NOTEMPTY = NotEmptyError
excTWCC_OPERATIONERROR = OperationError
excTWCC_PAPERDOUBLEFEED = PaperDoubleFeedError
excTWCC_PAPERJAM = PaperJam
excTWCC_SEQERROR = SequenceError
excTWCC_UNKNOWN = UnknownError

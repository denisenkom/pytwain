import ctypes as ct
from .. import utils


class TW_CAPABILITY(ct.Structure):
    _pack_ = 2
    _fields_ = [("Cap", ct.c_uint16),
                ('ConType', ct.c_uint16),
                ('hContainer', ct.c_void_p)]


class TW_ONEVALUE(ct.Structure):
    _pack_ = 2
    _fields_ = [('ItemType', ct.c_uint16),
                ('Item', ct.c_uint32)]


class TW_FIX32(ct.Structure):
    _pack_ = 2
    _fields_ = [('Whole', ct.c_int16),
                ('Frac', ct.c_uint16)]

    def __str__(self):
        return str(fix2float(self))


class TW_FRAME(ct.Structure):
    _pack_ = 2
    _fields_ = [('Left', TW_FIX32),
                ('Top', TW_FIX32),
                ('Right', TW_FIX32),
                ('Bottom', TW_FIX32)]


class TW_STATUS(ct.Structure):
    _pack_ = 2
    _fields_ = [('ConditionCode', ct.c_uint16), # Any TWCC_ constant
                ('Data', ct.c_uint16)]


class TW_IMAGELAYOUT(ct.Structure):
    _pack_ = 2
    _fields_ = [('Frame', TW_FRAME), # Any TWCC_ constant
                ('DocumentNumber', ct.c_uint32),
                ('PageNumber', ct.c_uint32),
                ('FrameNumber', ct.c_uint32)]


class TW_USERINTERFACE(ct.Structure):
    _pack_ = 2
    _fields_ = [('ShowUI', ct.c_uint16),
                ('ModalUI', ct.c_uint16),
                ('hParent', ct.c_void_p)]


class MSG(ct.Structure):
    _pack_ = 8
    _fields_ = [('hwnd', ct.c_void_p),
                ('message', ct.c_uint),
                ('wParam', ct.c_void_p),
                ('lParam', ct.c_void_p),
                ('time', ct.c_uint32),
                ('pt_x', ct.c_long),
                ('pt_y', ct.c_long)]


class TW_EVENT(ct.Structure):
    _pack_ = 2
    _fields_ = [('pEvent', ct.c_void_p),
                ('TWMessage', ct.c_uint16)]


class TW_VERSION(ct.Structure):
    _pack_ = 2
    _fields_ = [('MajorNum', ct.c_uint16),
                ('MinorNum', ct.c_uint16),
                ('Language', ct.c_uint16),
                ('Country', ct.c_uint16),
                ('Info', ct.c_char * 34)]


class TW_IDENTITY(ct.Structure):
    _pack_ = 2
    _fields_ = [('Id', ct.c_uint32),
                ('Version', TW_VERSION),
                ('ProtocolMajor', ct.c_uint16),
                ('ProtocolMinor', ct.c_uint16),
                ('SupportedGroups', ct.c_uint32),
                ('Manufacturer', ct.c_char * 34),
                ('ProductFamily', ct.c_char * 34),
                ('ProductName', ct.c_char * 34)]


class TW_IMAGEINFO(ct.Structure):
    _pack_ = 2
    _fields_ = [('XResolution', TW_FIX32),
                ('YResolution', TW_FIX32),
                ('ImageWidth', ct.c_int32),
                ('ImageLength', ct.c_int32),
                ('SamplesPerPixel', ct.c_int16),
                ('BitsPerSample', ct.c_int16 * 8),
                ('BitsPerPixel', ct.c_int16),
                ('Planar', ct.c_uint16),
                ('PixelType', ct.c_int16),
                ('Compression', ct.c_uint16)]


class TW_PENDINGXFERS(ct.Structure):
    _pack_ = 2
    _fields_ = [('Count', ct.c_uint16),
                ('EOJ', ct.c_uint32)]


class TW_RANGE(ct.Structure):
    _pack_ = 2
    _fields_ = [('ItemType', ct.c_uint16),
                ('MinValue', ct.c_uint32),
                ('MaxValue', ct.c_uint32),
                ('StepSize', ct.c_uint32),
                ('DefaultValue', ct.c_uint32),
                ('CurrentValue', ct.c_uint32)]


class TW_ENUMERATION(ct.Structure):
    _pack_ = 2
    _fields_ = [('ItemType', ct.c_uint16),
                ('NumItems', ct.c_uint32),
                ('CurrentIndex', ct.c_uint32),
                ('DefaultIndex', ct.c_uint32)]


class TW_ARRAY(ct.Structure):
    _pack_ = 2
    _fields_ = [('ItemType', ct.c_uint16),
                ('NumItems', ct.c_uint32)]


class TW_SETUPFILEXFER(ct.Structure):
    _pack_ = 2
    _fields_ = [('FileName', ct.c_char * 256),
                ('Format', ct.c_uint16),
                ('VRefNum', ct.c_int16)]


if utils.is_windows():
    FUNCTYPE = ct.WINFUNCTYPE
else:
    FUNCTYPE = ct.CFUNCTYPE


class TW_ENTRYPOINT(ct.Structure):
    _pack_ = 2
    _fields_ = [('Size', ct.c_uint32),
                ('DSM_Entry', FUNCTYPE(ct.c_int, ct.POINTER(ct.c_int), ct.POINTER(ct.c_int))),
                ('DSM_MemAllocate', FUNCTYPE(ct.c_void_p, ct.c_uint32)),
                ('DSM_MemFree', FUNCTYPE(None, ct.c_void_p)),
                ('DSM_MemLock', FUNCTYPE(ct.c_void_p, ct.c_void_p)),
                ('DSM_MemUnlock', FUNCTYPE(None, ct.c_void_p))]


def float2fix(x):
    if x <= -2**15 - 1 and 2**15 + 1 <= x:
        raise Exception('Float value is out of range')
    x = int(x * 2**16 + 0.5)
    whole = x >> 16
    frac = x & 0xffff
    return TW_FIX32(whole, frac)


def fix2float(x):
    return x.Whole + float(x.Frac) / 2**16


def frame2tuple(frame):
    return (fix2float(frame.Left),
            fix2float(frame.Top),
            fix2float(frame.Right),
            fix2float(frame.Bottom))


def tuple2frame(tup):
    return TW_FRAME(float2fix(tup[0]),
                    float2fix(tup[1]),
                    float2fix(tup[2]),
                    float2fix(tup[3]))

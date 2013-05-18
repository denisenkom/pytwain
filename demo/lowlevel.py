
# demonstration of low-level access to TWAIN API
# prints out the list of available data sources

import twain, struct, string

## The identity structure is as follows (see twain.h)
##
## typedef struct {
##   TW_UINT16  MajorNum;  /* Major revision number of the software. */
##   TW_UINT16  MinorNum;  /* Incremental revision number of the software. */
##   TW_UINT16  Language;  /* e.g. TWLG_SWISSFRENCH */
##   TW_UINT16  Country;   /* e.g. TWCY_SWITZERLAND */
##   TW_STR32   Info;      /* e.g. "1.0b3 Beta release" */
##} TW_VERSION, FAR * pTW_VERSION;
##
##	2 + 2 + 2 + 2 + 34 bytes = 42
##
## typedef struct {
##    TW_UINT32  Id;              /* Unique number.  In Windows, application hWnd      */
##    TW_VERSION Version;         /* Identifies the piece of code              */
##    TW_UINT16  ProtocolMajor;   /* Application and DS must set to TWON_PROTOCOLMAJOR */
##    TW_UINT16  ProtocolMinor;   /* Application and DS must set to TWON_PROTOCOLMINOR */
##    TW_UINT32  SupportedGroups; /* Bit field OR combination of DG_ constants */
##    TW_STR32   Manufacturer;    /* Manufacturer name, e.g. "Hewlett-Packard" */
##    TW_STR32   ProductFamily;   /* Product family name, e.g. "ScanJet"       */
##    TW_STR32   ProductName;     /* Product name, e.g. "ScanJet Plus"         */
## } TW_IDENTITY, FAR * pTW_IDENTITY;
##
## 4 + 42 + 2 + 2 + 4 + 34 + 34 + 34 bytes = 156
##
##	Note: TW_STR32 = char x[34];

##	This is the struct module string which represents the TW_IDENTITY
##	structure. Note that the alignment is non-default. The long (SupportedGroups)
##	is aligned to a two byte boundary, and so I have to extract it using
##	a '4s', rather than a 'L'.
fmtString = "L42sHH4s34s34s34s"
slen= struct.calcsize(fmtString)

def UnpackIdentity(id):
	return struct.unpack(fmtString, id)

def StripNull(s):
	offset = string.find(s, '\0')
	if s != -1: s= s[:offset]
	return s

sm = twain.SourceManager(0L) 

identity = struct.pack("%ds" % slen, "")

rv = sm.DSM_Entry(twain.DG_CONTROL, twain.DAT_IDENTITY, twain.MSG_GETFIRST, identity)
while 1:
	if rv != twain.TWRC_SUCCESS: break
	#ProductName = UnpackIdentity(identity)[5]
	ProductName = identity[122:]
	ProductName = StripNull(ProductName)
	print ProductName
	rv = sm.DSM_Entry(twain.DG_CONTROL, twain.DAT_IDENTITY, 
		twain.MSG_GETNEXT, identity)

del sm

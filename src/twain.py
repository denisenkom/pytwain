import ctypes
from ctypes import *
import weakref
import sys
import platform
import warnings

TWON_PROTOCOLMAJOR = 2
TWON_PROTOCOLMINOR = 1

DF_DSM2 = 0x10000000
DF_APP2 = 0x20000000
DF_DS2 = 0x40000000


ACAP_AUDIOFILEFORMAT = 4609
ACAP_XFERMECH = 4610
CAP_ALARMS = 4120
CAP_ALARMVOLUME = 4121
CAP_AUTHOR = 4096
CAP_AUTOFEED = 4103
CAP_AUTOMATICCAPTURE = 4122
CAP_AUTOMATICSENSEMEDIUM = 4155
CAP_AUTOSCAN = 4112
CAP_BATTERYMINUTES = 4146
CAP_BATTERYPERCENTAGE = 4147
CAP_CAMERAENABLED = 4150
CAP_CAMERAORDER = 4151
CAP_CAMERAPREVIEWUI = 4129
CAP_CAMERASIDE = 4148
CAP_CAPTION = 4097
CAP_CLEARBUFFERS = 4125
CAP_CLEARPAGE = 4104
CAP_CUSTOMBASE = 32768
CAP_CUSTOMDSDATA = 4117
CAP_CUSTOMINTERFACEGUID = 4156
CAP_DEVICEEVENT = 4130
CAP_DEVICEONLINE = 4111
CAP_DEVICETIMEDATE = 4127
CAP_DUPLEX = 4114
CAP_DUPLEXENABLED = 4115
CAP_ENABLEDSUIONLY = 4116
CAP_ENDORSER = 4118
CAP_EXTENDEDCAPS = 4102
CAP_FEEDERALIGNMENT = 4141
CAP_FEEDERENABLED = 4098
CAP_FEEDERLOADED = 4099
CAP_FEEDERORDER = 4142
CAP_FEEDERPOCKET = 4154
CAP_FEEDERPREP = 4153
CAP_FEEDPAGE = 4105
CAP_INDICATORS = 4107
CAP_JOBCONTROL = 4119
CAP_LANGUAGE = 4140
CAP_MAXBATCHBUFFERS = 4126
CAP_MICRENABLED = 4152
CAP_PAGEMULTIPLEACQUIRE = 4131
CAP_PAPERBINDING = 4143
CAP_PAPERDETECTABLE = 4109
CAP_PASSTHRU = 4145
CAP_POWERDOWNTIME = 4148
CAP_POWERSUPPLY = 4128
CAP_PRINTER = 4134
CAP_PRINTERENABLED = 4135
CAP_PRINTERINDEX = 4136
CAP_PRINTERMODE = 4137
CAP_PRINTERSTRING = 4138
CAP_PRINTERSUFFIX = 4139
CAP_REACQUIREALLOWED = 4144
CAP_REWINDPAGE = 4106
CAP_SEGMENTED = 4149
CAP_SERIALNUMBER = 4132
CAP_SUPPORTEDCAPS = 4101
CAP_SUPPORTEDCAPSEXT = 4108
CAP_THUMBNAILSENABLED = 4113
CAP_TIMEBEFOREFIRSTCAPTURE = 4123
CAP_TIMEBETWEENCAPTURES = 4124
CAP_TIMEDATE = 4100
CAP_UICONTROLLABLE = 4110
CAP_XFERCOUNT = 1
DAT_AUDIOFILEXFER = 513
DAT_AUDIOINFO = 514
DAT_AUDIONATIVEXFER = 515
DAT_CAPABILITY = 1
DAT_CIECOLOR = 262
DAT_CUSTOMBASE = 32768
DAT_CUSTOMDSDATA = 12
DAT_DEVICEEVENT = 13
DAT_ENTRYPOINT = 0x0403
DAT_EVENT = 2
DAT_EXTIMAGEINFO = 267
DAT_FILESYSTEM = 14
DAT_GRAYRESPONSE = 263
DAT_IDENTITY = 3
DAT_IMAGEFILEXFER = 261
DAT_IMAGEINFO = 257
DAT_IMAGELAYOUT = 258
DAT_IMAGEMEMXFER = 259
DAT_IMAGENATIVEXFER = 260
DAT_JPEGCOMPRESSION = 265
DAT_NULL = 0
DAT_PALETTE8 = 266
DAT_PARENT = 4
DAT_PASSTHRU = 15
DAT_PENDINGXFERS = 5
DAT_RGBRESPONSE = 264
DAT_SETUPFILEXFER = 7
DAT_SETUPMEMXFER = 6
DAT_STATUS = 8
DAT_TWUNKIDENTITY = 11
DAT_USERINTERFACE = 9
DAT_XFERGROUP = 10
DG_AUDIO = 4
DG_CONTROL = 1
DG_IMAGE = 2
ICAP_AUTOBRIGHT = 4352
ICAP_AUTODISCARDBLANKPAGES = 4404
ICAP_AUTOMATICBORDERDETECTION = 4432
ICAP_AUTOMATICCOLORENABLED = 4441
ICAP_AUTOMATICCOLORNONCOLORPIXELTYPE = 4442
ICAP_AUTOMATICCROPUSESFRAME = 4439
ICAP_AUTOMATICDESKEW = 4433
ICAP_AUTOMATICLENGTHDETECTION = 4440
ICAP_AUTOMATICROTATE = 4434
ICAP_AUTOSIZE = 4438
ICAP_BARCODEDETECTIONENABLED = 4407
ICAP_BARCODEMAXRETRIES = 4412
ICAP_BARCODEMAXSEARCHPRIORITIES = 4409
ICAP_BARCODESEARCHMODE = 4411
ICAP_BARCODESEARCHPRIORITIES = 4410
ICAP_BARCODETIMEOUT = 4413
ICAP_BITDEPTH = 4395
ICAP_BITDEPTHREDUCTION = 4396
ICAP_BITORDER = 4380
ICAP_BITORDERCODES = 4390
ICAP_BRIGHTNESS = 4353
ICAP_CCITTKFACTOR = 4381
ICAP_COLORMANAGEMENTENABLED = 4443
ICAP_COMPRESSION = 256
ICAP_CONTRAST = 4355
ICAP_CUSTHALFTONE = 4356
ICAP_EXPOSURETIME = 4357
ICAP_EXTIMAGEINFO = 4399
ICAP_FEEDERTYPE = 4436
ICAP_FILTER = 4358
ICAP_FLASHUSED = 4359
ICAP_FLASHUSED2 = 4422
ICAP_FLIPROTATION = 4406
ICAP_FRAMES = 4372
ICAP_GAMMA = 4360
ICAP_HALFTONES = 4361
ICAP_HIGHLIGHT = 4362
ICAP_ICCPROFILE = 4437
ICAP_IMAGEDATASET = 4398
ICAP_IMAGEFILEFORMAT = 4364
ICAP_IMAGEFILTER = 4423
ICAP_IMAGEMERGE = 4444
ICAP_IMAGEMERGEHEIGHTTHRESHOLD = 4445
ICAP_JPEGPIXELTYPE = 4392
ICAP_JPEGQUALITY = 4435
ICAP_LAMPSTATE = 4365
ICAP_LIGHTPATH = 4382
ICAP_LIGHTSOURCE = 4366
ICAP_MAXFRAMES = 4378
ICAP_MINIMUMHEIGHT = 4400
ICAP_MINIMUMWIDTH = 4401
ICAP_NOISEFILTER = 4424
ICAP_ORIENTATION = 4368
ICAP_OVERSCAN = 4425
ICAP_PATCHCODEDETECTIONENABLED = 4415
ICAP_PATCHCODEMAXRETRIES = 4420
ICAP_PATCHCODEMAXSEARCHPRIORITIES = 4417
ICAP_PATCHCODESEARCHMODE = 4419
ICAP_PATCHCODESEARCHPRIORITIES = 4418
ICAP_PATCHCODETIMEOUT = 4421
ICAP_PHYSICALHEIGHT = 4370
ICAP_PHYSICALWIDTH = 4369
ICAP_PIXELFLAVOR = 4383
ICAP_PIXELFLAVORCODES = 4391
ICAP_PIXELTYPE = 257
ICAP_PLANARCHUNKY = 4384
ICAP_ROTATION = 4385
ICAP_SHADOW = 4371
ICAP_SUPPORTEDBARCODETYPES = 4408
ICAP_SUPPORTEDEXTIMAGEINFO = 4446
ICAP_SUPPORTEDPATCHCODETYPES = 4416
ICAP_SUPPORTEDSIZES = 4386
ICAP_THRESHOLD = 4387
ICAP_TILES = 4379
ICAP_TIMEFILL = 4394
ICAP_UNDEFINEDIMAGESIZE = 4397
ICAP_UNITS = 258
ICAP_XFERMECH = 259
ICAP_XNATIVERESOLUTION = 4374
ICAP_XRESOLUTION = 4376
ICAP_XSCALING = 4388
ICAP_YNATIVERESOLUTION = 4375
ICAP_YRESOLUTION = 4377
ICAP_YSCALING = 4389
ICAP_ZOOMFACTOR = 4414
MSG_CHANGEDIRECTORY = 2049
MSG_CHECKSTATUS = 513
MSG_CLOSEDS = 1026
MSG_CLOSEDSM = 770
MSG_CLOSEDSOK = 259
MSG_CLOSEDSREQ = 258
MSG_CREATEDIRECTORY = 2050
MSG_CUSTOMBASE = 32768
MSG_DELETE = 2051
MSG_DEVICEEVENT = 260
MSG_DISABLEDS = 1281
MSG_ENABLEDS = 1282
MSG_ENABLEDSUIONLY = 1283
MSG_ENDXFER = 1793
MSG_FORMATMEDIA = 2052
MSG_GET = 1
MSG_GETCLOSE = 2053
MSG_GETCURRENT = 2
MSG_GETDEFAULT = 3
MSG_GETFIRST = 4
MSG_GETFIRSTFILE = 2054
MSG_GETINFO = 2055
MSG_GETNEXT = 5
MSG_GETNEXTFILE = 2056
MSG_NULL = 0
MSG_OPENDS = 1025
MSG_OPENDSM = 769
MSG_PASSTHRU = 2305
MSG_PROCESSEVENT = 1537
MSG_QUERYSUPPORT = 8
MSG_RENAME = 2057
MSG_RESET = 7
MSG_SET = 6
MSG_USERSELECT = 1027
MSG_XFERREADY = 257
TWAF_AIFF = 1
TWAF_AU = 3
TWAF_SND = 4
TWAF_WAV = 0
TWAL_ALARM = 0
TWAL_BARCODE = 3
TWAL_DOUBLEFEED = 4
TWAL_FEEDERERROR = 1
TWAL_FEEDERWARNING = 2
TWAL_JAM = 5
TWAL_PATCHCODE = 6
TWAL_POWER = 7
TWAL_SKEW = 8
TWAS_AUTO = 1
TWAS_CURRENT = 2
TWAS_NONE = 0
TWBCOR_ROT0 = 0
TWBCOR_ROT180 = 2
TWBCOR_ROT270 = 3
TWBCOR_ROT90 = 1
TWBCOR_ROTX = 4
TWBD_HORZ = 0
TWBD_HORZVERT = 2
TWBD_VERT = 1
TWBD_VERTHORZ = 3
TWBO_LSBFIRST = 0
TWBO_MSBFIRST = 1
TWBP_AUTO = -1
TWBP_DISABLE = -2
TWBR_CUSTHALFTONE = 2
TWBR_DIFFUSION = 3
TWBR_HALFTONE = 1
TWBR_THRESHOLD = 0
TWBT_2OF5DATALOGIC = 15
TWBT_2OF5IATA = 16
TWBT_2OF5INDUSTRIAL = 13
TWBT_2OF5INTERLEAVED = 1
TWBT_2OF5MATRIX = 14
TWBT_2OF5NONINTERLEAVED = 2
TWBT_3OF9 = 0
TWBT_3OF9FULLASCII = 17
TWBT_CODABAR = 6
TWBT_CODABARWITHSTARTSTOP = 18
TWBT_CODE128 = 4
TWBT_CODE93 = 3
TWBT_EAN13 = 10
TWBT_EAN8 = 9
TWBT_MAXICODE = 19
TWBT_PDF417 = 12
TWBT_POSTNET = 11
TWBT_UCC128 = 5
TWBT_UPCA = 7
TWBT_UPCE = 8
TWCB_AUTO = 0
TWCB_CLEAR = 1
TWCB_NOCLEAR = 2
TWCC_BADCAP = 6
TWCC_BADDEST = 12
TWCC_BADPROTOCOL = 9
TWCC_BADVALUE = 10
TWCC_BUMMER = 1
TWCC_CAPBADOPERATION = 14
TWCC_CAPSEQERROR = 15
TWCC_CAPUNSUPPORTED = 13
TWCC_CHECKDEVICEONLINE = 23
TWCC_CUSTOMBASE = 32768
TWCC_DAMAGEDCORNER = 25
TWCC_DENIED = 16
TWCC_DOCTOODARK = 28
TWCC_DOCTOOLIGHT = 27
TWCC_FILEEXISTS = 17
TWCC_FILENOTFOUND = 18
TWCC_FILEWRITEERROR = 22
TWCC_FOCUSERROR = 26
TWCC_LOWMEMORY = 2
TWCC_MAXCONNECTIONS = 4
TWCC_NODS = 3
TWCC_NOMEDIA = 29
TWCC_NOTEMPTY = 19
TWCC_OPERATIONERROR = 5
TWCC_PAPERDOUBLEFEED = 21
TWCC_PAPERJAM = 20
TWCC_SEQERROR = 11
TWCC_SUCCESS = 0
TWCP_BITFIELDS = 12
TWCP_GROUP31D = 2
TWCP_GROUP31DEOL = 3
TWCP_GROUP32D = 4
TWCP_GROUP4 = 5
TWCP_JBIG = 8
TWCP_JPEG = 6
TWCP_LZW = 7
TWCP_NONE = 0
TWCP_PACKBITS = 1
TWCP_PNG = 9
TWCP_RLE4 = 10
TWCP_RLE8 = 11
TWCS_BOTH = 0
TWCS_BOTTOM = 2
TWCS_TOP = 1
TWCY_AFGHANISTAN = 1001
TWCY_ALBANIA = 355
TWCY_ALGERIA = 213
TWCY_AMERICANSAMOA = 684
TWCY_ANDORRA = 27
TWCY_ANGOLA = 1002
TWCY_ANGUILLA = 8090
TWCY_ANTIGUA = 8091
TWCY_ARGENTINA = 54
TWCY_ARMENIA = 374
TWCY_ARUBA = 297
TWCY_ASCENSIONI = 247
TWCY_AUSTRALIA = 61
TWCY_AUSTRIA = 43
TWCY_AZERBAIJAN = 994
TWCY_BAHAMAS = 8092
TWCY_BAHRAIN = 973
TWCY_BANGLADESH = 880
TWCY_BARBADOS = 8093
TWCY_BELARUS = 375
TWCY_BELGIUM = 32
TWCY_BELIZE = 501
TWCY_BENIN = 229
TWCY_BERMUDA = 8094
TWCY_BHUTAN = 1003
TWCY_BOLIVIA = 591
TWCY_BOSNIAHERZGO = 387
TWCY_BOTSWANA = 267
TWCY_BRAZIL = 55
TWCY_BRITAIN = 6
TWCY_BRITVIRGINIS = 8095
TWCY_BRUNEI = 673
TWCY_BULGARIA = 359
TWCY_BURKINAFASO = 1004
TWCY_BURMA = 1005
TWCY_BURUNDI = 1006
TWCY_CAMAROON = 237
TWCY_CAMBODIA = 855
TWCY_CANADA = 2
TWCY_CAPEVERDEIS = 238
TWCY_CAYMANIS = 8096
TWCY_CENTRALAFREP = 1007
TWCY_CHAD = 1008
TWCY_CHILE = 56
TWCY_CHINA = 86
TWCY_CHRISTMASIS = 1009
TWCY_COCOSIS = 1009
TWCY_COLOMBIA = 57
TWCY_COMOROS = 1010
TWCY_CONGO = 1011
TWCY_COOKIS = 1012
TWCY_COSTARICA = 506
TWCY_CROATIA = 385
TWCY_CUBA = 5
TWCY_CYPRUS = 357
TWCY_CZECHOSLOVAKIA = 42
TWCY_CZECHREPUBLIC = 420
TWCY_DENMARK = 45
TWCY_DIEGOGARCIA = 246
TWCY_DJIBOUTI = 1013
TWCY_DOMINCANREP = 8098
TWCY_DOMINICA = 8097
TWCY_EASTERIS = 1014
TWCY_ECUADOR = 593
TWCY_EGYPT = 20
TWCY_ELSALVADOR = 503
TWCY_EQGUINEA = 1015
TWCY_ERITREA = 291
TWCY_ESTONIA = 372
TWCY_ETHIOPIA = 251
TWCY_FAEROEIS = 298
TWCY_FALKLANDIS = 1016
TWCY_FIJIISLANDS = 679
TWCY_FINLAND = 358
TWCY_FRANCE = 33
TWCY_FRANTILLES = 596
TWCY_FRGUIANA = 594
TWCY_FRPOLYNEISA = 689
TWCY_FUTANAIS = 1043
TWCY_GABON = 241
TWCY_GAMBIA = 220
TWCY_GEORGIA = 995
TWCY_GERMANY = 49
TWCY_GHANA = 233
TWCY_GIBRALTER = 350
TWCY_GREECE = 30
TWCY_GREENLAND = 299
TWCY_GRENADA = 8099
TWCY_GRENEDINES = 8015
TWCY_GUADELOUPE = 590
TWCY_GUAM = 671
TWCY_GUANTANAMOBAY = 5399
TWCY_GUATEMALA = 502
TWCY_GUINEA = 224
TWCY_GUINEABISSAU = 1017
TWCY_GUYANA = 592
TWCY_HAITI = 509
TWCY_HONDURAS = 504
TWCY_HONGKONG = 852
TWCY_HUNGARY = 36
TWCY_ICELAND = 354
TWCY_INDIA = 91
TWCY_INDONESIA = 62
TWCY_IRAN = 98
TWCY_IRAQ = 964
TWCY_IRELAND = 353
TWCY_ISRAEL = 972
TWCY_ITALY = 39
TWCY_IVORYCOAST = 225
TWCY_JAMAICA = 8010
TWCY_JAPAN = 81
TWCY_JORDAN = 962
TWCY_KENYA = 254
TWCY_KIRIBATI = 1018
TWCY_KOREA = 82
TWCY_KUWAIT = 965
TWCY_LAOS = 1019
TWCY_LATVIA = 371
TWCY_LEBANON = 1020
TWCY_LESOTHO = 266
TWCY_LIBERIA = 231
TWCY_LIBYA = 218
TWCY_LIECHTENSTEIN = 41
TWCY_LITHUANIA = 370
TWCY_LUXENBOURG = 352
TWCY_MACAO = 853
TWCY_MACEDONIA = 389
TWCY_MADAGASCAR = 1021
TWCY_MALAWI = 265
TWCY_MALAYSIA = 60
TWCY_MALDIVES = 960
TWCY_MALI = 1022
TWCY_MALTA = 356
TWCY_MARSHALLIS = 692
TWCY_MAURITANIA = 1023
TWCY_MAURITIUS = 230
TWCY_MAYOTTEIS = 269
TWCY_MEXICO = 3
TWCY_MICRONESIA = 691
TWCY_MIQUELON = 508
TWCY_MOLDOVA = 373
TWCY_MONACO = 33
TWCY_MONGOLIA = 1024
TWCY_MONTSERRAT = 8011
TWCY_MOROCCO = 212
TWCY_MOZAMBIQUE = 1025
TWCY_MYANMAR = 95
TWCY_NAMIBIA = 264
TWCY_NAURU = 1026
TWCY_NEPAL = 977
TWCY_NETHANTILLES = 599
TWCY_NETHERLANDS = 31
TWCY_NEVIS = 8012
TWCY_NEWCALEDONIA = 687
TWCY_NEWZEALAND = 64
TWCY_NICARAGUA = 505
TWCY_NIGER = 227
TWCY_NIGERIA = 234
TWCY_NIUE = 1027
TWCY_NORFOLKI = 1028
TWCY_NORTHKOREA = 850
TWCY_NORWAY = 47
TWCY_OMAN = 968
TWCY_PAKISTAN = 92
TWCY_PALAU = 1029
TWCY_PANAMA = 507
TWCY_PARAGUAY = 595
TWCY_PERU = 51
TWCY_PHILLIPPINES = 63
TWCY_PITCAIRNIS = 1030
TWCY_PNEWGUINEA = 675
TWCY_POLAND = 48
TWCY_PORTUGAL = 351
TWCY_PUERTORICO = 787
TWCY_QATAR = 974
TWCY_REUNIONI = 1031
TWCY_ROMANIA = 40
TWCY_RUSSIA = 7
TWCY_RWANDA = 250
TWCY_SAIPAN = 670
TWCY_SANMARINO = 39
TWCY_SAOTOME = 1033
TWCY_SAUDIARABIA = 966
TWCY_SENEGAL = 221
TWCY_SERBIA = 381
TWCY_SEYCHELLESIS = 1034
TWCY_SIERRALEONE = 1035
TWCY_SINGAPORE = 65
TWCY_SLOVAKIA = 421
TWCY_SLOVENIA = 386
TWCY_SOLOMONIS = 1036
TWCY_SOMALI = 1037
TWCY_SOUTHAFRICA = 27
TWCY_SOUTHKOREA = 82
TWCY_SPAIN = 34
TWCY_SRILANKA = 94
TWCY_STHELENA = 1032
TWCY_STKITTS = 8013
TWCY_STLUCIA = 8014
TWCY_STPIERRE = 508
TWCY_STVINCENT = 8015
TWCY_SUDAN = 1038
TWCY_SURINAME = 597
TWCY_SWAZILAND = 268
TWCY_SWEDEN = 46
TWCY_SWITZERLAND = 41
TWCY_SYRIA = 1039
TWCY_TAIWAN = 886
TWCY_TANZANIA = 255
TWCY_THAILAND = 66
TWCY_TOBAGO = 8016
TWCY_TOGO = 228
TWCY_TONGAIS = 676
TWCY_TRINIDAD = 8016
TWCY_TUNISIA = 216
TWCY_TURKEY = 90
TWCY_TURKSCAICOS = 8017
TWCY_TUVALU = 1040
TWCY_UAEMIRATES = 971
TWCY_UGANDA = 256
TWCY_UKRAINE = 380
TWCY_UNITEDKINGDOM = 44
TWCY_URUGUAY = 598
TWCY_USA = 1
TWCY_USSR = 7
TWCY_USVIRGINIS = 340
TWCY_VANUATU = 1041
TWCY_VATICANCITY = 39
TWCY_VENEZUELA = 58
TWCY_VIETNAM = 84
TWCY_WAKE = 1042
TWCY_WALLISIS = 1043
TWCY_WESTERNSAHARA = 1044
TWCY_WESTERNSAMOA = 1045
TWCY_YEMEN = 1046
TWCY_YUGOSLAVIA = 38
TWCY_ZAIRE = 243
TWCY_ZAMBIA = 260
TWCY_ZIMBABWE = 263
TWDE_CHECKAUTOMATICCAPTURE = 0
TWDE_CHECKBATTERY = 1
TWDE_CHECKDEVICEONLINE = 2
TWDE_CHECKFLASH = 3
TWDE_CHECKPOWERSUPPLY = 4
TWDE_CHECKRESOLUTION = 5
TWDE_CUSTOMEVENTS = 32768
TWDE_DEVICEADDED = 6
TWDE_DEVICEOFFLINE = 7
TWDE_DEVICEREADY = 8
TWDE_DEVICEREMOVED = 9
TWDE_IMAGECAPTURED = 10
TWDE_IMAGEDELETED = 11
TWDE_LAMPFAILURE = 14
TWDE_PAPERDOUBLEFEED = 12
TWDE_PAPERJAM = 13
TWDE_POWERSAVE = 15
TWDE_POWERSAVENOTIFY = 16
TWDR_GET = 1
TWDR_SET = 2
TWDSK_DISABLED = 3
TWDSK_FAIL = 2
TWDSK_REPORTONLY = 1
TWDSK_SUCCESS = 0
TWDX_1PASSDUPLEX = 1
TWDX_2PASSDUPLEX = 2
TWDX_NONE = 0
TWEI_BARCODECONFIDENCE = 4634
TWEI_BARCODECOUNT = 4633
TWEI_BARCODEROTATION = 4635
TWEI_BARCODETEXT = 4610
TWEI_BARCODETEXTLENGTH = 4636
TWEI_BARCODETYPE = 4611
TWEI_BARCODEX = 4608
TWEI_BARCODEY = 4609
TWEI_BLACKSPECKLESREMOVED = 4647
TWEI_BOOKNAME = 4664
TWEI_CAMERA = 4668
TWEI_CHAPTERNUMBER = 4665
TWEI_DESHADEBLACKCOUNTNEW = 4639
TWEI_DESHADEBLACKCOUNTOLD = 4638
TWEI_DESHADEBLACKRLMAX = 4641
TWEI_DESHADEBLACKRLMIN = 4640
TWEI_DESHADECOUNT = 4637
TWEI_DESHADEHEIGHT = 4614
TWEI_DESHADELEFT = 4613
TWEI_DESHADESIZE = 4616
TWEI_DESHADETOP = 4612
TWEI_DESHADEWHITECOUNTNEW = 4643
TWEI_DESHADEWHITECOUNTOLD = 4642
TWEI_DESHADEWHITERLAVE = 4645
TWEI_DESHADEWHITERLMAX = 4646
TWEI_DESHADEWHITERLMIN = 4644
TWEI_DESHADEWIDTH = 4615
TWEI_DESKEWSTATUS = 4651
TWEI_DOCUMENTNUMBER = 4666
TWEI_ENDORSEDTEXT = 4627
TWEI_FILESYSTEMSOURCE = 4678
TWEI_FORMCONFIDENCE = 4628
TWEI_FORMHORZDOCOFFSET = 4631
TWEI_FORMTEMPLATEMATCH = 4629
TWEI_FORMTEMPLATEPAGEMATCH = 4630
TWEI_FORMVERTDOCOFFSET = 4632
TWEI_FRAME = 4670
TWEI_FRAMENUMBER = 4669
TWEI_HORZLINECOUNT = 4649
TWEI_HORZLINELENGTH = 4620
TWEI_HORZLINETHICKNESS = 4621
TWEI_HORZLINEXCOORD = 4618
TWEI_HORZLINEYCOORD = 4619
TWEI_ICCPROFILE = 4672
TWEI_IMAGEMERGED = 4679
TWEI_LASTSEGMENT = 4673
TWEI_MAGDATA = 4675
TWEI_MAGDATALENGTH = 4680
TWEI_MAGTYPE = 4676
TWEI_PAGENUMBER = 4667
TWEI_PAGESIDE = 4677
TWEI_PATCHCODE = 4626
TWEI_PIXELFLAVOR = 4671
TWEI_SEGMENTNUMBER = 4674
TWEI_SKEWCONFIDENCE = 4654
TWEI_SKEWFINALANGLE = 4653
TWEI_SKEWORIGINALANGLE = 4652
TWEI_SKEWWINDOWX1 = 4655
TWEI_SKEWWINDOWX2 = 4657
TWEI_SKEWWINDOWX3 = 4659
TWEI_SKEWWINDOWX4 = 4661
TWEI_SKEWWINDOWY1 = 4656
TWEI_SKEWWINDOWY2 = 4658
TWEI_SKEWWINDOWY3 = 4660
TWEI_SKEWWINDOWY4 = 4662
TWEI_SPECKLESREMOVED = 4617
TWEI_VERTLINECOUNT = 4650
TWEI_VERTLINELENGTH = 4624
TWEI_VERTLINETHICKNESS = 4625
TWEI_VERTLINEXCOORD = 4622
TWEI_VERTLINEYCOORD = 4623
TWEI_WHITESPECKLESREMOVED = 4648
TWEJ_MIDSEPARATOR = 1
TWEJ_NONE = 0
TWEJ_PATCH1 = 2
TWEJ_PATCH2 = 3
TWEJ_PATCH3 = 4
TWEJ_PATCH4 = 5
TWEJ_PATCH6 = 6
TWEJ_PATCHT = 7
TWFA_CENTER = 2
TWFA_LEFT = 1
TWFA_NONE = 0
TWFA_RIGHT = 3
TWFE_GENERAL = 0
TWFE_PHOTO = 1
TWFF_BMP = 2
TWFF_DEJAVU = 14
TWFF_EXIF = 9
TWFF_FPX = 5
TWFF_JFIF = 4
TWFF_JP2 = 11
TWFF_JPX = 13
TWFF_PDF = 10
TWFF_PDFA = 15
TWFF_PDFA2 = 16
TWFF_PICT = 1
TWFF_PNG = 7
TWFF_SPIFF = 8
TWFF_TIFF = 0
TWFF_TIFFMULTI = 6
TWFF_XBM = 3
TWFL_AUTO = 3
TWFL_NONE = 0
TWFL_OFF = 1
TWFL_ON = 2
TWFL_REDEYE = 4
TWFO_FIRSTPAGEFIRST = 0
TWFO_LASTPAGEFIRST = 1
TWFR_BOOK = 0
TWFR_FANFOLD = 1
TWFS_FILESYSTEM = 0
TWFS_RECURSIVEDELETE = 1
TWFT_BLACK = 8
TWFT_BLUE = 2
TWFT_CYAN = 5
TWFT_GREEN = 1
TWFT_MAGENTA = 6
TWFT_NONE = 3
TWFT_RED = 0
TWFT_WHITE = 4
TWFT_YELLOW = 7
TWFY_CAMERA = 0
TWFY_CAMERABOTTOM = 2
TWFY_CAMERAPREVIEW = 3
TWFY_CAMERATOP = 1
TWFY_DIRECTORY = 6
TWFY_DOMAIN = 4
TWFY_HOST = 5
TWFY_IMAGE = 7
TWFY_UNKNOWN = 8
TWIF_AUTO = 1
TWIF_BANDPASS = 3
TWIF_FINELINE = 4
TWIF_HIGHPASS = 4
TWIF_LOWPASS = 2
TWIF_NONE = 0
TWIF_TEXT = 3
TWJC_JSIC = 1
TWJC_JSIS = 2
TWJC_JSXC = 3
TWJC_JSXS = 4
TWJC_NONE = 0
TWLG_AFRIKAANS = 14
TWLG_ALBANIA = 15
TWLG_ARABIC = 16
TWLG_ARABIC_ALGERIA = 17
TWLG_ARABIC_BAHRAIN = 18
TWLG_ARABIC_EGYPT = 19
TWLG_ARABIC_IRAQ = 20
TWLG_ARABIC_JORDAN = 21
TWLG_ARABIC_KUWAIT = 22
TWLG_ARABIC_LEBANON = 23
TWLG_ARABIC_LIBYA = 24
TWLG_ARABIC_MOROCCO = 25
TWLG_ARABIC_OMAN = 26
TWLG_ARABIC_QATAR = 27
TWLG_ARABIC_SAUDIARABIA = 28
TWLG_ARABIC_SYRIA = 29
TWLG_ARABIC_TUNISIA = 30
TWLG_ARABIC_UAE = 31
TWLG_ARABIC_YEMEN = 32
TWLG_ASSAMESE = 87
TWLG_BASQUE = 33
TWLG_BENGALI = 88
TWLG_BIHARI = 89
TWLG_BODO = 90
TWLG_BULGARIAN = 35
TWLG_BYELORUSSIAN = 34
TWLG_CATALAN = 36
TWLG_CHINESE = 37
TWLG_CHINESE_HONGKONG = 38
TWLG_CHINESE_PRC = 39
TWLG_CHINESE_SIMPLIFIED = 41
TWLG_CHINESE_SINGAPORE = 40
TWLG_CHINESE_TAIWAN = 42
TWLG_CHINESE_TRADITIONAL = 43
TWLG_CROATIA = 44
TWLG_CZECH = 45
TWLG_DAN = 0
TWLG_DANISH = 0
TWLG_DOGRI = 91
TWLG_DUT = 1
TWLG_DUTCH = 1
TWLG_DUTCH_BELGIAN = 46
TWLG_ENG = 2
TWLG_ENGLISH = 2
TWLG_ENGLISH_AUSTRALIAN = 47
TWLG_ENGLISH_CANADIAN = 48
TWLG_ENGLISH_IRELAND = 49
TWLG_ENGLISH_NEWZEALAND = 50
TWLG_ENGLISH_SOUTHAFRICA = 51
TWLG_ENGLISH_UK = 52
TWLG_ENGLISH_USA = 13
TWLG_ESTONIAN = 53
TWLG_FAEROESE = 54
TWLG_FARSI = 55
TWLG_FCF = 3
TWLG_FIN = 4
TWLG_FINNISH = 4
TWLG_FRENCH = 5
TWLG_FRENCH_BELGIAN = 56
TWLG_FRENCH_CANADIAN = 3
TWLG_FRENCH_LUXEMBOURG = 57
TWLG_FRENCH_SWISS = 58
TWLG_FRN = 5
TWLG_GER = 6
TWLG_GERMAN = 6
TWLG_GERMAN_AUSTRIAN = 59
TWLG_GERMAN_LIECHTENSTEIN = 61
TWLG_GERMAN_LUXEMBOURG = 60
TWLG_GERMAN_SWISS = 62
TWLG_GREEK = 63
TWLG_GUJARATI = 92
TWLG_HARYANVI = 93
TWLG_HEBREW = 64
TWLG_HINDI = 94
TWLG_HUNGARIAN = 65
TWLG_ICE = 7
TWLG_ICELANDIC = 7
TWLG_INDONESIAN = 66
TWLG_ITALIAN = 8
TWLG_ITALIAN_SWISS = 67
TWLG_ITN = 8
TWLG_JAPANESE = 68
TWLG_KANNADA = 95
TWLG_KASHMIRI = 96
TWLG_KOREAN = 69
TWLG_KOREAN_JOHAB = 70
TWLG_LATVIAN = 71
TWLG_LITHUANIAN = 72
TWLG_MALAYALAM = 97
TWLG_MARATHI = 98
TWLG_MARWARI = 99
TWLG_MEGHALAYAN = 100
TWLG_MIZO = 101
TWLG_NAGA = 102
TWLG_NOR = 9
TWLG_NORWEGIAN = 9
TWLG_NORWEGIAN_BOKMAL = 73
TWLG_NORWEGIAN_NYNORSK = 74
TWLG_ORISSI = 103
TWLG_POLISH = 75
TWLG_POR = 10
TWLG_PORTUGUESE = 10
TWLG_PORTUGUESE_BRAZIL = 76
TWLG_PUNJABI = 104
TWLG_PUSHTU = 105
TWLG_ROMANIAN = 77
TWLG_RUSSIAN = 78
TWLG_SERBIAN_CYRILLIC = 106
TWLG_SERBIAN_LATIN = 79
TWLG_SIKKIMI = 107
TWLG_SLOVAK = 80
TWLG_SLOVENIAN = 81
TWLG_SPA = 11
TWLG_SPANISH = 11
TWLG_SPANISH_MEXICAN = 82
TWLG_SPANISH_MODERN = 83
TWLG_SWE = 12
TWLG_SWEDISH = 12
TWLG_SWEDISH_FINLAND = 108
TWLG_TAMIL = 109
TWLG_TELUGU = 110
TWLG_THAI = 84
TWLG_TRIPURI = 111
TWLG_TURKISH = 85
TWLG_UKRANIAN = 86
TWLG_URDU = 112
TWLG_USA = 13
TWLG_USERLOCALE = -1
TWLG_VIETNAMESE = 113
TWLP_REFLECTIVE = 0
TWLP_TRANSMISSIVE = 1
TWLS_BLUE = 2
TWLS_GREEN = 1
TWLS_IR = 6
TWLS_NONE = 3
TWLS_RED = 0
TWLS_UV = 5
TWLS_WHITE = 4
TWMF_APPOWNS = 1
TWMF_DSMOWNS = 2
TWMF_DSOWNS = 4
TWMF_HANDLE = 16
TWMF_POINTER = 8
TWNF_AUTO = 1
TWNF_LONEPIXEL = 2
TWNF_MAJORITYRULE = 3
TWNF_NONE = 0
TWON_ARRAY = 3
TWON_DONTCARE16 = 65535
TWON_DONTCARE32 = -1
TWON_DONTCARE8 = 255
TWON_DSMCODEID = 63
TWON_DSMID = 461
TWON_ENUMERATION = 4
TWON_ICONID = 962
TWON_ONEVALUE = 5
TWON_RANGE = 6
TWOR_LANDSCAPE = 3
TWOR_PORTRAIT = 0
TWOR_ROT0 = 0
TWOR_ROT180 = 2
TWOR_ROT270 = 3
TWOR_ROT90 = 1
TWOV_ALL = 4
TWOV_AUTO = 1
TWOV_LEFTRIGHT = 3
TWOV_NONE = 0
TWOV_TOPBOTTOM = 2
TWPA_CMY = 2
TWPA_GRAY = 1
TWPA_RGB = 0
TWPCH_PATCH1 = 0
TWPCH_PATCH2 = 1
TWPCH_PATCH3 = 2
TWPCH_PATCH4 = 3
TWPCH_PATCH6 = 4
TWPCH_PATCHT = 5
TWPC_CHUNKY = 0
TWPC_PLANAR = 1
TWPF_CHOCOLATE = 0
TWPF_VANILLA = 1
TWPM_COMPOUNDSTRING = 2
TWPM_MULTISTRING = 1
TWPM_SINGLESTRING = 0
TWPR_ENDORSERBOTTOMAFTER = 7
TWPR_ENDORSERBOTTOMBEFORE = 6
TWPR_ENDORSERTOPAFTER = 5
TWPR_ENDORSERTOPBEFORE = 4
TWPR_IMPRINTERBOTTOMAFTER = 3
TWPR_IMPRINTERBOTTOMBEFORE = 2
TWPR_IMPRINTERTOPAFTER = 1
TWPR_IMPRINTERTOPBEFORE = 0
TWPS_BATTERY = 1
TWPS_EXTERNAL = 0
TWPT_BW = 0
TWPT_CIEXYZ = 8
TWPT_CMY = 4
TWPT_CMYK = 5
TWPT_GRAY = 1
TWPT_PALETTE = 3
TWPT_RGB = 2
TWPT_YUV = 6
TWPT_YUVK = 7
TWQC_GET = 1
TWQC_GETCURRENT = 8
TWQC_GETDEFAULT = 4
TWQC_RESET = 16
TWQC_SET = 2
TWRC_CANCEL = 3
TWRC_CHECKSTATUS = 2
TWRC_CUSTOMBASE = 32768
TWRC_DATANOTAVAILABLE = 9
TWRC_DSEVENT = 4
TWRC_ENDOFLIST = 7
TWRC_FAILURE = 1
TWRC_INFONOTSUPPORTED = 8
TWRC_NOTDSEVENT = 5
TWRC_SUCCESS = 0
TWRC_XFERDONE = 6
TWSS_2A0 = 18
TWSS_4A0 = 17
TWSS_A0 = 19
TWSS_A1 = 20
TWSS_A10 = 25
TWSS_A2 = 21
TWSS_A3 = 11
TWSS_A4 = 1
TWSS_A4LETTER = 1
TWSS_A5 = 5
TWSS_A6 = 13
TWSS_A7 = 22
TWSS_A8 = 23
TWSS_A9 = 24
TWSS_B3 = 12
TWSS_B4 = 6
TWSS_B5LETTER = 2
TWSS_B6 = 7
TWSS_BUSINESSCARD = 53
TWSS_C0 = 44
TWSS_C1 = 45
TWSS_C10 = 51
TWSS_C2 = 46
TWSS_C3 = 47
TWSS_C4 = 14
TWSS_C5 = 15
TWSS_C6 = 16
TWSS_C7 = 48
TWSS_C8 = 49
TWSS_C9 = 50
TWSS_ISOB0 = 26
TWSS_ISOB1 = 27
TWSS_ISOB10 = 33
TWSS_ISOB2 = 28
TWSS_ISOB3 = 12
TWSS_ISOB4 = 6
TWSS_ISOB5 = 29
TWSS_ISOB6 = 7
TWSS_ISOB7 = 30
TWSS_ISOB8 = 31
TWSS_ISOB9 = 32
TWSS_JISB0 = 34
TWSS_JISB1 = 35
TWSS_JISB10 = 43
TWSS_JISB2 = 36
TWSS_JISB3 = 37
TWSS_JISB4 = 38
TWSS_JISB5 = 2
TWSS_JISB6 = 39
TWSS_JISB7 = 40
TWSS_JISB8 = 41
TWSS_JISB9 = 42
TWSS_NONE = 0
TWSS_USEXECUTIVE = 10
TWSS_USLEDGER = 9
TWSS_USLEGAL = 4
TWSS_USLETTER = 3
TWSS_USSTATEMENT = 52
TWSX_FILE = 1
TWSX_MEMORY = 2
TWSX_NATIVE = 0
TWTY_BOOL = 6
TWTY_FIX32 = 7
TWTY_FRAME = 8
TWTY_INT16 = 1
TWTY_INT32 = 2
TWTY_INT8 = 0
TWTY_STR1024 = 13
TWTY_STR128 = 11
TWTY_STR255 = 12
TWTY_STR32 = 9
TWTY_STR64 = 10
TWTY_UINT16 = 4
TWTY_UINT32 = 5
TWTY_UINT8 = 3
TWTY_UNI512 = 14
TWUN_CENTIMETERS = 1
TWUN_INCHES = 0
TWUN_PICAS = 2
TWUN_PIXELS = 5
TWUN_POINTS = 3
TWUN_TWIPS = 4


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


class excTWCC_BADDEST(Exception):
    pass


class excTWCC_BADPROTOCOL(Exception):
    pass


class excTWCC_BUMMER(Exception):
    """General failure.  Unload Source immediately."""
    pass


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


_ext_to_type = {'.bmp': TWFF_BMP,
                '.jpg': TWFF_JFIF,
                '.jpeg': TWFF_JFIF,
                '.png': TWFF_PNG,
                '.tiff': TWFF_TIFF,
                '.tif': TWFF_TIFF,
                }


class CancelAll(Exception):
    """Exception used by callbacks to cancel remaining image transfers"""
    pass


class CheckStatus(Exception):
    """This exception means that operation succeeded but user value was truncated
    to fit valid range
    """
    pass


class _Image(object):
    def __init__(self, handle):
        self._handle = handle
        
    def __del__(self):
        self.close()
        
    def close(self):
        """Releases memory of image"""
        self._free(self._handle)
        self._handle = None
        
    def save(self, filepath):
        """Saves in-memory image to BMP file"""
        _dib_write(self._handle, filepath, self._lock, self._unlock)


def _float2fix(x):
    if x <= -2**15 - 1 and 2**15 + 1 <= x:
        raise Exception('Float value is out of range')
    x = int(x * 2**16 + 0.5)
    whole = x >> 16
    frac = x & 0xffff
    return TW_FIX32(whole, frac)


def _fix2float(x):
    return x.Whole + float(x.Frac) / 2**16 


def _frame2tuple(frame):
    return (_fix2float(frame.Left),
            _fix2float(frame.Top),
            _fix2float(frame.Right),
            _fix2float(frame.Bottom))


def _tuple2frame(tup):
    return TW_FRAME(_float2fix(tup[0]),
                    _float2fix(tup[1]),
                    _float2fix(tup[2]),
                    _float2fix(tup[3]))


class TW_CAPABILITY(Structure):
    _pack_ = 2
    _fields_ = [("Cap", c_uint16),
                ('ConType', c_uint16),
                ('hContainer', c_void_p)]


class TW_ONEVALUE(Structure):
    _pack_ = 2
    _fields_ = [('ItemType', c_uint16),
                ('Item', c_uint32)]


class TW_FIX32(Structure):
    _pack_ = 2
    _fields_ = [('Whole', c_int16),
                ('Frac', c_uint16)]


class TW_FRAME(Structure):
    _pack_ = 2
    _fields_ = [('Left', TW_FIX32),
                ('Top', TW_FIX32),
                ('Right', TW_FIX32),
                ('Bottom', TW_FIX32)]


class TW_STATUS(Structure):
    _pack_ = 2
    _fields_ = [('ConditionCode', c_uint16), # Any TWCC_ constant
                ('Data', c_uint16)]


class TW_IMAGELAYOUT(Structure):
    _pack_ = 2
    _fields_ = [('Frame', TW_FRAME), # Any TWCC_ constant
                ('DocumentNumber', c_uint32),
                ('PageNumber', c_uint32),
                ('FrameNumber', c_uint32)]


class TW_USERINTERFACE(Structure):
    _pack_ = 2
    _fields_ = [('ShowUI', c_uint16),
                ('ModalUI', c_uint16),
                ('hParent', c_void_p)]


class MSG(Structure):
    _pack_ = 8
    _fields_ = [('hwnd', c_void_p),
                ('message', c_uint),
                ('wParam', c_void_p),
                ('lParam', c_void_p),
                ('time', c_uint32),
                ('pt_x', c_long),
                ('pt_y', c_long)]


class TW_EVENT(Structure):
    _pack_ = 2
    _fields_ = [('pEvent', c_void_p),
                ('TWMessage', c_uint16)]


class TW_VERSION(Structure):
    _pack_ = 2
    _fields_ = [('MajorNum', c_uint16),
                ('MinorNum', c_uint16),
                ('Language', c_uint16),
                ('Country', c_uint16),
                ('Info', c_char * 34)]


class TW_IDENTITY(Structure):
    _pack_ = 2
    _fields_ = [('Id', c_uint32),
                ('Version', TW_VERSION),
                ('ProtocolMajor', c_uint16),
                ('ProtocolMinor', c_uint16),
                ('SupportedGroups', c_uint32),
                ('Manufacturer', c_char * 34),
                ('ProductFamily', c_char * 34),
                ('ProductName', c_char * 34)]


class TW_IMAGEINFO(Structure):
    _pack_ = 2
    _fields_ = [('XResolution', TW_FIX32),
                ('YResolution', TW_FIX32),
                ('ImageWidth', c_int32),
                ('ImageLength', c_int32),
                ('SamplesPerPixel', c_int16),
                ('BitsPerSample', c_int16 * 8),
                ('BitsPerPixel', c_int16),
                ('Planar', c_uint16),
                ('PixelType', c_int16),
                ('Compression', c_uint16)]


class TW_PENDINGXFERS(Structure):
    _pack_ = 2
    _fields_ = [('Count', c_uint16),
                ('EOJ', c_uint32)]


class TW_RANGE(Structure):
    _pack_ = 2
    _fields_ = [('ItemType', c_uint16),
                ('MinValue', c_uint32),
                ('MaxValue', c_uint32),
                ('StepSize', c_uint32),
                ('DefaultValue', c_uint32),
                ('CurrentValue', c_uint32)]


class TW_ENUMERATION(Structure):
    _pack_ = 2
    _fields_ = [('ItemType', c_uint16),
                ('NumItems', c_uint32),
                ('CurrentIndex', c_uint32),
                ('DefaultIndex', c_uint32)]


class TW_ARRAY(Structure):
    _pack_ = 2
    _fields_ = [('ItemType', c_uint16),
                ('NumItems', c_uint32)]


class TW_SETUPFILEXFER(Structure):
    _pack_ = 2
    _fields_ = [('FileName', c_char * 256),
                ('Format', c_uint16),
                ('VRefNum', c_int16)]


def _is_windows():
    return platform.system() == 'Windows'


if _is_windows():
    FUNCTYPE = ctypes.WINFUNCTYPE
else:
    FUNCTYPE = ctypes.CFUNCTYPE


class TW_ENTRYPOINT(Structure):
    _pack_ = 2
    _fields_ = [('Size', c_uint32),
                ('DSM_Entry', FUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))),
                ('DSM_MemAllocate', FUNCTYPE(c_void_p, c_uint32)),
                ('DSM_MemFree', FUNCTYPE(None, c_void_p)),
                ('DSM_MemLock', FUNCTYPE(c_void_p, c_void_p)),
                ('DSM_MemUnlock', FUNCTYPE(None, c_void_p))]


_mapping = {TWTY_INT8: c_int8,
            TWTY_UINT8: c_uint8,
            TWTY_INT16: c_int16,
            TWTY_UINT16: c_uint16,
            TWTY_UINT32: c_uint32,
            TWTY_INT32: c_int32,
            TWTY_BOOL: c_uint16,
            TWTY_FIX32: TW_FIX32,
            TWTY_FRAME: TW_FRAME,
            TWTY_STR32: c_char*34,
            TWTY_STR64: c_char*66,
            TWTY_STR128: c_char*130,
            TWTY_STR255: c_char*255}


def _is_good_type(type_id):
    return type_id in list(_mapping.keys()) 


def _struct2dict(struct, decode):
    result = {}
    for field, _ in struct._fields_:
        value = getattr(struct, field)
        if hasattr(value, "_length_") and hasattr(value, "_type_"):
            # Probably an array
            value = list(value)
        elif hasattr(value, "_fields_"):
            # Probably another struct
            value = _struct2dict(value, decode)
        if isinstance(value, bytes):
            value = decode(value)
        result[field] = value
    return result


_exc_mapping = {TWCC_SUCCESS: excTWCC_SUCCESS,
                TWCC_BUMMER: excTWCC_BUMMER,
                TWCC_LOWMEMORY: MemoryError,
                TWCC_NODS: excTWCC_NODS,
                TWCC_OPERATIONERROR: excTWCC_OPERATIONERROR,
                TWCC_BADCAP: excTWCC_BADCAP,
                TWCC_BADPROTOCOL: excTWCC_BADPROTOCOL,
                TWCC_BADVALUE: ValueError,
                TWCC_SEQERROR: excTWCC_SEQERROR,
                TWCC_BADDEST: excTWCC_BADDEST,
                TWCC_CAPUNSUPPORTED: excTWCC_CAPUNSUPPORTED,
                TWCC_CAPBADOPERATION: excTWCC_CAPBADOPERATION,
                TWCC_CAPSEQERROR: excTWCC_CAPSEQERROR,
                TWCC_DENIED: excTWCC_DENIED,
                TWCC_FILEEXISTS: excTWCC_FILEEXISTS,
                TWCC_FILENOTFOUND: excTWCC_FILENOTFOUND,
                TWCC_NOTEMPTY: excTWCC_NOTEMPTY,
                TWCC_PAPERJAM: excTWCC_PAPERJAM,
                TWCC_PAPERDOUBLEFEED: excTWCC_PAPERDOUBLEFEED,
                TWCC_FILEWRITEERROR: excTWCC_FILEWRITEERROR,
                TWCC_CHECKDEVICEONLINE: excTWCC_CHECKDEVICEONLINE}


def _win_check(result, func, args):
    if func is _GlobalFree:
        if result:
            raise WinError()
        return None
    elif func is _GlobalUnlock:
        if not result and GetLastError() != 0:
            raise WinError()
        return result
    elif func is _GetMessage:
        if result == -1:
            raise WinError()
        return result
    elif func is _TranslateMessage or func is _DispatchMessage:
        return result
    else:
        if not result:
            raise WinError()
        return result


if _is_windows():
    _GlobalLock = windll.kernel32.GlobalLock
    _GlobalLock.errcheck = _win_check
    _GlobalUnlock = windll.kernel32.GlobalUnlock
    _GlobalUnlock.errcheck = _win_check
    _GlobalAlloc = windll.kernel32.GlobalAlloc
    _GlobalAlloc.errcheck = _win_check
    _GlobalFree = windll.kernel32.GlobalFree
    _GlobalFree.errcheck = _win_check
    _GlobalSize = windll.kernel32.GlobalSize
    _GlobalSize.errcheck = _win_check
    _GetMessage = windll.user32.GetMessageW
    _TranslateMessage = windll.user32.TranslateMessage
    _TranslateMessage.errcheck = _win_check
    _DispatchMessage = windll.user32.DispatchMessageW
    _DispatchMessage.errcheck = _win_check

    GMEM_ZEROINIT = 0x0040

    def _twain1_alloc(size):
        return _GlobalAlloc(GMEM_ZEROINIT, size)

    _twain1_free = _GlobalFree
    _twain1_lock = _GlobalLock
    _twain1_unlock = _GlobalUnlock
else:
    # Mac
    def _twain1_alloc(size):
        return ctypes.libc.malloc(size)

    def _twain1_lock(handle):
        return handle

    def _twain1_unlock(handle):
        pass

    def _twain1_free(handle):
        return ctypes.libc.free(handle)


class Source(object):
    """
    This object represents connection to Data Source.

    An instance of this class can be created by calling
    :meth:`SourceManager.open_source`
    """
    def __init__(self, sm, ds_id):
        self._sm = sm
        self._id = ds_id
        self._state = 'open'
        self._version2 = bool(ds_id.SupportedGroups & DF_DS2)
        if self._version2:
            self._alloc = sm._alloc
            self._free = sm._free
            self._lock = sm._lock
            self._unlock = sm._unlock
            self._encode = sm._encode
            self._decode = sm._decode
        else:
            self._alloc = _twain1_alloc
            self._free = _twain1_free
            self._lock = _twain1_lock
            self._unlock = _twain1_unlock
            self._encoding = sys.getfilesystemencoding()
            self._encode = lambda s: s.encode(self._encoding)
            self._decode = lambda s: s.decode(self._encoding)
        
    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """This method is used to close the data source object.
        It gives finer control over this connects than relying on garbage collection.
        """
        if self._state == 'ready':
            self._end_all_xfers()
        if self._state == 'enabled':
            self._disable()
        if self._state == 'open':
            self._sm._close_ds(self._id)
            self._state = 'closed'
            self._sm = None

    def _call(self, dg, dat, msg, buf, expected_returns=(TWRC_SUCCESS,)):
        return self._sm._call(self._id, dg, dat, msg, buf, expected_returns)

    def _get_capability(self, cap, current):
        twCapability = TW_CAPABILITY(cap, TWON_DONTCARE16, 0)
        self._call(DG_CONTROL, DAT_CAPABILITY, current, byref(twCapability))
        try:
            ptr = self._lock(twCapability.hContainer)
            try:
                if twCapability.ConType == TWON_ONEVALUE:
                    type_id = cast(ptr, POINTER(c_uint16))[0] 
                    if not _is_good_type(type_id):
                        msg = "Capability Code = %d, Format Code = %d, Item Type = %d" % (cap,
                                                                                          twCapability.ConType,
                                                                                          type_id)
                        raise excCapabilityFormatNotSupported(msg)
                    ctype = _mapping.get(type_id)
                    val = cast(ptr + 2, POINTER(ctype))[0]                   
                    if type_id in (TWTY_INT8, TWTY_UINT8, TWTY_INT16, TWTY_UINT16, TWTY_UINT32, TWTY_INT32):
                        pass
                    elif type_id == TWTY_BOOL:
                        val = bool(val)
                    elif type_id == TWTY_FIX32:
                        val = _fix2float(val)
                    elif type_id == TWTY_FRAME:
                        val = _frame2tuple(val)
                    return type_id, val
                elif twCapability.ConType == TWON_RANGE:
                    rng = cast(ptr, POINTER(TW_RANGE)).contents
                    return {'MinValue': rng.MinValue,
                            'MaxValue': rng.MaxValue,
                            'StepSize': rng.StepSize,
                            'DefaultValue': rng.DefaultValue,
                            'CurrentValue': rng.CurrentValue}
                elif twCapability.ConType == TWON_ENUMERATION:
                    enum = cast(ptr, POINTER(TW_ENUMERATION)).contents
                    if not _is_good_type(enum.ItemType):
                        msg = "Capability Code = %d, Format Code = %d, Item Type = %d" % (cap,
                                                                                          twCapability.ConType,
                                                                                          enum.ItemType)
                        raise excCapabilityFormatNotSupported(msg)
                    ctype = _mapping[enum.ItemType]
                    item_p = cast(ptr + sizeof(TW_ENUMERATION), POINTER(ctype))
                    values = [el for el in item_p[0:enum.NumItems]]
                    return enum.ItemType, (enum.CurrentIndex, enum.DefaultIndex, values)
                elif twCapability.ConType == TWON_ARRAY:
                    arr = cast(ptr, POINTER(TW_ARRAY)).contents
                    if not _is_good_type(arr.ItemType):
                        msg = "Capability Code = %d, Format Code = %d, Item Type = %d" % (cap,
                                                                                          twCapability.ConType,
                                                                                          arr.ItemType)
                        raise excCapabilityFormatNotSupported(msg)
                    ctype = _mapping[arr.ItemType]
                    item_p = cast(ptr + sizeof(TW_ARRAY), POINTER(ctype))
                    return arr.ItemType, [el for el in item_p[0:arr.NumItems]]
                else:
                    msg = "Capability Code = %d, Format Code = %d" % (cap, twCapability.ConType)
                    raise excCapabilityFormatNotSupported(msg)
            finally:
                self._unlock(twCapability.hContainer)
        finally:
            self._free(twCapability.hContainer)

    def get_capability(self, cap):
        """This function is used to return the capability information from the source.
        If the capability is not supported, an exception should be returned.
        Capabilities are returned as a tuple of a type (TWTY_*) and a value.
        The format of values depends on their container type.
        Capabilities can be in any of the following containers:
            singleton, range, enumerator or array.

         singletons are returned as a single value (integer or string)
         ranges are returned as a tuple dictionary containing MinValue,
             MaxValue, StepSize, DefaultValue and CurrentValue
         enumerators and arrays are returned as tuples, each containing
             a list which has the actual values
        """
        return self._get_capability(cap, MSG_GET)
    
    def get_capability_current(self, cap):
        """This function is used to return the current value of a capability from the source.
        If the capability is not supported, an exception should be returned.
        Capabilities are returned as a tuple of a type (TWTY_*) and a value.
        The format of values depends on their container type.
        Capabilities can be in any of the following containers:
            singleton, range, enumerator or array.

         singletons are returned as a single value (integer or string)
         ranges are returned as a tuple dictionary containing MinValue,
             MaxValue, StepSize, DefaultValue and CurrentValue
         enumerators and arrays are returned as tuples, each containing
             a list which has the actual values
        """
        return self._get_capability(cap, MSG_GETCURRENT)
    
    def get_capability_default(self, cap):
        """This function is used to return the default value of a capability from the source.
        If the capability is not supported, an exception should be returned.
        Capabilities are returned as a tuple of a type (TWTY_*) and a value.
        The format of values depends on their container type.
        Capabilities can be in any of the following containers:
            singleton, range, enumerator or array.

         singletons are returned as a single value (integer or string)
         ranges are returned as a tuple dictionary containing MinValue,
             MaxValue, StepSize, DefaultValue and CurrentValue
         enumerators and arrays are returned as tuples, each containing
             a list which has the actual values
        """
        return self._get_capability(cap, MSG_GETDEFAULT)
    
    @property
    def name(self):
        """Get the name of the source. This can be used later for
        connecting to the same source.
        """
        return self._decode(self._id.ProductName)
    
    @property
    def identity(self):
        """This function is used to retrieve information about the source.
        driver. The information is returned in a dictionary.
        """
        res = _struct2dict(self._id, self._decode)
        res.update(_struct2dict(self._id.Version, self._decode))
        return res
        
    def set_capability(self, cap, type_id, value):
        """This function is used to set the value of a capability in the source.
        Three parameters are required, a Capability Identifier (twain.CAP_* or
        twain.ICAP_*) a value type (twain.TWTY_*) and a value
        If the capability is not supported, an exception should be returned.
        This function is used to set a value using a TW_ONEVALUE.
        """
        if not _is_good_type(type_id):
            raise excCapabilityFormatNotSupported("Capability Code = %d, Format Code = %d" % (cap, type_id))
        ctype = _mapping[type_id]
        if type_id in (TWTY_INT8, TWTY_INT16, TWTY_INT32, TWTY_UINT8, TWTY_UINT16, TWTY_UINT32, TWTY_BOOL):
            cval = ctype(value)
        elif type_id in (TWTY_STR32, TWTY_STR64, TWTY_STR128, TWTY_STR255):
            cval = ctype(self._encode(value))
        elif type_id == TWTY_FIX32:
            cval = _float2fix(value)
        elif type_id == TWTY_FRAME:
            cval = _tuple2frame(value)
        else:
            assert 0, 'invalid case'
        handle = self._alloc(sizeof(TW_ONEVALUE) + sizeof(ctype))
        try:
            ptr = self._lock(handle)
            try:
                cast(ptr, POINTER(c_uint16))[0] = type_id
                cast(ptr + 2, POINTER(ctype))[0] = cval
            finally:
                self._unlock(handle)
            capability = TW_CAPABILITY(cap, TWON_ONEVALUE, handle)
            rv = self._call(DG_CONTROL,
                            DAT_CAPABILITY,
                            MSG_SET,
                            byref(capability),
                            [TWRC_CHECKSTATUS])
        finally:
            self._free(handle)
        if rv == TWRC_CHECKSTATUS:
            raise CheckStatus
        
    def reset_capability(self, cap):
        """This function is used to reset the value of a capability to the source default.

        :param cap: Capability Identifier (twain.CAP_* or twain.ICAP_*).
        """
        cap = TW_CAPABILITY(Cap=cap)
        self._call(DG_CONTROL, DAT_CAPABILITY, MSG_RESET, byref(cap))
        
    def set_image_layout(self, frame, document_number=1, page_number=1, frame_number=1):
        """This function is used to inform the source of the Image Layout.

        It uses a tuple containing frame coordinates, document
        number, page number, frame number.
        """
        il = TW_IMAGELAYOUT(Frame=_tuple2frame(frame),
                            DocumentNumber=document_number,
                            PageNumber=page_number,
                            FrameNumber=frame_number)
        rv = self._call(DG_IMAGE,
                        DAT_IMAGELAYOUT,
                        MSG_SET,
                        byref(il),
                        (TWRC_SUCCESS, TWRC_CHECKSTATUS))
        if rv == TWRC_CHECKSTATUS:
            raise CheckStatus

    def get_image_layout(self):
        """This function is used to ask the source for Image Layout.

        It returns a tuple containing frame coordinates, document
        number, page number, frame number.

        Valid states 4 through 6
        """
        il = TW_IMAGELAYOUT()
        self._call(DG_IMAGE, DAT_IMAGELAYOUT, MSG_GET, byref(il))
        return _frame2tuple(il.Frame), il.DocumentNumber, il.PageNumber, il.FrameNumber    
    
    def get_image_layout_default(self):
        """This function is used to ask the source for default Image Layout.

        It returns a tuple containing frame coordinates, document
        number, page number, frame number.

        Valid states 4 through 6
        """
        il = TW_IMAGELAYOUT()
        self._call(DG_IMAGE, DAT_IMAGELAYOUT, MSG_GETDEFAULT, byref(il))
        return _frame2tuple(il.Frame), il.DocumentNumber, il.PageNumber, il.FrameNumber
    
    def reset_image_layout(self):
        """This function is used to reset Image Layout to its default settings"""
        il = TW_IMAGELAYOUT()
        self._call(DG_IMAGE, DAT_IMAGELAYOUT, MSG_RESET, byref(il))

    def _enable(self, show_ui, modal_ui, hparent):
        """This function is used to ask the source to begin aquistion.
        Parameters:
            show_ui - bool
            modal_ui - bool
        """
        ui = TW_USERINTERFACE(ShowUI=show_ui, ModalUI=modal_ui, hParent=hparent)
        self._call(DG_CONTROL, DAT_USERINTERFACE, MSG_ENABLEDS, byref(ui))
        self._state = 'enabled'

    def _disable(self):
        """This function is used to ask the source to hide the user interface."""
        ui = TW_USERINTERFACE()
        self._call(DG_CONTROL, DAT_USERINTERFACE, MSG_DISABLEDS, byref(ui))
        self._state = 'open'
        
    def _process_event(self, msg_ref):
        """The TWAIN interface requires that the windows events
        are available to both the application and the twain
        source (which operates in the same process).
        This method is called in the event loop to pass on those
        events.
        """
        event = TW_EVENT(cast(msg_ref, c_void_p), 0)
        rv = self._call(DG_CONTROL,
                        DAT_EVENT,
                        MSG_PROCESSEVENT,
                        byref(event),
                        (TWRC_DSEVENT,
                         TWRC_NOTDSEVENT))
        if event.TWMessage == MSG_XFERREADY:
            self._state = 'ready'
        return rv, event.TWMessage
    
    def _modal_loop(self, callback):
        done = False
        msg = MSG()
        while not done:
            if not _GetMessage(byref(msg), 0, 0, 0):
                break
            rc, event = self._process_event(byref(msg))
            if callback:
                callback(event)
            if event in (MSG_XFERREADY, MSG_CLOSEDSREQ):
                done = True
            if rc == TWRC_NOTDSEVENT:
                _TranslateMessage(byref(msg))
                _DispatchMessage(byref(msg))
    
    def _acquire(self, callback, show_ui=True, modal=False):
        self._enable(show_ui, modal, self._sm._hwnd)
        try:
            def callback_lolevel(event):
                if event == MSG_XFERREADY:
                    more = True
                    while more:
                        try:
                            more = callback()
                        except CancelAll:
                            self._end_all_xfers()
                            break
            self._modal_loop(callback_lolevel)
        finally:
            self._disable()
    
    @property
    def file_xfer_params(self):
        """ Property which stores tuple of (file name, format) where format is one of TWFF_*

        This property is used by :meth:`xfer_image_by_file`

        Valid states: 4, 5, 6
        """
        sfx = TW_SETUPFILEXFER()
        self._call(DG_CONTROL, DAT_SETUPFILEXFER, MSG_GET, byref(sfx))
        return self._decode(sfx.FileName), sfx.Format
    
    @file_xfer_params.setter
    def file_xfer_params(self, params):
        (path, fmt) = params
        sfx = TW_SETUPFILEXFER(self._encode(path), fmt, 0)
        self._call(DG_CONTROL, DAT_SETUPFILEXFER, MSG_SET, byref(sfx))

    @property
    def image_info(self):
        """This function is used to ask the source for Image Info.
        Normally, the application is notified that the image is
        ready for transfer using the message loop. However, it is
        hard to get at the message loop in toolkits such as wxPython.
        As an alternative, I poll the source looking for image information.
        When the image information is available, the image is ready for transfer

        Valid states: 6, 7
        """
        ii = TW_IMAGEINFO()
        self._call(DG_IMAGE,
                   DAT_IMAGEINFO,
                   MSG_GET,
                   byref(ii))
        return {"XResolution": _fix2float(ii.XResolution),
                "YResolution": _fix2float(ii.YResolution),
                "ImageWidth": ii.ImageWidth,
                "ImageLength": ii.ImageLength,
                "SamplesPerPixel": ii.SamplesPerPixel,
                "BitsPerSample": list(ii.BitsPerSample),
                "BitsPerPixel": ii.BitsPerPixel,
                "Planar": ii.Planar,
                "PixelType": ii.PixelType,
                "Compression": ii.Compression}
    
    def _get_native_image(self):
        hbitmap = c_void_p()
        rv = self._call(DG_IMAGE,
                        DAT_IMAGENATIVEXFER,
                        MSG_GET,
                        byref(hbitmap),
                        (TWRC_XFERDONE, TWRC_CANCEL))
        return rv, hbitmap
            
    def _get_file_image(self):
        return self._call(DG_IMAGE,
                          DAT_IMAGEFILEXFER,
                          MSG_GET,
                          None,
                          (TWRC_XFERDONE, TWRC_CANCEL))

    def _get_file_audio(self):
        return self._call(DG_AUDIO,
                          DAT_AUDIOFILEXFER,
                          MSG_GET,
                          None,
                          (TWRC_XFERDONE, TWRC_CANCEL)) 

    def _end_xfer(self):
        px = TW_PENDINGXFERS()
        self._call(DG_CONTROL, DAT_PENDINGXFERS, MSG_ENDXFER, byref(px))
        if px.Count == 0:
            self._state = 'enabled'
        return px.Count
    
    def _end_all_xfers(self):
        """Cancel all outstanding transfers on the data source."""
        px = TW_PENDINGXFERS()
        self._call(DG_CONTROL, DAT_PENDINGXFERS, MSG_RESET, byref(px))
        self._state = 'enabled'
        
    def request_acquire(self, show_ui, modal_ui):
        """This function is used to ask the source to begin acquisition.

        Transitions Source to state 5.

        :param show_ui: bool (default 1)
        :param modal_ui: bool (default 1)

        Valid states: 4
        """
        self._enable(show_ui, modal_ui, self._sm._hwnd)
    
    def modal_loop(self):
        """This function should be called after call to :func:`requiest_acquire`
        it will return after acquisition complete.

        Valid states: 5
        """
        self._modal_loop(self._sm._cb)
        
    def hide_ui(self):
        """This function is used to ask the source to hide the user interface.

        Transitions Source to state 4 if successful.

        Valid states: 5
        """
        self._disable()
        
    def xfer_image_natively(self):
        """Perform a 'Native' form transfer of the image.

        When successful, this routine returns two values,
        an image handle and a count of the number of images
        remaining in the source.

        If remaining number of images is zero Source will
        transition to state 5, otherwise it stays in state 6
        in which case you should call
        :meth:`xfer_image_natively` again.

        Valid states: 6
        """
        rv, handle = self._get_native_image()
        more = self._end_xfer()
        if rv == TWRC_CANCEL:
            raise excDSTransferCancelled
        return handle.value, more

    def xfer_image_by_file(self):
        """Perform a file based transfer of the image.

        When successful, the file is saved to the image file,
        defined in a previous call to :meth:`file_xfer_params`.

        Returns  the number of pending transfers

        If remaining number of images is zero Source will
        transition to state 5, otherwise it stays in state 6
        in which case you should call
        :meth:`xfer_image_natively` again.

        Valid states: 6
        """
        rv = self._get_file_image()
        more = self._end_xfer()
        if rv == TWRC_CANCEL:
            raise excDSTransferCancelled
        return more

    def acquire_file(self, before, after=lambda more: None, show_ui=True, modal=False):
        """Acquires one ore more images as files. Call returns when acquisition complete.

        :param before: Callback called before each acquired file, it should return
                       full file path. It can also throw CancelAll to cancel acquisition
        :keyword after: Callback called after each acquired file, it receives number of
                        images remaining. It can throw CancelAll to cancel remaining
                        acquisition
        :keyword show_ui: If True source's UI will be presented to user
        :keyword modal: If True source's UI will be modal
        """
        _, (_, _, mechs) = self.get_capability(ICAP_XFERMECH)
        if TWSX_FILE not in mechs:
            raise Exception('File transfer is not supported')

        def callback():
            filepath = before(self.image_info)
            import os
            _, ext = os.path.splitext(filepath)
            ext = ext.lower()
            if ext != '.bmp':
                import tempfile
                handle, bmppath = tempfile.mkstemp('.bmp')
                os.close(handle)
            else:
                bmppath = filepath
                
            self.file_xfer_params = bmppath, TWFF_BMP
            rv = self._get_file_image()
            more = self._end_xfer()
            if rv == TWRC_CANCEL:
                raise excDSTransferCancelled
            if ext != '.bmp':
                import Image
                Image.open(bmppath).save(filepath)            
                os.remove(bmppath)
            after(more)
            return more

        self.set_capability(ICAP_XFERMECH, TWTY_UINT16, TWSX_FILE)
        self._acquire(callback, show_ui, modal)
    
    def acquire_natively(self, after, before=lambda img_info: None, show_ui=True, modal=False):
        """Acquires one ore more images in memory. Call returns when acquisition complete

        :param after: Callback called after each acquired file, it receives an image object and
                     number of images remaining. It can throw CancelAll to cancel remaining
                     acquisition
        :keyword before: Callback called before each acquired file. It can throw CancelAll
                      to cancel acquisition
        :keyword show_ui: If True source's UI will be presented to user
        :keyword modal:   If True source's UI will be modal
        """

        def callback():
            before(self.image_info)
            rv, handle = self._get_native_image()
            more = self._end_xfer()
            if rv == TWRC_CANCEL:
                raise excDSTransferCancelled
            after(_Image(handle), more)
            return more

        self.set_capability(ICAP_XFERMECH, TWTY_UINT16, TWSX_NATIVE)
        self._acquire(callback, show_ui, modal)
        
    def is_twain2(self):
        return self._version2

    # backward compatible aliases
    def destroy(self):
        self.close()

    def GetCapabilityCurrent(self, cap):
        warnings.warn("GetCapabilityCurrent is deprecated, use get_capability_current instead", DeprecationWarning)
        return self.get_capability_current(cap)

    def GetCapabilityDefault(self, cap):
        warnings.warn("GetCapabilityDefault is deprecated, use get_capability_default instead", DeprecationWarning)
        return self.get_capability_default(cap)

    def GetSourceName(self):
        warnings.warn("GetSourceName is deprecated, use name property instead", DeprecationWarning)
        return self.name

    def GetIdentity(self):
        warnings.warn("GetIdentity is deprecated, use identity property instead", DeprecationWarning)
        return self.identity

    def GetCapability(self, cap):
        warnings.warn("GetCapability is deprecated, use get_capability instead", DeprecationWarning)
        return self.get_capability(cap)

    def SetCapability(self, cap, type_id, value):
        warnings.warn("SetCapability is deprecated, use set_capability instead", DeprecationWarning)
        return self.set_capability(cap, type_id, value)

    def ResetCapability(self, cap):
        warnings.warn("ResetCapability is deprecated, use reset_capability instead", DeprecationWarning)
        self.reset_capability(cap)

    def SetImageLayout(self, frame, document_number=1, page_number=1, frame_number=1):
        warnings.warn("SetImageLayout is deprecated, use set_image_layout instead", DeprecationWarning)
        self.set_image_layout(frame, document_number, page_number, frame_number)

    def GetImageLayout(self):
        warnings.warn("GetImageLayout is deprecated, use get_image_layout instead", DeprecationWarning)
        return self.get_image_layout()

    def GetDefaultImageLayout(self):
        warnings.warn("GetDefaultImageLayout is deprecated, use get_default_image_layout instead", DeprecationWarning)
        return self.get_image_layout_default()

    def ResetImageLayout(self):
        warnings.warn("ResetImageLayout is deprecated, use reset_image_layout instead", DeprecationWarning)
        self.reset_image_layout()

    def RequestAcquire(self, show_ui, modal_ui):
        warnings.warn("RequestAcquire is deprecated, use reset_acquire instead", DeprecationWarning)
        self.request_acquire(show_ui, modal_ui)

    def ModalLoop(self):
        warnings.warn("ModalLoop is deprecated, use modal_loop instead", DeprecationWarning)
        self.modal_loop()

    def HideUI(self):
        warnings.warn("HideUI is deprecated, use hide_ui instead", DeprecationWarning)
        self.hide_ui()

    def SetXferFileName(self, path, format):
        warnings.warn("SetXferFileName is deprecated, use file_xfer_params instead", DeprecationWarning)
        self.file_xfer_params = (path, format)

    def GetXferFileName(self):
        warnings.warn("GetXferFileName is deprecated, use file_xfer_params property instead", DeprecationWarning)
        return self.file_xfer_params

    def GetImageInfo(self):
        warnings.warn("GetImageInfo is deprecated, use image_info property instead", DeprecationWarning)
        return self.image_info

    def XferImageNatively(self):
        warnings.warn("XferImageNatively is deprecated, use xfer_image_natively instead", DeprecationWarning)
        return self.xfer_image_natively()

    def XferImageByFile(self):
        warnings.warn("XferImageByFile is deprecated, use xfer_image_by_file instead", DeprecationWarning)
        return self.xfer_image_by_file()


def _get_dsm(dsm_name=None):
    if _is_windows():
        try:
            if dsm_name:
                return ctypes.WinDLL(dsm_name)
            else:
                dsm_name = 'twaindsm.dll'
                try:
                    return ctypes.WinDLL(dsm_name)
                except WindowsError:
                    dsm_name = 'twain_32.dll'
                    return ctypes.WinDLL(dsm_name)
        except WindowsError as e:
            raise excSMLoadFileFailed(e)
    else:
        return ctypes.CDLL('/System/Library/Frameworks/TWAIN.framework/TWAIN')


class SourceManager(object):
    """Represents a Data Source Manager connection"""
    def __init__(self,
                 parent_window=None,
                 MajorNum=1,
                 MinorNum=0,
                 Language=TWLG_USA,
                 Country=TWCY_USA,
                 Info="",
                 ProductName="TWAIN Python Interface",
                 ProtocolMajor=TWON_PROTOCOLMAJOR,
                 ProtocolMinor=TWON_PROTOCOLMINOR,
                 SupportedGroups=DG_IMAGE | DG_CONTROL,
                 Manufacturer="Kevin Gill",
                 ProductFamily="TWAIN Python Interface",
                 dsm_name = None):
        """Constructor for a TWAIN Source Manager Object. This
        constructor has one position argument, parent_window, which
        should contain .

        :param parent_window: can contain Tk, Wx or Gtk window object or the windows
            handle of the main window
        :keyword MajorNum:   default = 1
        :keyword MinorNum:   default = 0
        :keyword Language:   default = TWLG_USA
        :keyword Country:    default = TWCY_USA
        :keyword Info:       default = 'TWAIN Python Interface 1.0.0.0  10/02/2002'
        :keyword ProductName:  default = 'TWAIN Python Interface'
        :keyword ProtocolMajor: default = TWON_PROTOCOLMAJOR
        :keyword ProtocolMinor: default = TWON_PROTOCOLMINOR
        :keyword SupportedGroups: default =  DG_IMAGE | DG_CONTROL
        :keyword Manufacturer:    default =  'Kevin Gill'
        :keyword ProductFamily: default = 'TWAIN Python Interface'

        """
        self._sources = weakref.WeakSet()
        self._cb = None
        self._state = 'closed'
        self._parent_window = parent_window
        self._hwnd = 0
        if _is_windows():
            if hasattr(parent_window, 'winfo_id'):
                # tk window
                self._hwnd = parent_window.winfo_id()
            elif hasattr(parent_window, 'GetHandle'):
                # wx window
                self._hwnd = parent_window.GetHandle()
            elif hasattr(parent_window, 'window') and hasattr(parent_window.window, 'handle'):
                # gtk window
                self._hwnd = parent_window.window.handle
            elif parent_window is None:
                self._hwnd = 0
            else:
                self._hwnd = int(parent_window)
        twain_dll = _get_dsm(dsm_name)
        try:
            self._entry = twain_dll['DSM_Entry']
        except AttributeError as e:
            raise excSMGetProcAddressFailed(e)
        self._entry.restype = c_uint16
        self._entry.argtypes = (POINTER(TW_IDENTITY),
                                POINTER(TW_IDENTITY),
                                c_uint32,
                                c_uint16,
                                c_uint16,
                                c_void_p)
        
        self._app_id = TW_IDENTITY(Version=TW_VERSION(MajorNum=MajorNum,
                                                      MinorNum=MinorNum,
                                                      Language=Language,
                                                      Country=Country,
                                                      Info=Info.encode('utf8')),
                                   ProtocolMajor=ProtocolMajor,
                                   ProtocolMinor=ProtocolMinor,
                                   SupportedGroups=SupportedGroups | DF_APP2,
                                   Manufacturer=Manufacturer.encode('utf8'),
                                   ProductFamily=ProductFamily.encode('utf8'),
                                   ProductName=ProductName.encode('utf8'))
        self._call(None, DG_CONTROL, DAT_PARENT, MSG_OPENDSM, byref(c_void_p(self._hwnd)))
        self._version2 = bool(self._app_id.SupportedGroups & DF_DSM2)
        if self._version2:
            entrypoint = TW_ENTRYPOINT(Size=sizeof(TW_ENTRYPOINT))
            rv = self._entry(self._app_id,
                             None,
                             DG_CONTROL,
                             DAT_ENTRYPOINT,
                             MSG_GET,
                             byref(entrypoint))
            if rv != TWRC_SUCCESS:
                raise excSMOpenFailed("[%s], return code %d from DG_CONTROL DAT_ENTRYPOINT MSG_GET" % (dsm_name, rv))
            self._alloc = entrypoint.DSM_MemAllocate
            self._free = entrypoint.DSM_MemFree
            self._lock = entrypoint.DSM_MemLock
            self._unlock = entrypoint.DSM_MemUnlock
            self._encode = lambda s: s.encode('utf8')
            self._decode = lambda s: s.decode('utf8')
        else:
            self._alloc = _twain1_alloc
            self._free = _twain1_free
            self._lock = _twain1_lock
            self._unlock = _twain1_unlock
            self._encoding = sys.getfilesystemencoding()
            self._encode = lambda s: s.encode(self._encoding)
            self._decode = lambda s: s.decode(self._encoding)
            
        self._state = 'open'
        
    def __del__(self):
        if self._state == 'open':
            self._close_dsm()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _close_dsm(self):
        self._call(None,
                   DG_CONTROL,
                   DAT_PARENT,
                   MSG_CLOSEDSM,
                   byref(c_void_p(self._hwnd)))

    def close(self):
        """This method is used to force the SourceManager to close down.
        It is provided for finer control than letting garbage collection drop the connections.
        """
        while self._sources:
            self._sources.pop().close()
        if self._state == 'open':
            self._close_dsm()
            self._state = 'closed'

    def _call(self, dest_id, dg, dat, msg, buf, expected_returns=()):
        rv = self._entry(self._app_id, dest_id, dg, dat, msg, buf)
        if rv == TWRC_SUCCESS or rv in expected_returns:
            return rv
        elif rv == TWRC_FAILURE:
            status = TW_STATUS()
            rv = self._entry(self._app_id,
                             dest_id,
                             DG_CONTROL,
                             DAT_STATUS,
                             MSG_GET,
                             byref(status))
            if rv != TWRC_SUCCESS:
                raise Exception('DG_CONTROL DAT_STATUS MSG_GET returned non success code, rv = %d' % rv)
            code = status.ConditionCode
            exc = _exc_mapping.get(code,
                                   excTWCC_UNKNOWN("ConditionCode = %d" % code))
            raise exc
        else:
            raise Exception('Unexpected result: %d' % rv)
        
    def _user_select(self):
        ds_id = TW_IDENTITY()
        rv = self._call(None,
                        DG_CONTROL,
                        DAT_IDENTITY,
                        MSG_USERSELECT,
                        byref(ds_id),
                        (TWRC_SUCCESS, TWRC_CANCEL))
        if rv == TWRC_SUCCESS:
            return ds_id
        elif rv == TWRC_CANCEL:
            return None
        
    def _open_ds(self, ds_id):
        self._call(None,
                   DG_CONTROL,
                   DAT_IDENTITY,
                   MSG_OPENDS,
                   byref(ds_id))
        
    def _close_ds(self, ds_id):
        self._call(None,
                   DG_CONTROL,
                   DAT_IDENTITY,
                   MSG_CLOSEDS,
                   byref(ds_id))

    def open_source(self, product_name=None):
        """Open a TWAIN Source.

        Returns a :class:`Source` Object, which can be used to communicate with the source or None if user cancelled
        source selection dialog.

        :keyword product_name: source to be opened, if not specified or value is None user will be prompted for
                               source selection
        """
        if product_name:
            ds_id = TW_IDENTITY(ProductName=self._encode(product_name))
        else:
            ds_id = self._user_select()
            if not ds_id:
                return None
        self._open_ds(ds_id)
        source = Source(self, ds_id)
        self._sources.add(source)
        return source

    @property
    def identity(self):
        """This property is used to retrieve the identity of our application.
        The information is returned in a dictionary.
        """
        res = _struct2dict(self._app_id, self._decode)
        res.update(_struct2dict(self._app_id.Version, self._decode))
        return res

    @property
    def source_list(self):
        """Returns a list containing the names of the available source."""
        names = []
        ds_id = TW_IDENTITY()
        try:
            rv = self._call(None,
                            DG_CONTROL,
                            DAT_IDENTITY,
                            MSG_GETFIRST,
                            byref(ds_id),
                            (TWRC_SUCCESS, TWRC_ENDOFLIST))
        except excTWCC_NODS:
            # there are no data sources
            return names

        while rv != TWRC_ENDOFLIST:
            names.append(self._decode(ds_id.ProductName))
            rv = self._call(None,
                            DG_CONTROL,
                            DAT_IDENTITY,
                            MSG_GETNEXT,
                            byref(ds_id),
                            (TWRC_SUCCESS, TWRC_ENDOFLIST))
        return names
    
    def set_callback(self, cb):
        """Register a python function to be used for notification that the
        transfer is ready, etc.
        """
        self._cb = cb

    def is_twain2(self):
        return self._version2

    # backward compatible aliases
    def destroy(self):
        warnings.warn("destroy is deprecated, use close instead", DeprecationWarning)
        self.close()

    def SetCallback(self, cb):
        warnings.warn("SetCallback is deprecated, use set_callback instead", DeprecationWarning)
        return self.set_callback(cb)

    def OpenSource(self, product_name=None):
        warnings.warn("OpenSource is deprecated, use open_source instead", DeprecationWarning)
        return self.open_source(product_name)

    def GetIdentity(self):
        warnings.warn("GetIdentity is deprecated, use identity property instead", DeprecationWarning)
        return self.identity

    def GetSourceList(self):
        warnings.warn("GetSourceList is deprecated, use source_list property instead", DeprecationWarning)
        return self.source_list


def version():
    """Retrieve the version of the module"""
    return '2.0'


class BITMAPINFOHEADER(Structure):
    _pack_ = 4
    _fields_ = [('biSize', c_uint32),
                ('biWidth', c_long),
                ('biHeight', c_long),
                ('biPlanes', c_uint16),
                ('biBitCount', c_uint16),
                ('biCompression', c_uint32),
                ('biSizeImage', c_uint32),
                ('biXPelsPerMeter', c_long),
                ('biYPelsPerMeter', c_long),
                ('biClrUsed', c_uint32),
                ('biClrImportant', c_uint32)]


def _dib_write(handle, path, lock, unlock):
    file_header_size = 14
    ptr = lock(handle)
    try:
        char_ptr = cast(ptr, POINTER(c_char))
        bih = cast(ptr, POINTER(BITMAPINFOHEADER)).contents
        if bih.biCompression != 0:
            msg = 'Cannot handle compressed image. Compression Format %d' % bih.biCompression
            raise excImageFormat(msg)
        bits_offset = file_header_size + bih.biSize + bih.biClrUsed * 4
        if bih.biSizeImage == 0:
            row_bytes = (((bih.biWidth * bih.biBitCount) + 31) & ~31) / 8
            bih.biSizeImage = row_bytes * bih.biHeight
        dib_size = bih.biSize + bih.biClrUsed * 4 + bih.biSizeImage 
        file_size = dib_size + file_header_size

        def _write_bmp(f):
            import struct
            f.write(b'BM')
            f.write(struct.pack('LHHL', file_size, 0, 0, bits_offset))
            for i in range(dib_size):
                f.write(char_ptr[i])

        if path:
            f = open(path, 'wb')
            try:
                _write_bmp(f)
            finally:
                f.close()
        else:
            import io
            f = io.StringIO(file_size)
            try:
                _write_bmp(f)
                return f.getvalue()
            finally:
                f.close()
    finally:
        unlock(handle)

def dib_to_bm_file(handle, path=None):
    """Convert a DIB (Device Independent Bitmap) to a windows
    bitmap file format. The BitMap file is either returned as
    a string, or written to a file with the name given in the
    second argument.

    .. note::

        Can only be used with twain 1.x sources
    """
    return _dib_write(handle, path, _GlobalLock, _GlobalUnlock)


def dib_to_xbm_file(handle, path=None):
    """Convert a DIB (Device Independent Bitmap) to an X-Windows
    bitmap file (XBM format). The XBM file is either returned as
    a string, or written to a file with the name given in the
    third argument.
    Parameters:

    :param handle: Handle to a global area containing a DIB,
    :param path: Path prefix to be used for the name and an optional filename
        for file only output.

    .. note::

        Can only be used with twain 1.x sources
    """
    import tempfile
    import os
    handle, bmppath = tempfile.mkstemp('.bmp')
    os.close(handle)
    dib_to_bm_file(handle, bmppath)
    import Image
    Image.open(bmppath).save(path, 'xbm')
    os.remove(bmppath)


def global_handle_get_bytes(handle, offset, count):
    """Read a specified number of bytes from a global handle.

    Parameters:
    :param handle: Global handle
    :param offset: An index into the handle data
    :param count: The number of bytes to be returned

    .. note::

        Can only be used with twain 1.x sources
    """
    size = _GlobalSize(handle)
    ptr = _GlobalLock(handle)
    try:
        char_ptr = cast(ptr, POINTER(c_char))
        return char_ptr[min(offset, size) : min(offset + count, size)]
    finally:
        _GlobalUnlock(handle)


def global_handle_put_bytes(handle, offset, count, data):
    """Write a specified number of bytes to a global handle.

    Parameters:

    :param handle: Global handle
    :param offset: An index into the handle data
    :param count: The number of bytes to update
    :param data: String of data to be written

    .. note::

        Can only be used with twain 1.x sources
    """
    size = _GlobalSize(handle)
    ptr = _GlobalLock(handle)
    try:
        char_ptr = cast(ptr, POINTER(c_char))
        offset = min(offset, size)
        end = min(offset + count, size)
        count = end - offset
        count = min(count, len(data))
        for i in range(count):
            char_ptr[i + offset] = data[i]
    finally:
        _GlobalUnlock(handle)


def global_handle_allocate(flags, size):
    """Allocate a specified number of bytes via a global handle.

    Parameters:

    :param size: The number of bytes to be allocated

    .. note::

        Can only be used with twain 1.x sources
    """
    return _GlobalAlloc(flags, size)


def global_handle_free(handle):
    """Free an allocated heap section via the global handle.

    Parameters:

    :param handle: Handle to memory to be freed

    .. note::

        Can only be used with twain 1.x sources
    """
    return _GlobalFree(handle)


def acquire(path,
            ds_name=None,
            dpi=None,
            pixel_type=None,
            bpp=None,
            frame=None,
            parent_window=None,
            show_ui=False,
            dsm_name=None):
    """Acquires single image into file

    :param path: Path where to save image
    :keyword ds_name: name of twain data source, if not provided user will be presented with selection dialog
    :keyword dpi: resolution in dots per inch
    :keyword pixel_type: can be 'bw', 'gray', 'color'
    :keyword bpp: bits per pixel
    :keyword frame: tuple (left, top, right, bottom) scan area in inches
    :keyword parent_window: can be Tk, Wx, Gtk window object or Win32 window handle
    :keyword show_ui: if True source's UI dialog will be presented to user

    Returns a dictionary describing image, or None if scanning was cancelled by user

    """
    if pixel_type:
        pixel_type_map = {'bw': TWPT_BW,
                          'gray': TWPT_GRAY,
                          'color': TWPT_RGB}
        twain_pixel_type = pixel_type_map[pixel_type]
    if not parent_window:
        from tkinter import Tk
        parent_window = Tk()        
    sm = SourceManager(parent_window, dsm_name=dsm_name)
    try:
        sd = sm.open_source(ds_name)
        if not sd:
            return None
        try:
            if pixel_type:
                sd.set_capability(ICAP_PIXELTYPE, TWTY_UINT16, twain_pixel_type)
            sd.set_capability(ICAP_UNITS, TWTY_UINT16, TWUN_INCHES)
            if bpp:
                sd.set_capability(ICAP_BITDEPTH, TWTY_UINT16, bpp)
            if dpi:
                sd.set_capability(ICAP_XRESOLUTION, TWTY_FIX32, dpi)
                sd.set_capability(ICAP_YRESOLUTION, TWTY_FIX32, dpi)
            if frame:
                try:
                    sd.set_image_layout(frame)
                except CheckStatus:
                    pass
        
            res = []
            def before(img_info):
                res.append(img_info)
                return path
            
            def after(more):
                if more:
                    raise CancelAll
        
            try:
                sd.acquire_file(before=before, after=after, show_ui=show_ui)
            except excDSTransferCancelled:
                return None
        finally:
            sd.close()
    finally:
        sm.close()
    return res[0]


# backward compatible aliases
def DIBToBMFile(handle, path=None):
    """ Backward compatible alias for :func:`dib_to_bm_file` """
    warnings.warn("DIBToBMFile is deprecated, use dib_to_bm_file instead", DeprecationWarning)
    return dib_to_bm_file(handle, path)


def DIBToXBMFile(handle, path=None):
    """ Backward compatible alias for :func:`dib_to_xbm_file` """
    warnings.warn("DIBToXBMFile is deprecated, use dib_to_xbm_file instead", DeprecationWarning)
    return dib_to_xbm_file(handle, path)


def GlobalHandleGetBytes(handle, offset, count):
    """ Backward compatible alias for :func:`global_handle_get_bytes` """
    warnings.warn("GlobalHandleGetBytes is deprecated, use global_handle_get_bytes instead", DeprecationWarning)
    return global_handle_get_bytes(handle, offset, count)


def GlobalHandlePutBytes(handle, offset, count, data):
    """ Backward compatible alias for :func:`global_handle_put_bytes` """
    warnings.warn("GlobalHandlePutBytes is deprecated, use global_handle_put_bytes instead", DeprecationWarning)
    return global_handle_put_bytes(handle, offset, count, data)


def GlobalHandleAllocate(flags, size):
    """ Backward compatible alias for :func:`global_handle_allocate` """
    warnings.warn("GlobalHandleAllocate is deprecated, use global_handle_allocate instead", DeprecationWarning)
    return global_handle_allocate(flags, size)


def GlobalHandleFree(handle):
    """ Backward compatible alias for :func:`global_handle_free` """
    warnings.warn("GlobalHandleFree is deprecated, use global_handle_free instead", DeprecationWarning)
    return global_handle_free(handle)

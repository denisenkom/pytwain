.. pytwain documentation master file, created by
   sphinx-quickstart on Sat Jan 30 12:02:32 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pytwain's documentation!
===================================

Overview
========

The Python TWAIN module provides an interface to scanners,
digital cameras and other devices which implement TWAIN,
for Windows and Mac platforms.

It provides the functionality to allow a Python application to connect to the
scanner/camera and to retrieve images from that device.

If you use 64-bit Python on Windows you need to install 64 bit TWAIN DSM: http://sourceforge.net/projects/twain-dsm/.
Although there is a good chance that your scanner's driver is not compatible with 64-bit TWAIN DSM,
in this case you will get an empty list when you enumerate scanners.
If you have this issue try using 32-bit Python with TWAIN DSM supplied with Windows.

TWAIN specification can be found here: http://www.twain.org/scanner-application-developers/specification-and-tools.html

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


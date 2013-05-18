

from distutils.core import setup, Extension
setup(name='twain',
      version='2.0',
      author='Kevin Gill',
      author_email='kevin@movieextras.ie',
      maintainer='Mikhail Denisenko',
      maintainer_email='denisenkom@gmail.com',
      url='http://twainmodule.sourceforge.net',
      package_dir={'': 'src'},
      py_modules=['twain'],
      description="TWAIN API for accessing scanners, cameras, etc on Windows",
      long_description="""
The Python TWAIN module provides an interface to scanners, digital cameras and other devices which implement TWAIN, for the Windows platform. It provides the functionality to allow a Python application to connect to the scanner/camera and to retrieve images from that device.

The Python TWAIN module supports 32bit Windows only. It does not run on Apple Computer Platforms or on UNIX based Platforms. 
      """,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Win32 (MS Windows)',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
          'Topic :: Multimedia :: Graphics :: Capture :: Scanners',
          ],
      download_url='https://sourceforge.net/projects/twainmodule/files/',
      )

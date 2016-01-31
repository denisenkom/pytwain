from distutils.core import setup

setup(name='pytwain',
      version='2.0',
      author='Mikhail Denisenko',
      author_email='denisenkom@gmail.com',
      url='https://github.com/denisenkom/pytwain',
      package_dir={'': 'src'},
      py_modules=['twain'],
      description="TWAIN API for accessing scanners, cameras, etc on Windows",
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
      tests_require=['six'],
      )

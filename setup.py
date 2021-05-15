from setuptools import setup

setup(
    name='pyftpdlib_zipreaderfilesystem',
    description='pyftpdlib_zipreaderfilesystem',
    long_description=open("README.md").read(),
    version='0.0.0.1',
    url='https://github.com/cielavenir/pyftpdlib_zipreaderfilesystem',
    license='BSD',
    author='cielavenir',
    author_email='cielartisan@gmail.com',
    py_modules=['pyftpdlib_zipreaderfilesystem'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['pyftpdlib'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)

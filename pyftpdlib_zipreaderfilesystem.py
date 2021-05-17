from pyftpdlib.filesystems import AbstractedFS
from pyftpdlib.filesystems import FilesystemError
from os.path import join
from os.path import dirname
from os.path import basename
from os.path import normpath
from os import getuid
from os import getgid
from calendar import timegm
from zipfile import ZipFile

import sys
if sys.version_info[0]>=3:
    unicode = str

class ZipReaderFileSystem(AbstractedFS):
    '''
    usage: handler.abstracted_fs = ZipReaderFileSystem.withFilename(zipFileName)
    '''
    class ST:
        pass

    @classmethod
    def withFilename(cls, filename):
        def wrapper(fakeSelf, root, cmd_channel):
            return cls(root, cmd_channel, filename)
        return wrapper

    def __init__(self, root, cmd_channel, filename):
        AbstractedFS.__init__(self, root, cmd_channel)
        self.cwd = u'/'
        self.__zip = ZipFile(filename, 'r')

        self.__namelist = self.__zip.namelist()
        self.__dirnames = set(name.rstrip('/') for name in self.__namelist if name.endswith('/'))
        for name in self.__namelist:
            if name.endswith('/'):
                pass
            else:
                name+='/'
            while name!='/':
                name = dirname(dirname(name))+'/'
                if name.rstrip('/') not in self.__dirnames:
                    self.__dirnames.add(name.rstrip('/'))
                    self.__namelist.append(name)

    def stat(self, path):
        if path[0] == '/':
            path = path[1:]
        st=ZipReaderFileSystem.ST()
        if path in self.__dirnames:
            st.st_mode=0o755
            st.st_size=0
            st.st_mtime=0
        else:
            info = self.__zip.getinfo(path)
            st.st_mode=0o644
            st.st_size=info.file_size
            st.st_mtime=int(timegm(info.date_time))
        st.st_nlink = 1
        st.st_uid = getuid()
        st.st_gid = getgid()
        return st

    def lstat(self, path):
        return self.stat(path)

    def open(self, filename, mode):
        path = filename
        if path[0] == '/':
            path = path[1:]
        return self.__zip.open(path, mode.replace('b',''))

    def listdir(self, path):
        if path[0] == '/':
            path = path[1:]
        res = []
        for name in self.__namelist:
            if name.endswith('/'):
                if dirname(dirname(name))==path:
                    res.append(basename(dirname(name)))
            else:
                if dirname(name)==path:
                    res.append(basename(name))
        return res

    def ftp2fs(self, path):
        if path[0] == '/':
            pass #path = path[1:]
        else:
            path = join(self.cwd, path)
        return path

    def validpath(self, path):
        return True

    def isdir(self, path):
        if path[0] == '/':
            path = path[1:]
        return path in self.__dirnames

    def isfile(self, path):
        return not self.isdir(path)

    def chdir(self, path):
        if path[0]=='/':
            normpath(path+'/')
        else:
            path = normpath(join(self.cwd,path+'/'))
        if path[1:] not in self.__dirnames:
            raise FilesystemError('no such directory /%s'%path[1:])
        self.cwd = unicode(path)

if __name__ == '__main__':
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer
    from pyftpdlib.authorizers import DummyAuthorizer
    from os import environ
    from sys import argv
    authorizer = DummyAuthorizer()
    handler = FTPHandler
    handler.use_sendfile = False # required as the open() returns non-real-file
    handler.authorizer = authorizer
    authorizer.add_user(environ['USER'], '', '/', perm='elr')
    handler.abstracted_fs = ZipReaderFileSystem.withFilename(argv[1])
    server = FTPServer(('', 1121), handler)
    # press Ctrl+C to stop
    server.serve_forever()
    server.close_all()

from conans import ConanFile

class CsuTestConan(ConanFile):
    requires = 'llvm/3.3-7@vuo/stable'

    def imports(self):
        self.copy('*', dst='bin', src='bin')
        self.copy('*', dst='lib', src='lib')

    def build(self):
        self.run('bin/clang -nostartfiles ../../test_package.c -o test_package lib/crt1.o -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk')

    def test(self):
        self.run('./test_package')
        self.run('file lib/crt1.o')
        self.run('nm lib/crt1.o')

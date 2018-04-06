from conans import ConanFile

class CsuTestConan(ConanFile):
    requires = 'llvm/3.3-5@vuo/stable'
    generators = 'qbs'

    def imports(self):
        self.copy('*', dst='bin', src='bin')
        self.copy('*', dst='lib', src='lib')

    def build(self):
        self.run('bin/clang -nostartfiles ../../test_package.c -o test_package lib/crt1.o')

    def test(self):
        self.run('./test_package')
        self.run('file lib/crt1.o')
        self.run('nm lib/crt1.o')

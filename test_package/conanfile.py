from conans import ConanFile

class CsuTestConan(ConanFile):
    requires = (
        'llvm/5.0.2-1@vuo/stable',
        'macos-sdk/11.0-0@vuo/stable',
    )

    def imports(self):
        self.copy('*', dst='bin', src='bin')
        self.copy('*', dst='lib', src='lib')

    def build(self):
        self.run('bin/clang -nostartfiles ../../test_package.c -o test_package lib/crt1.o -isysroot %s' % self.deps_cpp_info['macos-sdk'].rootpath)

    def test(self):
        self.run('./test_package')
        self.run('file lib/crt1.o')
        self.run('nm lib/crt1.o')

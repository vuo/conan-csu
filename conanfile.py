from conans import ConanFile, tools
import shutil

class CsuConan(ConanFile):
    name = 'csu'

    csu_version = '88'
    package_version = '0'
    version = '%s-%s' % (csu_version, package_version)

    build_requires = (
        'llvm/5.0.2-1@vuo/stable',
        'macos-sdk/11.0-0@vuo/stable',
    )
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://opensource.apple.com/'
    license = 'https://opensource.apple.com/source/Csu/Csu-%s/crt.c.auto.html' % csu_version
    description = 'C runtime stubs'
    source_dir = 'Csu-%s' % csu_version

    def source(self):
        tools.get('http://www.opensource.apple.com/tarballs/Csu/Csu-%s.tar.gz' % self.csu_version,
                  sha256='b9bda91165d6c05c40fadbb622e70ace876c9a339d5101cd002644203d7b3409')

        with tools.chdir(self.source_dir):
            tools.replace_in_file('start.s',
                                  '#include <Availability.h>',
                                  '')

            # crt.c contains the license in the first block comment.
            # Truncate it at the end of that comment.
            self.run('sed "/\\*\\//q" crt.c > %s.txt' % self.name)

    def build(self):
        with tools.chdir(self.source_dir):
            env_vars = {
                'CC' : self.deps_cpp_info['llvm'].rootpath + '/bin/clang',
                'CXX': self.deps_cpp_info['llvm'].rootpath + '/bin/clang++',
                'RC_ARCHS': 'x86_64 arm64'
            }
            with tools.environment_append(env_vars):
                self.run('make crt1.v4.o')
            shutil.move('crt1.v4.o', 'crt1.o')

    def package(self):
        self.copy('crt1.o', src=self.source_dir, dst='lib')
        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')

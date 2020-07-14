from conans import ConanFile, tools
import shutil

class CsuConan(ConanFile):
    name = 'csu'

    csu_version = '85'
    package_version = '0'
    version = '%s-%s' % (csu_version, package_version)

    build_requires = 'llvm/3.3-7@vuo/stable'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://opensource.apple.com/'
    license = 'https://opensource.apple.com/source/Csu/Csu-%s/crt.c.auto.html' % csu_version
    description = 'C runtime helpers'
    source_dir = 'Csu-%s' % csu_version

    def source(self):
        tools.get('http://www.opensource.apple.com/tarballs/Csu/Csu-%s.tar.gz' % self.csu_version,
                  sha256='f2291d7548da854322acf194a875609bfae96c2481738cf6fd1d89eea9ae057a')

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
            }
            with tools.environment_append(env_vars):
                self.run('make crt1.v2.o')
            shutil.move('crt1.v2.o', 'crt1.o')

    def package(self):
        self.copy('crt1.o', src=self.source_dir, dst='lib')
        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')

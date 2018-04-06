from conans import ConanFile, tools
import shutil

class CsuConan(ConanFile):
    name = 'csu'

    csu_version = '79'
    package_version = '1'
    version = '%s-%s' % (csu_version, package_version)

    build_requires = 'llvm/3.3-5@vuo/stable'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://opensource.apple.com/'
    license = 'https://opensource.apple.com/source/Csu/Csu-%s/crt.c.auto.html' % csu_version
    description = 'Combines several object files and libraries, resolves references, and produces an ouput file'
    source_dir = 'Csu-%s' % csu_version

    def source(self):
        tools.get('http://www.opensource.apple.com/tarballs/Csu/Csu-%s.tar.gz' % self.csu_version,
                  sha256='d052e1daa1f5de7fc02e7e7cb8b79ee2eeaad0f321c0a70bea4fc7217e232ec2')

        # crt.c contains the license in the first block comment.
        # Truncate it at the end of that comment.
        self.run('sed "/\\*\\//q" %s/crt.c > %s/%s.txt' % (self.source_dir, self.source_dir, self.name))

    def build(self):
        with tools.chdir(self.source_dir):
            env_vars = {
                'CC' : self.deps_cpp_info['llvm'].rootpath + '/bin/clang',
                'CXX': self.deps_cpp_info['llvm'].rootpath + '/bin/clang++',
            }
            with tools.environment_append(env_vars):
                self.run('make')
            shutil.move('crt1.v3.o', 'crt1.o')

    def package(self):
        self.copy('crt1.o', src=self.source_dir, dst='lib')
        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')

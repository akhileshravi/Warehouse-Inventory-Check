#Copyright 2014-2016 MathWorks, Inc.

from distutils.core import setup
from distutils.command.build_py import build_py
import os
import sys
import platform

_supported_versions = ['2.7', '3.4', '3.5']
_ver = sys.version_info
_version = '{0}.{1}'.format(_ver[0], _ver[1])
if not _version in _supported_versions:
    raise EnvironmentError('MATLAB Engine for Python supports Python version'
                           ' 2.7, 3.4 and 3.5, but your version of Python '
                           'is %s' % _version)
_dist = "dist"
_matlab_package = "matlab"
_engine_package = "engine"
_arch_filename = "_arch.txt"
_py_arch=platform.architecture()
_py_bitness=_py_arch[0]

class BuildEngine(build_py):

    @staticmethod
    def _find_arch(predicate):
        _bin_dir = predicate
        _arch = None
        _archs = ["win64", "glnxa64", "maci64", "win32"]
        _arch_bitness = {"glnxa64": "64bit", "maci64": "64bit",
                         "win32": "32bit", "win64": "64bit"}
        for arch in _archs:
            if os.access(_bin_dir+arch, os.F_OK):
                _arch = arch
                break
        if _arch is None:
            raise EnvironmentError('The installation of MATLAB is corrupted.  '
                                   'Please reinstall MATLAB or contact '
                                   'Technical Support for assistance.')

        if _py_bitness != _arch_bitness[_arch]:
            raise EnvironmentError('%s Python does not work with %s MATLAB. '
                                   'Please check your version of Python' %
                                   (_py_bitness, _arch_bitness[_arch]))
        return _arch

    def _generate_arch_file(self, target_dir):
        _arch_file_path = target_dir+_arch_filename
        _cwd=os.getcwd()
        _bin_dir = _cwd+os.sep+os.pardir+os.sep+os.pardir+os.sep+os.pardir\
            + os.sep+"bin"+os.sep
        _engine_dir = _cwd+os.sep+_dist+os.sep+_matlab_package+os.sep\
            + _engine_package+os.sep
        _arch = self._find_arch(_bin_dir)
        _bin_dir += _arch
        _engine_dir += _arch
        try:
            _arch_file = open(_arch_file_path,'w')
            _arch_file.write(_arch+os.linesep)
            _arch_file.write(_bin_dir+os.linesep)
            _arch_file.write(_engine_dir+os.linesep)
            _arch_file.close()
        except IOError:
            raise EnvironmentError('You do not have write permission '
                                   'in %s ' % target_dir)

    def run(self):
        build_py.run(self)
        _target_dir = self.build_lib + os.sep + _matlab_package + os.sep + \
            _engine_package + os.sep
        self._generate_arch_file(_target_dir)


if __name__ == '__main__':

    setup(
        name="matlabengineforpython",
        version="R2017a",
        description='A module to call MATLAB from Python',
        author='MathWorks',
        url='http://www.mathworks.com/',
        platforms=['Linux', 'Windows', 'MacOS'],
        package_dir={'': 'dist'},
        packages=['matlab','matlab.engine','matlab._internal'],
        cmdclass={'build_py': BuildEngine}
    )

from pybuilder.core import use_plugin, init
from pybuilder.vcs import VCSRevision
import os

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")
use_plugin("copy_resources")
use_plugin("python.pycharm")

name = "cfn-signal-elb-healthcheck"
default_task = ['clean', 'publish']
version = VCSRevision().count

@init
def set_properties(project):
    project.build_depends_on('mock')
    project.depends_on('docopt')
    project.depends_on('botocore')
    project.depends_on('boto')

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').extend(['setup.cfg', 'rpm-*.sh', 'misc/*'])

    project.install_file('/etc/init/', 'misc/cfn-signal-elb-healthcheck.conf')

    project.set_property('verbose', True)
    project.rpm_release = os.environ.get('BUILD_NUMBER', 0)


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os
    project.set_property('teamcity_output', True)
    project.default_task = ['clean', 'install_build_dependencies', 'publish']
    project.set_property('install_dependencies_index_url', os.environ.get('PYPIPROXY_URL'))
    project.set_property('install_dependencies_use_mirrors', False)

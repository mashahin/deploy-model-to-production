from fabric.api import cd, run
from fabric.contrib.files import exists
from fabric.context_managers import prefix

# defaults
CONDA_REPO = 'http://repo.continuum.io/miniconda/'
CONDA_VERS = 'Miniconda2-3.19.0-Linux-x86_64.sh'


def install(conda_repo=CONDA_REPO, conda_vers=CONDA_VERS, home='~'):
    anaconda = home+'/anaconda'
    if not exists(anaconda):
        run('mkdir -p %s/downloads' % home)
        with cd(home+'/downloads'):
            run('wget -nv -N %s%s' % (conda_repo, conda_vers))
            run('bash %s -b -p %s' % (conda_vers, anaconda))


def create_env(environment_yml, home='~'):
    anaconda_bin = '%s/anaconda/bin' % home
    with cd(anaconda_bin):
        if exists(anaconda_bin):
            run('./conda env update -f %s' % environment_yml)
        else:
            run('./conda env create -f %s' % environment_yml)


def env(name, home='~'):
    """Run with an anaconda environment"""
    return prefix('source %s/anaconda/bin/activate %s' % (home, name))

from fabric.api import env, local, run, sudo
from fabric.operations import put
import anaconda

env.roledefs = {
    'prd': ['deploy@server1.example.com'],
}
APP_PATH = '/apps/mlapi'


def setup():
    # anaconda setup
    anaconda.install()
    run('mkdir -p %s/logs' % APP_PATH)
    put('deploy/mlapi.conf', '/etc/init/mlapi.conf', use_sudo=True)
    put('deploy/upstart_mlapi', '/etc/sudoers.d/mlapi', use_sudo=True)
    sudo('chown root:root /etc/init/mlapi.conf /etc/sudoers.d/mlapi')


def deploy():
    # ensure environment up to date
    put('environment.yml', APP_PATH)
    anaconda.create_env(APP_PATH+'/environment.yml')

    # install egg
    local('python setup.py bdist_wheel')
    wheel = 'mlapi-0.1.0-py2-none-any.whl'
    put('dist/'+wheel, APP_PATH)
    with anaconda.env('ml'):
        run('pip install -U %s/%s' % (APP_PATH, wheel))

    # deploy models
    put('models', APP_PATH)

    # restart gunicorn
    # stop, then start: ensure it succeeds first time
    run('sudo /usr/sbin/service mlapi stop; sudo /usr/sbin/service mlapi start')

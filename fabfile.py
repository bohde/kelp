from fabric.api import local, settings, abort, sudo, run, put, require, cd, env
from fabric.contrib.console import confirm

def production():
    "Set the variables for the production environment"
    env.fab_hosts=["jabc59@marconi.kmnr.org"]
    env.hosts = env.fab_hosts
    env.fab_user="jabc59"

def test():
    with settings(warn_only=True):
        result = local('./manage.py test program_log', capture=False)
        if result.failed and not confirm("Tests failed. Continue anyway?"):
            abort("Aborting at user request.")

def update_remote():
    with cd("/home/kelp/kelp"):
        sudo("su -c 'svn up' www-data")

def restart_database():
    with cd("/home/kelp/kelp"):
        sudo("su -c 'rm ../kelpdb' www-data")
        sudo("su -c './manage.py syncdb' www-data")
        sudo("su -c './manage.py loaddata fixtures/*' www-data)")         

def push_to_server():
    local("git checkout -f marconi_deploy")
    local("git merge master")
    local("git svn dcommit")
    local("git checkout master")

def restart_server():
    sudo("/usr/sbin/apache2ctl graceful")

def deploy():
    "Deploy the application by packaging a specific hash or tag from the git repo"
    # Make sure that the required variables are here
    require("fab_hosts", provided_by=[production])
    require("fab_user", provided_by=[production])

    test()
    push_to_server()
    update_remote()
    restart_server()

def remote_deploy():
    local('sudo vpnc')
    try:
        deploy()
    finally:
        local('sudo vpnc-disconnect')
    

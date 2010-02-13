"""
Fabfile to deploy to KMNR's Marconi server.
"""
from fabric.api import local, settings, abort, sudo, require, cd, env
from fabric.contrib.console import confirm


def production():
    "Set the variables for the production environment"
    env.fab_hosts = ["jabc59@marconi.kmnr.org"]
    env.hosts = env.fab_hosts
    env.fab_user = "jabc59"


def test():
    "Run the Djano tests."
    with settings(warn_only=True):
        result = local('./manage.py test program_log', capture=False)
        if result.failed and not confirm("Tests failed. Continue anyway?"):
            abort("Aborting at user request.")


def update_remote():
    "Update the remote from SVN."
    with cd("/home/kelp/kelp"):
        sudo("su -c 'svn up' www-data")

def local_db_restart():
    "Delete and rebuild database on the local"
    with settings(warn_only=True):
        local("rm kelpdb")
    local("python2.6 manage.py syncdb --noinput")
    local("python2.6  manage.py loaddata fixtures/*")

def restart_database():
    "Delete and rebuild the database on the remote"
    with cd("/home/kelp/kelp"):
        with settings(warn_only=True):
            sudo("su -c 'rm ../kelpdb' www-data")
        sudo("su -c 'python manage.py syncdb --noinput' www-data")
        sudo("su -c 'python manage.py loaddata fixtures/*' www-data)")


def push_to_server():
    "Merge into the marconi deploy branch."
    local("git checkout marconi_deploy")
    local("git merge master")
    local("git svn dcommit")
    local("git checkout master")


def restart_server():
    "Gracefully restart Apache."
    sudo("/usr/sbin/apache2ctl graceful")


def deploy():
    "Deploy the code to the server."
    require("fab_hosts", provided_by=[production])
    require("fab_user", provided_by=[production])

    test()
    push_to_server()
    update_remote()
    restart_server()


def remote_deploy():
    "Deploy when not on campus."
    with settings(warn_only=True):
        local('sudo vpnc')
    try:
        deploy()
    finally:
        with settings(warn_only=True):
            local('sudo vpnc-disconnect')

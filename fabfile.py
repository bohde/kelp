"""
Fabfile to deploy to KMNR's Marconi server.
"""
from fabric.api import local, settings, abort, sudo, require, cd, env, roles, run
from fabric.contrib.console import confirm
import os
import functools
import itertools

def production():
    "Set the variables for the production environment"
    env.fab_hosts = ["jabc59@marconi.kmnr.org"]
    env.hosts = env.fab_hosts
    env.fab_user = "jabc59"

def hms():
    "Setup the environment for hms_beatdown"
    env.roledefs = {
        "web":["django@10.138"],
        "sudo":["joshbohde@10.138"],
    }
    env.roles = ["web", "sudo"]
    env.web_root = "/home/django"
    env.code_root = os.path.join(env.web_root, "kelp")

def remote():
    "Setup the environment for remote hms_beatdown"
    env.roledefs = {
        "web":["django@git.joshbohde.com"],
        "sudo":["joshbohde@git.joshbohde.com"],
    }
    env.roles = ["web", "sudo"]
    env.web_root = "/home/django"
    env.code_root = os.path.join(env.web_root, "kelp")


def only_these_roles(*roles_list):
    role_set = set(roles_list)
    def func_wrapper(f):
        f = roles(*roles_list)(f)
        @functools.wraps(f)
        def inner(*args, **kwargs):
            s = set(itertools.chain(*[x for k,x in env.roledefs.iteritems() if k in role_set]))
            if env.host_string not in s:
                return None
            else:
                return f(*args, **kwargs)
        return inner
    return func_wrapper

@only_these_roles("web")    
def git_update():
    "Update the remote from git."
    with cd(env.code_root):
        run("git pull")

@only_these_roles("web")
def remote_test():
    "Test the app on the remote server"
    with cd(env.code_root):
        with settings(warn_only=True):
            result = run("./manage.py test program_log")
            if result.failed and not confirm("Remote tests failed. Continue anyway?"):
                abort("Aborting at user request.")

@only_these_roles("sudo")
def remote_refresh():
    sudo("pkill -HUP supervisor")

def home_deploy():
    test()
    git_update()
    remote_test()
    remote_refresh()

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

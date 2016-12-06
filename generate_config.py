#!/usr/bin/env python
import os
import argparse
import sys
import getpass


def main():
    args = parse_args()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", args.django_settings_module)
    try:
        from django.conf import settings
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )



    project_name = settings.ROOT_URLCONF.split('.')[0]
    project_path = settings.BASE_DIR

    virtualenv = 'home = {}'.format(args.virtualenv) if args.virtualenv else '#home = <your_venv_path>'
    server_name = 'server_name {};'.format(args.server_name) if args.server_name else '#server_name <your_server_name>;'
    uwsgi_user = args.owner_user if args.owner_user else getpass.getuser()

    uwsgi_ini_templ = open('uwsgi_template.ini', 'r').read()
    uwsgi_ini = uwsgi_ini_templ.format(
        project_name=project_name,
        project_path=project_path,
        virtualenv=virtualenv,
        user=uwsgi_user
    )
    with open('{}_uwsgi.ini'.format(project_name), 'w') as f:
        f.write(uwsgi_ini)

    nginx_templ = open('nginx_template.conf', 'r').read()
    nginx = nginx_templ.format(
        project_name=project_name,
        project_path=project_path,
        server_name=server_name,
        static_url=settings.STATIC_URL,
        static_root=settings.STATIC_ROOT + '/'
    )
    with open('{}_nginx.conf'.format(project_name), 'w') as f:
        f.write(nginx)



def parse_args():
    parser = argparse.ArgumentParser(description="move this file and relatated to him into "
                                                 "your django project directory, near manage.py and run. "
                                                 "It will generate files: p_uwsgi.ini and p_nginx.conf "
                                                 "where p - projectname. \n"
                                                 "usage example:\n"
                                                 "python {} myproject.settings -v /home/user1/envs/myproject"
                                                 " -s example.com".format(sys.argv[0]))
    parser.add_argument("django_settings_module", help="for ex.: myproject.settings")
    parser.add_argument("-v", "--virtualenv", help="absolute path to project virtualenv", default=None)
    parser.add_argument("-s", "--server_name", help="server ip or FQDN, which will be used in nginx", default=None)
    parser.add_argument("-u", "--owner_user", help="user under who uwsgi will start. default: current user", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    main()

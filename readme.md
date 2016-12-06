####Copy files from here into your django project
```bash
cp * /<fullpath_to_project>/
cd /<fullpath_to_project>/
```

####Install packages for ubuntu server
```bash
apt install uwsgi uwsgi-plugin-python3 nginx nginx-full
```

####Enable nginx.service
```bash
systemctl enable nginx.service
```

#### Install uwsgi emperor
```bash
mkdir -p /etc/uwsgi/vassals
cp ./emperor.ini /etc/uwsgi/
cp ./emperor.uwsgi.service /etc/systemd/system/
systemctl enable emperor.uwsgi.service
```


#### Generate configuration for project
```bash
python generate_config.py <django_settings_module> -v <path_to_virtualenv> -s <server_name>
```
example:
```bash
python generate_config.py myproj.settings -v /home/user/envs/myproj -s myproj.com
```
type `python generate_config.py -h` for help



#### Link generated configuration to uwsgi and nginx
```bash
ln -s /<fullpath_to_project>/*uwsgi.ini /etc/uwsgi/vassals/
ln -s /<fullpath_to_project>/*nginx.conf /etc/nginx/sites-enabled/
```

ensure you deleted default nginx server:
```bash
rm /etc/nginx/sites-enabled/default
```

#### Start services
```bash
systemctl start emperor.uwsgi.service
systemctl restart nginx.service
```


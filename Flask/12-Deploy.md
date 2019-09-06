```shell
export FLASK_APP=run.py
flask run --host=0.0.0.0
```



```shell
sudo apt install nginx
pip install gunicorn
```



```shell
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-enabled/flaskblog

server{
	listen 80;
	server_name ipaddress;
	
	location /static {
		alias /home/username/Flask_Blog/flaskblog/static;
	}
	
	location / {
		proxy_pass http://localhost:8000;
		include /etc/nginx/proxy_params;
		proxy_redirect off;
	}
}
```





```shell
sudo ufw allow http/tcp
sudo ufw delete allow 5000
sudo ufw enable
```



```shell
sudo systemclt restart nginx
```



### Get gunicorn working

```shell
gunicorn -m 3 run:app
```

- -w 3 : number of workers ( 2 * number of cores + 1)

- run : name of file

- app: name of variable



### Supervisor

force gunicorn to restart when crashed

```shell
sudo apt install supervisor
sudo nano /etc/supervisor/conf.d/flaskblog.conf

[program:flaskblog]
directory=/home/username/Flask_Blog
command=/home/username/Flash_Blog/venv/bin/gunicorn -w 3 run:app
user=username
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
sdterr_logfile=/var/log/flaskblog/flaskblog.err.log
sdtout_logfile=/var/log/flaskblog/flaskblog.out.log

sudo mkdir -p /var/log/flaskblog
sudo touch /var/log/flaskblog/flaskblog.err.log
sudo touch /var/log/flaskblog/flaskblog.out.log

sudo supervisorctl reload
```





### nginx

files too big

```shell
sudo nano /etc/nginx/nginx.conf

client_max_body_size 5M;
```





### test

```shell
sudo nginx -t
```


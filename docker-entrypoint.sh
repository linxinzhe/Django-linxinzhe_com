/www/manage.py makemigrations --noinput
/www/manage.py migrate --noinput
/usr/local/bin/gunicorn linxinzhe_com.wsgi:application -w 2 -b :8000
sudo service nginx restart
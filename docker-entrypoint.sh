sleep 5
nginx
python3 /www/manage.py collectstatic --noinput
python3 /www/manage.py makemigrations --noinput
python3 /www/manage.py migrate --noinput
/usr/local/bin/gunicorn linxinzhe_com.wsgi:application -w 2 -b :8000

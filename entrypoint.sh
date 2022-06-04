# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
#gunicorn project.wsgi:application --bind 0.0.0.0:8000
gunicorn project.wsgi:application --bind 0.0.0.0:8000


#DJANGO_SUPERUSER_PASSWORD=abriev4453 python manage.py createsuperuser     --no-input     --username=abriev     --email=my_user@domain.com

#/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
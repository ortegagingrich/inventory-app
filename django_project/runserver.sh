#first get local ip address
INET_ADDR=`/sbin/ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'`
PORT='8000'

python manage.py runserver $INET_ADDR:$PORT

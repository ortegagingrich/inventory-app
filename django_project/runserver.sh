#first get local ip address
if [ "$1" != "local" ]; then 
	INET_ADDR=`/sbin/ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'`
else
	INET_ADDR="127.0.0.1"
fi

PORT='8000'

{
	python manage.py runserver $INET_ADDR:$PORT
} || {
	echo "Cannot start server; not connected to eth0."
}

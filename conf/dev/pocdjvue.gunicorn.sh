#!/bin/bash
set -e

APP_NAME=pocdjvue

# user/group to run as
USER=ubuntu
GROUP=ubuntu

LOGFILE=/home/$USER/poc/log/pocdjvue.gunicorn.log
LOGDIR=$(dirname $LOGFILE)

cd /home/$USER/poc/$APP_NAME
test -d $LOGDIR || mkdir -p $LOGDIR

source /home/ubuntu/.virtualenvs/pocdjvue/bin/activate

export DJANGO_SETTINGS_MODULE="pocdjvue.settings"
export DJANGO_WSGI_MODULE="pocdjvue.wsgi"

gunicorn ${DJANGO_WSGI_MODULE}:application --config /home/$USER/poc/$APP_NAME/conf/dev/pocdjvue.gunicorn.conf.py \
--user=$USER --group=$GROUP --log-level=error --reload --log-file=$LOGFILE 2>>$LOGFILE

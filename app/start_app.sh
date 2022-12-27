#!/bin/bash

if [ "$1" == 'api' ]; then
    echo "Launching Web Application"
    python3 main.py
elif  [ "$1" == 'flower' ]; then
    echo "Launching Flower Service"
    celery --broker=${REDIS_URI}// flower --address=0.0.0.0
elif [ "$1" == 'workers' ]; then
  # celery -A celery_task.most_wanted.ice worker --concurrency=1 --pool=gevent --loglevel=info -Q ice_queue -n ice_worker_%n &
  # celery -A celery_task.most_wanted.dea worker --concurrency=1 --pool=gevent --loglevel=info -Q dea_queue -n dea_worker_%n &
  # celery -A celery_task.most_wanted.fbi worker --concurrency=1 --pool=gevent --loglevel=info -Q fbi_queue -n fbi_worker_%n &
  # celery -A celery_task.most_wanted.interpol worker --concurrency=1 --pool=gevent --loglevel=info -Q interpol_queue -n interpol_worker_%n &
  celery -A celery_task.generate_tasks worker --concurrency=25 --pool=gevent --loglevel=info -n sdk_worker
else
  python3 main.py &
  celery -A celery_task.generate_tasks worker --concurrency=25 --pool=gevent --loglevel=info -n sdk_worker &
  celery --broker=${REDIS_URI}// flower --address=0.0.0.0
fi

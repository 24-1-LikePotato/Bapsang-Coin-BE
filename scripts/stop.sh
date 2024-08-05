#!/bin/bash

# uWSGI 프로세스 ID를 찾기
uwsgi_pids=$(ps -ef | grep '[u]wsgi' | grep -- '--ini uwsgi.ini' | awk '{print $2}')

# 프로세스 ID가 있으면 종료
if [ -n "$uwsgi_pids" ]; then
    echo "Stopping uWSGI processes with PIDs: $uwsgi_pids"
    kill $uwsgi_pids
    echo "uWSGI processes stopped."
else
    echo "No uWSGI processes found."
fi

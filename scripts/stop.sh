#!/bin/bash

# uWSGI 프로세스 ID를 찾기 (전체 경로 포함)
uwsgi_pids=$(ps -ef | grep '[/]home/ubuntu/Zipbab-Coin-BE/Zipbab/venv/bin/uwsgi --ini uwsgi.ini' | awk '{print $2}')

# 프로세스 ID가 있으면 종료
if [ -n "$uwsgi_pids" ]; then
    echo "Stopping uWSGI processes with PIDs: $uwsgi_pids"
    kill -9 $uwsgi_pids
    echo "uWSGI processes stopped."
else
    echo "No uWSGI processes found."
fi

# 추가적으로 남아있는 uWSGI 프로세스 확인 및 종료
remaining_pids=$(pgrep -f "uwsgi --ini uwsgi.ini")
if [ -n "$remaining_pids" ]; then
    echo "Found remaining uWSGI processes. Stopping them with PIDs: $remaining_pids"
    kill -9 $remaining_pids
    echo "Remaining uWSGI processes stopped."
fi

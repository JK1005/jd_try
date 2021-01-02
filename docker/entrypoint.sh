#!/bin/bash
set -e

echo "" | crontab -
crond

if [ -f ${SCRIPTS_DIR}/config/config.yml ]
then
  echo "开始添加定时任务..."
  cd ${SCRIPTS_DIR}
  python3 setup.py
  echo "添加定时任务完成..."
else
  echo "请先配置好config.yml..."
  exit 1
fi

if [ "${1#-}" != "${1}" ] || [ -z "$(command -v "${1}")" ]; then
  set -- python3 "$@"
fi

exec "$@"
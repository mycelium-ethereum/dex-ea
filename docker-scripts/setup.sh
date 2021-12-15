# !/usr/bin/env bash

printenv | grep -v "no_proxy" >> /etc/environment
cron
tail -F /var/log/cron.log
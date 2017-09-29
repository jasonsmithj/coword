#!/bin/sh

/sbin/service sshd start
/sbin/service ntpd start

while true
do
  sleep 10
done

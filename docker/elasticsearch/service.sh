#!/bin/sh

/sbin/service sshd start
/sbin/service ntpd start
/sbin/service elasticsearch start
/sbin/service kibana start

while true
do
  sleep 10
done

FROM amazonlinux:latest

MAINTAINER coword_devteam

# Install Package
RUN yum clean all
RUN yum -y install gcc gcc-c++ pcre-devel zlib-devel openssl-devel readline-devel libxml2-devel libsxlt-devel tar postgresql-devel git cmake passwd vi mysql mysql-devel telnet tar patch sudo openssh-server | true
RUN yum -y install java-1.8.0-openjdk-devel | true

# Install ElasticSearch
RUN yum install -y https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.2.rpm
RUN yum install -y https://artifacts.elastic.co/downloads/kibana/kibana-5.5.2-x86_64.rpm

COPY elasticsearch.yml /etc/elasticsearch/elasticsearch.yml
COPY kibana.yml /etc/kibana/kibana.yml

# Install kuromoji
COPY ./elasticsearch /etc/sysconfig/elasticsearch
COPY ./elasticsearch.sh /etc/profile.d/elasticsearch.sh
RUN export JAVA_HOME=/usr/lib/jvm/java ; /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-kuromoji

# Create coword user
RUN passwd -d root
RUN useradd -u 501 coword
RUN passwd -d coword
RUN sed -ri 's/^wheel:x:10:/wheel:x:10:coword/' /etc/group
RUN sed -ri 's/^# %wheel/coword/' /etc/sudoers

COPY ./.vimrc /root/
COPY ./.vimrc /home/coword/
RUN chown coword:coword /home/coword/.vimrc

# Service Setup
ADD ./network /etc/sysconfig/

# Service Setup
COPY ./service.sh /root/
RUN chmod 744 /root/service.sh

# Port to expose *outside* the container
EXPOSE 80
EXPOSE 9200

# Service to run
CMD ["/root/service.sh"]

# Clean up
RUN yum clean all
RUN rm -rf /tmp/*
RUN rm -rf /var/tmp/*

# Set Time Zone
RUN echo -e 'ZONE="Asia/Tokyo"\nUTC=false' > /etc/sysconfig/clock
RUN ln -sf  /usr/share/zoneinfo/Asia/Tokyo /etc/localtime


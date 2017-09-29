FROM amazonlinux:latest

MAINTAINER devteam

# Install Package
RUN yum clean all
RUN yum -y install gcc gcc-c++ pcre-devel zlib-devel openssl-devel readline-devel libxml2-devel libsxlt-devel tar git cmake passwd vi telnet tar patch sudo openssh-server which wget diffutils file | true

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

# Create Directory
RUN mkdir -m 755 -p /var/www
RUN chown coword:coword -R /var/www

# Install python
COPY ./python.sh /etc/profile.d/
RUN chmod 755 /etc/profile.d/python.sh
RUN source /etc/profile.d/python.sh; git clone https://github.com/yyuu/pyenv ${PYENV_ROOT}
RUN source /etc/profile.d/python.sh; pyenv install 3.6.2
RUN source /etc/profile.d/python.sh; pyenv global 3.6.2
RUN source /etc/profile.d/python.sh; pyenv rehash
RUN source /etc/profile.d/python.sh; pip install pip-tools
RUN chown coword:coword -R /usr/local/pyenv
RUN wget -O /usr/local/bin/direnv "https://github.com/direnv/direnv/releases/download/v2.12.2/direnv.linux-amd64"
RUN chmod +x /usr/local/bin/direnv

RUN echo 'export EDITOR="vi"' >> /home/coword/.bashrc
RUN echo 'eval "$(direnv hook bash)"' >> /home/coword/.bashrc
RUN echo 'show_virtual_env() {' >> /home/coword/.bashrc
RUN echo '  if [ -n "$VIRTUAL_ENV" ]; then' >> /home/coword/.bashrc
RUN echo '    echo "($(basename $VIRTUAL_ENV))"' >> /home/coword/.bashrc
RUN echo '  fi' >> /home/coword/.bashrc
RUN echo '}' >> /home/coword/.bashrc
RUN echo 'PS1='$(show_virtual_env)'$PS1' >> /home/coword/.bashrc

# Install Mecab
RUN wget -O /tmp/mecab-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE"
RUN cd /tmp/ && \
    tar zvfx mecab-0.996.tar.gz
RUN cd /tmp/mecab-0.996 && \
    ./configure --with-charset=utf8 --enable-utf8-only && \
    make && \
    make install
COPY ./es.conf /etc/ld.so.conf.d/es.conf
RUN ldconfig

RUN wget -O /tmp/mecab-ipadic-2.7.0-20070801.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM"
RUN cd /tmp/ && \
    tar zvfx mecab-ipadic-2.7.0-20070801.tar.gz
RUN cd /tmp/mecab-ipadic-2.7.0-20070801 && \
    ./configure --with-charset=utf8 && \
    make && \
    make install

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /tmp/mecab-ipadic-neologd
RUN cd /tmp/mecab-ipadic-neologd && \
    ./bin/install-mecab-ipadic-neologd -n -y

# Service Setup
COPY ./service.sh /root/
RUN chmod 744 /root/service.sh

# Port to expose *outside* the container
EXPOSE 80

# Service to run
CMD ["/root/service.sh"]

# Clean up
RUN yum clean all
RUN rm -rf /tmp/*
RUN rm -rf /var/tmp/*

# Set Time Zone
RUN echo -e 'ZONE="Asia/Tokyo"\nUTC=false' > /etc/sysconfig/clock
RUN ln -sf  /usr/share/zoneinfo/Asia/Tokyo /etc/localtime


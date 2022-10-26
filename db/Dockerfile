FROM postgres:15

RUN localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8

COPY ./shell /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/initdb.sh
COPY ./sql /docker-entrypoint-initdb.d/

USER postgres
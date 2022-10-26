#!/usr/bin/env bash

psql=( psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --no-password )
find /docker-entrypoint-initdb.d -type f -not -path */02_develop/* -not -path */02_verify/* -not -path */02_production/* | sort | while read f; do
  case "$f" in
    *.sql)    echo "$0: running $f"; "${psql[@]}" -f "$f"; echo ;;
    *.sql.gz) echo "$0: running $f"; gunzip -c "$f" | "${psql[@]}"; echo ;;
    *)        echo "$0: ignoring $f" ;;
  esac
  echo
done
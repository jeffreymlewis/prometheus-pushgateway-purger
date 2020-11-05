FROM python:3.9

WORKDIR /usr/src/app

COPY ./prometheus_pushgateway_purger/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./prometheus_pushgateway_purger/prometheus_pushgateway_purger.py ./

# ENV variables must be set by docker-compose or Kubernetes
CMD ["sh", "-c", "./prometheus_pushgateway_purger.py --url=$PROMETHEUS_PG_URL --older-than=${PROMETHEUS_PG_OLDER_THAN:-300} ${DRY_RUN:+--dry-run}"]

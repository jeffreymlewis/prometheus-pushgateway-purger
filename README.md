# prometheus-pushgateway-purger
A simple script to purge metrics from the given [prometheus pushgateway](https://github.com/prometheus/pushgateway) after X minutes.

## Making Changes
When updating this script, be sure to increment the `VERSION` global at the top. Then push your changes and tag the repo using the same version number.

## Testing
For testing I recommend passing setting `DRY_RUN=true` as shown below, otherwise your test **can and will** delete data from your prometheus pushgateway.

To test, do the following.
```
# If you're pushgateway is running in Kubernetes, you can setup port forwarding
kubectl -n kube-system port-forward deploy/prometheus-pushgateway 9091:9091

# build & run
TAG=test docker-compose build prometheus-pushgateway-purger
TAG=test docker-compose run -e DRY_RUN=true prometheus-pushgateway-purger

# test with different --older-than time
TAG=test docker-compose run -e DRY_RUN=true -e PROMETHEUS_PG_OLDER_THAN=600 prometheus-pushgateway-purger
```

## Environment Variables
The following environment variables are supported by this container.
| Variable | Type | Description |
| --- | --- | --- |
| PROMETHEUS_PG_URL | string | REQUIRED url for the prometheus pushgateway (ex. http://localhost:9091) |
| PROMETHEUS_PG_OLDER_THAN | int | Purge Grouping Keys older then X seconds (default: 300) |
| DRY_RUN | string | If set to anything, print Job IDs but do not delete |

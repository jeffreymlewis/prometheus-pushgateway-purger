#!/usr/bin/env python3
"""Purge Grouping Keys (jobs) from Prometheus Pushgateway if they haven't been pushed to for X seconds.

Usage:
    prometheus_pushgateway_purger.py [options] --url=URL [--older-than=SECONDS]

Options:
  --url=URL  Prometheus Pushgateway URL (ie, http://localhost:9091)
  --older-than=SECONDS  Purge Grouping Keys older then X seconds [default: 300]
  --dry-run  List Grouping Keys (jobs) to purge
  --help     Show this screen
  --version  Show version and exit

"""
import pprint
import sys
import time

import docopt  # pylint: disable=import-error
import requests  # pylint: disable=import-error

VERSION = "0.0.3"


def get_jobs_data(url):
  """Return a dictionary containing data from all Grouping Keys on the given Prometheus Pushgateway.
  Input:
    url: (string) URL for Prometheus Pushgateway (ie, http://localhost:9091)
  Output:
    (dictionary) All metric data from the Prometheus Pushgateway
  """
  response = requests.get(url + "/api/v1/metrics")
  jobs = response.json()
  return jobs


def get_purgable_jobs(jobs, older_than):
  """Return list of Grouping Keys with `push_time_seconds` older than specified age.
  Input:
    jobs: (dictionary) output from Prometheus Pushgateway /api/v1/metrics endpoint
    older_than: (float) seconds
  Output:
    (list) List of pushgateway Job IDs
  """
  purgable = []
  for job in jobs['data']:
    last_push = job['push_time_seconds']['metrics'][0]['value']
    # If last push is too old, return the Grouping Key's unique label
    if float(last_push) + float(older_than) < time.time():
      purgable.append(job['labels']['job'])
  return purgable


def purge_jobs_by_id(url, job_ids):
  """Purge jobs_ids from given Prometheus Pushgateway.
  Input:
    url: (string) URL for Prometheus Pushgateway (ie, http://localhost:9091)
    job_ids: (list) List of pushgateway Job IDs
  Output:
    (int) number of pushgateway jobs deleted
  """
  count = 0
  for job in job_ids:
    requests.delete(url + '/metrics/job/%s' % job)
    count += 1
  return count


def main(args):
  """Delete Grouping Keys (jobs) not pushed to in X minutes."""
  all_jobs_data = get_jobs_data(url=args['--url'])
  purgable_job_ids = get_purgable_jobs(jobs=all_jobs_data, older_than=args['--older-than'])

  if args['--dry-run']:
    sys.exit(pprint.pprint(purgable_job_ids))

  number_purged = purge_jobs_by_id(url=args['--url'], job_ids=purgable_job_ids)
  print("%d jobs purged: %s" % (number_purged, purgable_job_ids))


if __name__ == '__main__':
  sys.exit(main(docopt.docopt(__doc__, version=VERSION)))

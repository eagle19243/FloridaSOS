#!/usr/bin/env bash
# Initialize options for gunicorn
OPTS=(
  --env FLASK_APP=florida_sos
  --env FLASK_ENV=development
  --env FLORIDA_SOS_CONF=conf.yml
  --access-logfile -
  --error-logfile -
  --log-level debug
  --timeout 108000
  -b 0.0.0.0:8093
  --reload
)

#Run gunicorn
gunicorn "${OPTS[@]}" florida_sos.application:APP

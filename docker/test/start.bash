#!/bin/bash

set -e

cd /api || exit

start=$(date +%s)

pip_start=$(date +%s)
procs=$(wc -l requirements.txt | awk '{print $1}')
max_attempts=5
attempt=1
while (( attempt <= max_attempts )); do
  xargs --max-args=1 --max-procs="$procs" --exit pip install \
    --no-input --progress-bar off --root-user-action ignore \
    --no-cache-dir --disable-pip-version-check --no-clean --prefer-binary \
    < requirements.txt
  # shellcheck disable=SC2181
  if [[ $? -eq 0 ]]; then
    break
  fi
  ((attempt++))
  sleep 1
done
if (( attempt > max_attempts )); then
  exit 1
fi
pip_end=$(date +%s)
echo "pip install took $(( pip_end - pip_start )) seconds"

test_start=$(date +%s)
coverage run manage.py test --noinput
coverage_end=$(date +%s)
echo "test took $(( coverage_end - test_start )) seconds"

report_start=$(date +%s)
coverage report
report_end=$(date +%s)
echo "coverage report took $(( report_end - report_start )) seconds"

xml_start=$(date +%s)
coverage xml -o /api/coverages/coverage.xml
xml_end=$(date +%s)
echo "coverage xml took $(( xml_end - xml_start )) seconds"

end=$(date +%s)
echo "Total execution time: $(( end - start )) seconds"

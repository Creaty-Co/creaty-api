#!/bin/bash

set -e

cd /api || exit

start=$(date +%s)

pip_start=$(date +%s)
procs=$(wc -l requirements.txt | awk '{print $1}')
pip install --upgrade pip
xargs -t -n2 -P20 pip download -d ./dist < requirements.txt
pip install \
  --no-input --progress-bar off --root-user-action ignore \
  --no-cache-dir --disable-pip-version-check --no-clean --prefer-binary \
  --no-index --find-links=./dist \
  -r requirements.txt
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

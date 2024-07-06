#!/bin/bash

set -e

cd /api || exit

start=$(date +%s)

pip_download_start=$(date +%s%3N)
xargs -t -n15 -P100 pip download -d ./dist \
  --progress-bar off --disable-pip-version-check --no-clean --prefer-binary -q \
  < requirements.txt
pip_download_end=$(date +%s%3N)
echo "pip download took $(( pip_download_end - pip_download_start )) milliseconds"

pip_install_start=$(date +%s%3N)
pip install \
  --progress-bar off --root-user-action ignore \
  --no-cache-dir --disable-pip-version-check --no-clean --prefer-binary \
  --no-index --find-links=./dist \
  -r requirements.txt
pip_install_end=$(date +%s%3N)
echo "pip install took $(( pip_install_end - pip_install_start )) milliseconds"

test_start=$(date +%s%3N)
coverage run manage.py test --noinput
coverage_end=$(date +%s%3N)
echo "test took $(( coverage_end - test_start )) milliseconds"

report_start=$(date +%s%3N)
coverage report
report_end=$(date +%s%3N)
echo "coverage report took $(( report_end - report_start )) milliseconds"

xml_start=$(date +%s%3N)
coverage xml -o /api/coverages/coverage.xml
xml_end=$(date +%s%3N)
echo "coverage xml took $(( xml_end - xml_start )) milliseconds"

end=$(date +%s)
echo "Total execution time: $(( end - start )) seconds"

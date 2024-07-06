#!/bin/bash

set -e

cd /api || exit

start=$(date +%s)

# Файл requirements.txt должен находиться в текущей директории
REQUIREMENTS_FILE="requirements.txt"
# Директория для скачивания пакетов
DOWNLOAD_DIR="./dist"
# Количество параллельных процессов
NUM_PROCESSES=1000
# Файл для временного хранения результатов
RESULTS_FILE="results.txt"

# Убедитесь, что директория для скачивания существует
mkdir -p "$DOWNLOAD_DIR"
# Очистите файл с результатами
echo "" > "$RESULTS_FILE"

# Функция для выполнения команды и замера времени
run_pip_download() {
    local n=$1
    rm -rf ./dist
    pip_download_start=$(date +%s%3N)
    xargs -n"$n" -P"$NUM_PROCESSES" pip download -d "$DOWNLOAD_DIR" \
        --progress-bar off --disable-pip-version-check --no-clean --prefer-binary -q \
        < "$REQUIREMENTS_FILE"
    pip_download_end=$(date +%s%3N)
    duration=$(( pip_download_end - pip_download_start ))
    echo "$n $duration" >> "$RESULTS_FILE"
}

# Прогоняем команду для всех значений n
for n in $(seq 1 15); do
    run_pip_download "$n"
done

# Сортируем результаты и выводим топ-результаты
echo "Top execution times:"
sort -nk2 "$RESULTS_FILE" | head -n 10 | while read -r line; do
    n=$(echo "$line" | awk '{print $1}')
    duration=$(echo "$line" | awk '{print $2}')
    echo "n=$n: $duration milliseconds"
done

#pip_download_start=$(date +%s%3N)
#xargs -n10 -P100 pip download -d ./dist \
#  --progress-bar off --disable-pip-version-check --no-clean --prefer-binary -q \
#  < requirements.txt
#pip_download_end=$(date +%s%3N)
#echo "pip download took $(( pip_download_end - pip_download_start )) milliseconds"

#pip_install_start=$(date +%s)
#pip install \
#  --progress-bar off --root-user-action ignore \
#  --no-cache-dir --disable-pip-version-check --no-clean --prefer-binary \
#  --no-index --find-links=./dist \
#  -r requirements.txt
#pip_install_end=$(date +%s)
#echo "pip install took $(( pip_install_end - pip_install_start )) seconds"

#test_start=$(date +%s)
#coverage run manage.py test --noinput
#coverage_end=$(date +%s)
#echo "test took $(( coverage_end - test_start )) seconds"
#
#report_start=$(date +%s)
#coverage report
#report_end=$(date +%s)
#echo "coverage report took $(( report_end - report_start )) seconds"
#
#xml_start=$(date +%s)
#coverage xml -o /api/coverages/coverage.xml
#xml_end=$(date +%s)
#echo "coverage xml took $(( xml_end - xml_start )) seconds"

end=$(date +%s)
echo "Total execution time: $(( end - start )) seconds"

#!/bin/bash

BUILD_DIR=${PWD}

cd ../python/
pipenv install
pipenv sync
cp -r app ${BUILD_DIR}/
pipenv lock -r > ${BUILD_DIR}/app/requirements.txt
cd ../docker/
docker build . -t myapp:latest
rm -r app

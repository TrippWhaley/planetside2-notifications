#!/bin/bash
set -ex

hash=$(git rev-parse HEAD)
version=${hash:0:8}

docker build -t planetside2-notifications:$version .
docker run -d --name planetside2-notifications --restart unless-stopped planetside2-notifications:$version

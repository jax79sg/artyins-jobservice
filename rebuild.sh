#!/bin/bash
git commit -a -m update
git push
docker build ./docker/. --no-cache -t artyins-jobservice
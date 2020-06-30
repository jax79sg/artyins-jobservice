#!/bin/bash

mkdir -p dockerdev
sudo rm -r dockerdev/artyins-jobservice
rsync -r ../artyins-jobservice dockerdev/
docker build ./dockerdev/. --no-cache -t artyins-jobservice

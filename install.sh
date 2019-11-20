#!/usr/bin/env bash

# This script will download and install Cerberus
cd
git clone https://github.com/geoffbacon/cerberus.git
cd cerberus
make install
make run 
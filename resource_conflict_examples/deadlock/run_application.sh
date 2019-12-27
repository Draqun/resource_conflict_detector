#!/usr/bin/bash

cmake .
make
cat data.in
bash -c "time ./deadlock_example < data.in"

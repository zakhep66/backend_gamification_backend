#!/bin/bash
autopep8 --in-place --aggressive --aggressive $1
autoflake --remove-unused-imports --remove-unused-variables --in-place $1

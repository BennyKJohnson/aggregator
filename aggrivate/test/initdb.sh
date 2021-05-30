#!/bin/bash

path=$(dirname "$0")
mysql -u $MYSQL_USER -p $MYSQL_PASSWORD < "${path%/}/initdb.sql";
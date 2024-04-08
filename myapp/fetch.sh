#!/bin/bash

# db connect
host="localhost"
port="5432"
name="bash_data"
user="postgres"

psql -h $host -d $name -U $user -p $port

req=$(psql -h "$host" -d "$name" -U "$user" -p "$port" -c "select pl,topic from myapp_data where status='req accepted';")

echo $req

cd /home/cogbee/All_Projects/dj+selenium+scheduler/myapp || exit

python3 fetch.py "$req"

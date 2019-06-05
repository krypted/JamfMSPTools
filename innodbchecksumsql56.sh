#! /bin/bash
for file in $(ls /usr/local/mysql-5.6.12-osx10.7-x86_64/data/*/*.ibd)
do
/usr/local/mysql-5.6.12-osx10.7-x86_64/bin/innochecksum $file
done

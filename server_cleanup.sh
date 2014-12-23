#!/bin/bash
function getPropertyFromFile()
{
  propertyName=`echo $1 | sed -e 's/\./\\\./g'`
  fileName=$2;
  cat $fileName | sed -n -e "s/^[ ]*//g;/^#/d;s/^$propertyName=//p" | tail -1
}

pkill python
port=`getPropertyFromFile REDIS_PORT ./refine/web/config.py`
redis-cli -p $port -a PyEsReduce  KEYS "*" | xargs redis-cli -p $port -a PyEsReduce DEL
for file in `ls /root/refine/jobs/refine`
do
  if [[ "$file" != template ]]; then
    echo $file
    redis-cli -p $port -a PyEsReduce sadd "PyEsReduce::job-types" $file
    redis-cli -p $port -a PyEsReduce set "PyEsReduce::job-types::status::${file}" "INACTIVE" 
  fi
done

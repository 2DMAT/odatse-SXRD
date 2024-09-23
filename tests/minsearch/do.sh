#!/bin/sh

set -e

#CMD=odatse-SXRD
CMD="python3 ../../src/main.py"

sh prepare.sh

time $CMD input.toml

result=output/res.txt
reference=ref.txt

echo diff $result $reference
res=0
diff $result $reference || res=$?
if [ $res -eq 0 ]; then
  echo TEST PASS
  true
else
  echo TEST FAILED: $result and $reference differ
  false
fi

result=output/0/SimplexData.txt
reference=ref_SimplexData.txt

echo diff $result $reference
res=0
diff $result $reference || res=$?
if [ $res -eq 0 ]; then
  echo TEST PASS
  true
else
  echo TEST FAILED: $result and $reference differ
  false
fi


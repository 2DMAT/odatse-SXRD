#!/bin/sh

set -e

export PYTHONUNBUFFERED=1
export OMPI_MCA_rmaps_base_oversubscribe=true

#CMD=odatse-SXRD
CMD="python3 ../../src/main.py"

MPIEXEC=""
#MPIEXEC="mpiexec -np 4"


time $MPIEXEC $CMD input.toml

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


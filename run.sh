#!/bin/bash

if [[ $1 == "local" ]]
then
  source ./settings.local
else
  if [[ -z $TIME_TO_RUN ]] || [[ $TIME_TO_RUN == "0" ]]
  then
    export TIME_TO_RUN=`date +%s`
  else
    export TIME_TO_RUN=`date --date="$TIME_TO_RUN" +%s`
  fi

  if [[ -z $DEBUG ]]
  then
    export DEBUG=0
  fi

  if [[ -z $TYPE ]]
  then
    export TYPE=2
  fi

  if [[ -z $DISK_IO_PROCESSES ]]
  then
    export DISK_IO_PROCESSES=1
  fi

  if [[ -z $MAXFILESIZE ]]
  then
    export MAXFILESIZE=20
  fi

  if [[ -z $WORK_PATH ]]
  then
    export WORK_PATH=/slow
  fi

  if [[ -z $READ_PRIORITY ]]
  then
    export READ_PRIORITY=2
  fi

  if [[ -z $INITIAL_REMOVE ]]
  then
    export INITIAL_REMOVE=1
  fi

  if [[ -z $STRESS_PROCESSES ]]
  then
    export STRESS_PROCESSES=1
  fi

  if [[ -z $MAX_MEM ]]
  then
    export MAX_MEM=60
  fi

  if [[ -z $MEM_INCREMENTER ]]
  then
    export MEM_INCREMENTER=1
  fi

  if [[ -z $MEM ]]
  then
    export MEM=60
  fi

  if [[ -z $TIMEOUT ]]
  then
    export TIMEOUT=300
  fi

  if [[ -z $BRUTE_FORCE_AMOUNT ]]
  then
    export BRUTE_FORCE_AMOUNT=600
  fi
fi

function memtest {
  MEM=$(($MEM * 1048576))
  MAX_MEM=$(($MAX_MEM * 1048576))
  MEM_INCREMENTER=$(($MEM_INCREMENTER * 1048576))
  DEFMEM=$MEM
  while :
  do
    if [[ $MEM -gt $MAX_MEM ]]
    then
      MEM=$DEFMEM
    fi
    echo $STRESS_PROCESSES workers trying to allocate $MEM bytes each
    if [[ $DEBUG -eq 1 ]]
    then
      stress -v -m $STRESS_PROCESSES -t $TIMEOUT --vm-bytes $MEM
      MEM=$(($MEM+$MEM_INCREMENTER))
      echo "MEM setted to $MEM"
    else
      stress -m $STRESS_PROCESSES -t $TIMEOUT --vm-bytes $MEM
      MEM=$(($MEM+$MEM_INCREMENTER))
    fi
    MEM=$(($MEM+$MEM_INCREMENTER))
  done

}

function disk {
  python3 ./main.py
}

function _debug {

  echo "TIME_TO_RUN:" `date --date=@"$TIME_TO_RUN" +%c`
  echo "DEBUG: $DEBUG"
  echo "TYPE: $TYPE"
  echo "DISK_IO_PROCESSES: $DISK_IO_PROCESSES"
  echo "MAXFILESIZE: $MAXFILESIZE"
  echo "WORK_PATH: $WORK_PATH"
  echo "READ_PRIORITY: $READ_PRIORITY"
  echo "INITIAL_REMOVE: $INITIAL_REMOVE"
  echo "STRESS_PROCESSES: $STRESS_PROCESSES"
  echo "MAX_MEM: $MAX_MEM"
  echo "MEM_INCREMENTER: $MEM_INCREMENTER"
  echo "MEM: $MEM"
  echo "TIMEOUT: $TIMEOUT"
  echo "BRUTE_FORCE_AMOUNT: $BRUTE_FORCE_AMOUNT"

}
if [[ $DEBUG -eq 1 ]]
then
  _debug | tee $WORK_PATH/log
fi

while :
do
  if [[ `date +%s` -ge $TIME_TO_RUN ]]
  then
    echo "Start!!!!!"
    if [[ $TYPE -eq 0 ]]
    then
      memtest &
      disk
    elif [[ $TYPE -eq 1 ]]
    then
      memtest
    elif [[ $TYPE -eq 2 ]]
    then
      disk
    elif [[ $TYPE -eq 3 ]]
    then
      ./brute_force $BRUTE_FORCE_AMOUNT
    else
      echo Some troubles with variable '$TYPE'. It is $TYPE now. Can be 0, 1, 2, 3, 4
    fi
  else
    echo $(($TIME_TO_RUN-`date +%s`)) to start
    sleep 0.2
  fi
done

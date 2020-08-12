#!/bin/bash

if (( $# < 2 )); then

  echo "hott.sh: Hot Online Test Tool: a poor man's hot-reloader. "
  echo
  echo 'USAGE: ./hott.sh <command> <args> <file1> [<file2> ... <fileN>]'
  echo
  echo 'When any of the files changes, '
  echo 'any process matching <command> exactly will be killed, '
  echo 'and "<command> <args>" will be run.'

else

  command=$1
  shift
  log=$1
  shift
  a=''
  
  while true; do
    # Check if ls -l changed
    b=`ls -l $*`

    if [[ $a != $b ]]; then
      a=$b

      pids=`pgrep -x -f "$command"`

      if [[ ! -z $pids ]]; then
        echo kill $pids
        kill $pids
      fi

      echo $command $log
      eval $command $log
    fi

    sleep 0.25
  done

fi
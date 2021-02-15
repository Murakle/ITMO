#!/bin/bash
cd /Users/user/dev/ITMO/year3/ML/codeforces/src
javac Generate.java
javac Main.java
javac Test.java
i=0
while true; do
  java -cp . Generate
  python3 /Users/user/dev/ITMO/year3/ML/labs/lab3/main.py # python
  java -cp . Main
  java -cp . Test
  read -r line <"/Users/user/dev/ITMO/year3/ML/codeforces/src/result.txt"
  if [ "$line" = "Found" ]; then
    break
  fi
  i=$((i+1))
  echo "$i"
  if [ "$i" = "100" ]; then
    echo "100"
    break
  fi
done

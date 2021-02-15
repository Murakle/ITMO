#!/bin/bash
java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8080 -jar bin/felix.jar

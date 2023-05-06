#!/bin/sh
grep -o '{{ [^}]* }}' templates/content.xml | sed 's/^{{ //;s/ }}$//;s/\(.*\)/"\1","\1"/' | sort | uniq > translations/de.csv

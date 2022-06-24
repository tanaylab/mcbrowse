#!/bin/sh
grep '^[A-Z][^A-Z].* =' mcbrowse/**/*.py | sed '
s/\//./g;
s/ =.*//;
s/^\(.*\)\.py:\(.*\)/  "\2": "\1.\2",/;
' | sort

#!/bin/bash

DIRS="`/bin/ls --color=always -gGA $@ | grep ^d | cut -d' ' -f 3-| sed -r -e 's/^\s+[0-9]+\s+//' `"
FILES="`/bin/ls -gGASh --color=always $@ | grep ^\- | cut -c 2-`"

if [ "$DIRS" ]
then
    #echo "DIRECTORIES"
    echo -e "$DIRS"
fi

if [ "$FILES" ]
then
    #echo "FILES"
    echo -e "$FILES"
fi
#printf "****DIRS****\n";
#find . -maxdepth 1 -type d -ls| cut -f 2-;
#echo "****FILES****";
#find . -maxdepth 1 -type f -ls| cut -f 2-;

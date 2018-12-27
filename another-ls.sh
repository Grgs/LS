#!/bin/bash
d=`find . -maxdepth 1 -type d -ls  | awk '{print($8, $9, $10,  substr($11,3))}' | sed 's/-/\\\(en/g'| sed 's/_//g'  | sed -r 's/\s+/\t/g'`;
f=`find . -maxdepth 1 -type f -ls | awk '{print($3, $7, $8, $9, $10, substr($11,3))}' | sed -r 's/\s+/\t/g' `;
#echo -n -e "\n$f\n"
echo -n -e  ".TS\nexpand;\nr n c a n a.\n$f\n.TE" |groff -t -a - | less
#printf "****DIRS****\n";
#find . -maxdepth 1 -type d -ls| cut -f 2-;
#echo "****FILES****";
#find . -maxdepth 1 -type f -ls| cut -f 2-;
#d=`find . -maxdepth 1 -type d -ls | sed -r -e 's/^\s*([0-9]+\s+)+d//'  | awk '{print($6, $7, $8,  substr($9,3))}' | column -t`;
#f=`find . -maxdepth 1 -type f -ls | sed -r -e 's/^\s*([0-9]+\s+)+-//' | awk '{print($1, $5, $6, $7, $8, substr($9,3))}' | column -t`;
#echo -e  "$d"  "\n$f"tbl - | nroff| colcrt| | sed 's/(\.|-|_|,)/\\\1/g' |tr \[:blank:\] "\t"

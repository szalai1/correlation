#!/bin/bash

do_normalization="$2"

function sort_directory {
    for i in $(ls $1/*.txt); do
        python $(dirname $0)/src/sort_by_value.py $i "$i"_s "$do_normalization" &
    done
}

echo "sorting in folder " $1 "..."
sort_directory $1
echo "done"

#for i in $1/oc $1/yo $1/maidan $1/euromaidan $1/15o $1/20n $1/olympics $1/normalized_syntatic_model; do
#    echo "sorting" $1 "..."
#    sort_directory $i;
#    echo $1 "done"
#done
    
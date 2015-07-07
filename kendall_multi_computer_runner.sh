#!/bin/bash -eu

preprocess_folder="$1"
from_interval="$2"
to_interval="$3"

thisDir="$(dirname $0)"
thisDir="$(readlink -f "$thisDir")"

pushd "$thisDir"

echo "Computing kendall-tau for intervals STARTED."
echo "It takes a lot of time..."
for (( i="$from_interval"; i<="$to_interval"; i++)); do
	python kendall_multi_computer.py "$preprocess_folder" "$i" &
done;
wait # postprocess needs all subprocess to finish!
echo "Computing kendall-tau for intervals FINISHED."

popd

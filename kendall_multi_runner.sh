#!/bin/bash -eu

centrality_data_folder="$1"
preprocess_folder="$2"
file_prefix="$3"
output_file="$4"
from_interval="$5"
to_interval="$6"

thisDir="$(dirname $0)"
thisDir="$(readlink -f "$thisDir")"

pushd "$thisDir"/src

echo "Preprocessing centrality data..."
python kendall_multi_preproc.py "$centrality_data_folder" "$file_prefix" "$preprocess_folder"
echo "Preprocess FINISHED"

echo "Computing kendall-tau for intervals STARTED."
echo "It takes a lot of time..."
for (( i="$from_interval"; i<="$to_interval"; i++)); do
	python kendall_multi_computer.py "$preprocess_folder" "$file_prefix" "$i" &
done;
wait # postprocess needs all subprocess to finish!
echo "Computing kendall-tau for intervals FINISHED."

echo "Postprocessing partial results..."
python kendall_multi_postproc.py "$centrality_data_folder" "$preprocess_folder" "$file_prefix" "$output_file" "$from_interval" "$to_interval"
echo "All process FINISHED."

popd

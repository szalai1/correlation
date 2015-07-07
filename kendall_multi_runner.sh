#!/bin/bash -eu

centrality_data_folder="$1"
preprocess_folder="$2"
output_file="$3"
num_of_intervals="$4"

thisDir="$(dirname $0)"
thisDir="$(readlink -f "$thisDir")"

pushd "$thisDir"

echo $centrality_data_folder
echo $preprocess_folder

echo "Preprocessing centrality data..."
python kendall_multi_preproc.py "$centrality_data_folder" "$preprocess_folder"
echo "Preprocess FINISHED"

echo "Computing kendall-tau for intervals STARTED."
echo "It takes a lot of time..."
for (( i=1; i<"$num_of_intervals"; i++)); do
	python kendall_multi_computer.py "$preprocess_folder" "$i" &
done;
wait # postprocess needs all subprocess to finish!
echo "Computing kendall-tau for intervals FINISHED."

echo "Postprocessing partial results..."
python kendall_multi_postproc.py "$centrality_data_folder" "$preprocess_folder" "$output_file"
echo "All process FINISHED."

popd

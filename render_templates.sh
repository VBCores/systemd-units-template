#!/usr/bin/env bash
set -e

jsonnet_targets=(`find . -name "*.service.jsonnet"`)

for target in "${jsonnet_targets[@]}"
do
    destination=`sed -e 's/.jsonnet//g' <<< "$target"`
    dest_dir=(`dirname ${destination}`/services)
    mkdir -p ${dest_dir}
    destination=(${dest_dir}/`basename ${destination}`)
    echo "Processing" $target "to " $destination

   jsonnet -S --jpath $(pwd) $target -o $destination
done

exit 0

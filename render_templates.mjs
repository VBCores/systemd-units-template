#!/usr/bin/env zx

const jsonnet_targets = (
    await $`find . -name "*.service.jsonnet"`.quiet()
).stdout.slice(0, -1).split('\n');

const cwd = (await $`pwd`.quiet()).stdout.slice(0, -1);

jsonnet_targets.forEach(async (filename) => {
    let destination = filename.replace('.jsonnet', '');
    console.log(`Processing ${destination}.`);

    const dest_dir = (
        await $`dirname ${destination}`.quiet()
    ).stdout.slice(0, -1).concat('', "/services");
    console.log(dest_dir);
    
    await $`mkdir -p ${dest_dir}`;

    destination = dest_dir.concat(
        '/',
        (await $`basename ${destination}`.quiet()).stdout.slice(0, -1)
    );
    console.log(`Processing ${filename} to ${destination}.`);

    await $`jsonnet -S --jpath ${cwd} ${filename} -o ${destination}`;
});

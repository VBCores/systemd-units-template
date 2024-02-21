#!/usr/bin/env zx

await $`./render_templates.mjs`;

let unit_dir = '/etc/systemd/system';

await $`sudo mkdir -p ${unit_dir}`;

async function link_service(serv_dir, serv_name) {
  await $`sudo rm -f ${unit_dir}/${serv_name} && sudo ln -s \
/opt/voltbro/${serv_dir}/${serv_name} \
${unit_dir}/${serv_name}`;
}

await link_service('canhat', 'canhat.service');

await link_service('log_watcher', 'log_watcher.timer');
await link_service('log_watcher', 'log_watcher.service');

/* Uncomment after setting up all ros units
await link_service('ros', 'ros.target');            // Main ROS target
await link_service('ros/services', 'imu.service');  // ROS node example
*/

await $`sudo systemctl daemon-reload`;

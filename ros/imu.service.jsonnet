local roslib = import 'ros.libjsonnet';
local systemd = import 'systemd.libjsonnet';

systemd.manifestService({
  Unit: {
    Description: 'Bosch IMU driver',
    PathExists: '/dev/ttyUSB0',
  },
  Service: roslib.service_defaults {
    ExecStart: roslib.exec_script('imu.sh'),
  },
  Install: roslib.install_reqs {
  },
})

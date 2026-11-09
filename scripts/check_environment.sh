#!/usr/bin/env bash
set -euo pipefail
echo '== OS =='
(lsb_release -a 2>/dev/null || cat /etc/os-release)
echo
echo '== User/groups =='
whoami
id
if id -nG | grep -qw docker; then
  echo 'Docker group membership: OK'
else
  echo 'Docker group membership is not active; re-login or use sudo'
fi
echo
echo '== Versions =='
git --version || true
docker --version || true
docker compose version || true
python3 --version || true
echo
echo '== Resources =='
free -h || true
df -h / || true
echo
docker info >/dev/null 2>&1 && echo 'Docker access: OK' || {
  echo 'Docker access failed without sudo; try sudo docker info'
  exit 1
}

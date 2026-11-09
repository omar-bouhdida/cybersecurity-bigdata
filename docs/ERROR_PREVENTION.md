# Errors Encountered and Prevention

## Docker permission denied

**Cause:** The active login session did not have Docker group membership, or the command ran under a different user.

**Fix:**
```bash
sudo usermod -aG docker "$USER"
```
Log out and back in, then run `groups` and `docker ps`. Use `sudo docker ...` as a temporary workaround.

## `newgrp: command not found`

The utility was missing. Logging out and back in refreshes group membership without needing `newgrp`. If required, install it with:

```bash
sudo apt install -y util-linux-extra
```

## Kafka consumer reported zero messages

A running broker and an existing topic do not prove that records were produced. Produce test records, inspect offsets with `kafka-get-offsets.sh`, then consume using `--from-beginning`.

## All Kafka messages appeared in one partition

The console producer was used without keys. This is acceptable for a basic smoke test. For a partitioning demonstration, publish records with keys and explain the partitioning strategy.

## VM resource pressure

The reference VM has approximately 7.2 GiB RAM and a 49 GB disk. Check `free -h`, `df -h`, and `docker stats --no-stream`. Start services incrementally and do not remove Docker volumes unless intentionally deleting persisted data.

## Version drift

Pin all image and software versions. Record Java, Hadoop, Flume, Sqoop and JDBC driver versions. Never use `latest`; test compatibility before integration.

## Pre-run checklist

- [ ] Correct Ubuntu user is active.
- [ ] Docker group is active, or commands consistently use `sudo`.
- [ ] Docker daemon is running.
- [ ] `docker compose config` succeeds.
- [ ] RAM and disk space are sufficient.
- [ ] Correct Git branch is checked out.
- [ ] No secrets or large raw datasets are staged.
- [ ] Versions match the repository configuration.
- [ ] Test evidence is saved.

# Apache Flume Installation and HDFS Integration Validation

## 1. Environment

- Operating system: Ubuntu 26.04.1 LTS
- Java runtime: Eclipse Temurin OpenJDK 11
- Apache Flume: 1.11.0
- Apache Hadoop: 3.3.6
- Deployment: Docker
- HDFS NameNode: `hdfs://localhost:9000`

## 2. Architecture

The implemented ingestion pipeline is:

Synthetic Linux authentication logs → Taildir Source → File Channel → HDFS Sink

Flume monitors authentication log files, buffers collected events through a persistent File Channel, and writes them into Hadoop Distributed File System.

## 3. Installation

1. Downloaded the official Apache Flume 1.11.0 binary distribution.
2. Verified the downloaded archive using its SHA-512 checksum.
3. Built a Docker image using Eclipse Temurin 11 JRE.
4. Configured the Flume agent.
5. Integrated the Hadoop configuration and libraries.
6. Configured the HDFS Sink to write events into HDFS.

Docker image:

`cybersecurity-flume:1.11.0`

Container:

`bigdata-flume`

## 4. Flume Components

| Component | Configuration | Purpose |
|---|---|---|
| Source | TAILDIR | Monitors authentication log files |
| Channel | FILE | Buffers events using persistent disk storage |
| Sink | HDFS | Persists collected events in HDFS |

Input file: `/opt/flume/input/auth.log`

Position file: `/opt/flume/data/taildir_position.json`

Channel checkpoint: `/opt/flume/data/checkpoint`

Channel data directory: `/opt/flume/data/data`

## 5. HDFS Configuration

Destination:

`/cybersecurity/raw/flume/`

The output directory uses date-based partitioning:

`YYYY/MM/DD/`

Output files use the `auth-events` prefix and `.log` suffix.

The HDFS Sink is configured to roll files periodically and write collected events in text format.

## 6. Validation Procedure

The following tests were performed:

- Confirmed successful startup of the Flume container.
- Confirmed successful initialization of the Taildir Source.
- Confirmed successful initialization of the HDFS Sink.
- Verified that the input authentication log was monitored.
- Appended a synthetic authentication event.
- Confirmed that Flume collected the new event.
- Confirmed that the HDFS Sink created an output file.
- Confirmed that the temporary HDFS file was closed and renamed.
- Read the resulting HDFS file to verify persisted content.

## 7. Validation Result

**PASS: Flume-to-HDFS integration successfully validated.**

A synthetic authentication event was collected from the monitored log file, transferred through the Flume File Channel, and successfully persisted in HDFS.

## 8. Evidence

Historical and current validation evidence is maintained in:

`docs/evidence/flume/`

Additional validation evidence contributed by Mohamed Ali is maintained separately in the installation documentation.

## 9. Limitations

- The authentication events are synthetic demonstration data.
- They are not part of the CIC-IDS2017 dataset.
- The demonstration uses a single Flume agent.
- HDFS currently operates with one DataNode and replication factor 1.
- Taildir file replacement and inode changes can cause duplicate event ingestion in certain circumstances.
- The demonstration is intended to validate ingestion functionality, not production-scale reliability.

## 10. Conclusion

Apache Flume 1.11.0 was successfully deployed using Docker and integrated with Hadoop HDFS.

The implemented pipeline demonstrates the collection, buffering, and persistent storage of authentication log events using Apache Flume.

# Apache Flume Validation

## 1. Environment

- Operating system: Ubuntu 26.04.1 LTS
- Java runtime: Eclipse Temurin OpenJDK 11
- Apache Flume: 1.11.0
- Deployment: Docker

## 2. Architecture

The standalone ingestion pipeline consists of:

Synthetic Linux authentication logs → Taildir Source → File Channel → Logger Sink

## 3. Installation

1. Downloaded the official Apache Flume 1.11.0 binary distribution.
2. Verified the downloaded archive using its SHA-512 checksum.
3. Extracted the binary distribution.
4. Created a Docker image using Eclipse Temurin 11 JRE.
5. Configured the Flume agent.
6. Configured Log4j2 to send application logs to the container console.

## 4. Flume Components

| Component | Configuration | Purpose |
|---|---|---|
| Source | TAILDIR | Monitors authentication log files |
| Channel | FILE | Buffers events using disk storage |
| Sink | LOGGER | Outputs collected events to the console |

Input file: `/opt/flume/input/auth.log`

Position file: `/opt/flume/data/taildir_position.json`

## 5. Validation

The initial synthetic authentication log contained eight records.

The following tests were performed:

- Confirmed that the input file contained eight lines.
- Confirmed that Taildir tracked the file at byte position 778.
- Confirmed successful initialization of the source, channel, and sink.
- Appended a ninth synthetic authentication event.
- Confirmed that Taildir advanced its position to byte 892.
- Confirmed that Logger Sink emitted the newly appended event.
- Confirmed that the Flume Docker container remained running.

## 6. Result

**PASS: Standalone Flume ingestion successfully validated.**

The test demonstrates the collection of authentication log events through the Taildir Source, buffering through the File Channel, and delivery to the Logger Sink.

## 7. Limitations and Future Work

- The current Logger Sink is used for standalone validation.
- Integration with HDFS is planned for the next implementation stage.
- The authentication logs are synthetic test data and are not part of CIC-IDS2017.
- CIC-IDS2017 will be handled separately as the network traffic analysis dataset.

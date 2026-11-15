# Integration Validation Report

## 1. Objective

The objective of this report is to document the integration and validation of the Big Data components used in the Cybersecurity Log Analytics project.

The project demonstrates three complementary data-ingestion mechanisms:

- Apache Kafka for real-time security-event streaming.
- Apache Flume for collecting authentication logs.
- Apache Sqoop for importing structured records from MySQL into HDFS.

The CIC-IDS2017 dataset is also stored and prepared in HDFS for cybersecurity traffic analysis.

The validation focuses on confirming that each component can transfer data successfully and that the resulting data is accessible in Hadoop Distributed File System (HDFS).

## 2. Implemented Architecture

The implemented architecture contains three ingestion paths converging on HDFS.

### 2.1 Kafka ingestion

Security events are published to the Kafka topic `security-logs`.

A Python consumer reads the events, converts them into JSON Lines format, and writes batches to HDFS.

Destination:

`/cybersecurity/raw/kafka/`

### 2.2 Flume ingestion

Apache Flume monitors authentication log files using the TAILDIR source.

Events pass through a persistent file channel before being written to HDFS through the HDFS sink.

Destination:

`/cybersecurity/raw/flume/YYYY/MM/DD/`

### 2.3 Sqoop ingestion

Apache Sqoop connects to the MySQL database `cybersecurity_db` and imports the `security_events` table into HDFS.

Destination:

`/cybersecurity/raw/sqoop/security_events/`

### 2.4 CIC-IDS2017 dataset

The Wednesday-workingHours dataset from CIC-IDS2017 was downloaded, analyzed, cleaned, and uploaded to HDFS.

Raw dataset:

`/cybersecurity/raw/cicids2017/`

Processed dataset:

`/cybersecurity/processed/cicids2017/`

Analysis reports and visualizations:

`/cybersecurity/reports/cicids2017/`

These ingestion paths are complementary demonstrations. They do not represent one sequential pipeline.

## 3. Reference Environment

The implementation was tested on a VirtualBox Ubuntu virtual machine.

| Component | Verified version |
|---|---|
| Operating system | Ubuntu 26.04.1 LTS |
| Architecture | x86_64 |
| CPU | 6 vCPU |
| RAM | 15 GB |
| Java | OpenJDK 11.0.33 |
| Hadoop | 3.3.6 |
| Apache Kafka | 4.1.1 |
| Apache Flume | 1.11.0 |
| Apache Sqoop | 1.4.7 |
| MySQL Server | 8.4.13 |
| Docker Engine | 29.1.3 |
| Docker Compose | 2.40.3 |
| Python | 3.14.4 |

## 4. HDFS Health Verification

HDFS was started successfully and its NameNode and DataNode processes were verified.

The HDFS directory structure was created to separate raw ingestion data, processed datasets, and analytical reports.

Main directory:

`/cybersecurity/`

Subdirectories:

- `raw/`
- `processed/`
- `reports/`

The HDFS health report confirmed one live DataNode.

The configured replication factor is 1. Therefore, this deployment demonstrates HDFS functionality but does not provide multi-node fault tolerance.

## 5. Kafka-to-HDFS Validation

Kafka was deployed using Apache Kafka 4.1.1 in KRaft mode.

The topic `security-logs` was created with:

- Partitions: 3
- Replication factor: 1

A Python consumer was implemented using `kafka-python`.

The consumer reads JSON events, groups them into batches, writes them to HDFS, and commits Kafka offsets after successful HDFS writes.

### Validation results

- Kafka broker connection: successful.
- Topic discovery: successful.
- Event consumption: successful.
- Batch writing to HDFS: successful.
- Offset commit: successful.
- Graceful shutdown: tested.

Four output files were identified in the HDFS Kafka directory.

Total size: 1,343 bytes.

Destination:

`/cybersecurity/raw/kafka/year=2026/month=11/day=15/`

The output files were inspected and contained the expected JSON security events.

The implementation provides at-least-once delivery semantics. A failure after writing to HDFS but before committing the Kafka offset may result in duplicate records.

## 6. Flume-to-HDFS Validation

Apache Flume 1.11.0 was deployed in a Docker container.

The implemented Flume agent uses:

- Source: TAILDIR
- Channel: FILE
- Sink: HDFS

The source monitors the authentication log file:

`/opt/flume/input/auth.log`

The sink writes events to:

`/cybersecurity/raw/flume/YYYY/MM/DD/`

### Validation results

- Flume container startup: successful.
- TAILDIR source configuration: successful.
- Persistent file channel: configured.
- HDFS sink: successful.
- HDFS output inspection: successful.

One authentication log record was verified in HDFS.

The demonstration record is synthetic and was created for testing. It is not a real security incident or part of CIC-IDS2017.

## 7. MySQL-to-HDFS Validation Using Sqoop

MySQL Server 8.4.13 was configured with the database:

`cybersecurity_db`

The database contains the table:

`security_events`

A dedicated MySQL account was configured with the required read permissions for the import.

Apache Sqoop 1.4.7 was configured with the MySQL JDBC connector.

The import operation successfully transferred the table into HDFS.

### Validation results

- MySQL service: active.
- Database connection: successful.
- Sqoop version: verified.
- MySQL JDBC connection: successful.
- Table import: successful.
- HDFS output inspection: successful.

Imported records: 8.

Destination:

`/cybersecurity/raw/sqoop/security_events/`

The imported records were inspected in HDFS and matched the expected demonstration data.

These eight records are synthetic test records.

## 8. CIC-IDS2017 Dataset Validation

The project uses the CIC-IDS2017 dataset published by the Canadian Institute for Cybersecurity.

The selected file is:

`Wednesday-workingHours.pcap_ISCX.csv`

The dataset contains network-flow records with 78 features and one target label.

### 8.1 Raw dataset

- Records: 692,703
- Columns: 79
- Labels: 6

The raw dataset was uploaded to HDFS.

Destination:

`/cybersecurity/raw/cicids2017/Wednesday-workingHours.pcap_ISCX.csv`

### 8.2 Data cleaning

The cleaning process included:

- Column-name normalization.
- Label normalization.
- Replacement of infinite values with missing values.
- Removal of records with missing or empty labels.
- Duplicate detection using row fingerprints.
- Numeric missing-value imputation using chunk-level medians.

The original dataset contained 692,703 records.

The cleaned dataset contains 619,791 records.

A total of 72,912 records were removed during duplicate detection.

Missing numeric values were handled by the cleaning process.

The implementation uses chunk-level median imputation rather than a single global median. This is documented as a methodological limitation.

### 8.3 Processed dataset

The cleaned dataset was uploaded to:

`/cybersecurity/processed/cicids2017/Wednesday-cleaned.csv`

The dataset was verified in HDFS.

### 8.4 Reports and visualizations

The following analytical reports were stored in HDFS:

- `wednesday-analysis.txt`
- `cleaning-summary.txt`

Three visualizations were generated:

- `01_benign_vs_malicious.png`
- `02_traffic_class_distribution.png`
- `03_before_after_cleaning.png`

They are available under:

`/cybersecurity/reports/cicids2017/figures/`

## 9. Consolidated Validation Results

| Component | Validation | Result |
|---|---|---|
| HDFS | NameNode and DataNode operational | Passed |
| Kafka | Event streaming and HDFS persistence | Passed |
| Flume | Authentication log collection and HDFS persistence | Passed |
| MySQL | Database service and table availability | Passed |
| Sqoop | Import of 8 MySQL records into HDFS | Passed |
| CIC-IDS2017 raw | 692,703 records stored in HDFS | Passed |
| CIC-IDS2017 processed | 619,791 records stored in HDFS | Passed |
| Reports | Analysis files and visualizations stored in HDFS | Passed |

### Record-count verification

The HDFS validation commands returned:

| Dataset | Lines reported | Actual data records |
|---|---:|---:|
| Flume | 1 | 1 |
| Sqoop | 8 | 8 |
| CIC-IDS2017 raw | 692,704 | 692,703 |
| CIC-IDS2017 cleaned | 619,792 | 619,791 |

The CIC-IDS2017 line counts include one CSV header row.

Kafka produced four files with a combined size of 1,343 bytes.

## 10. Technical Limitations

The implementation has several limitations that must be considered when interpreting the results.

1. **Single-node HDFS:** The deployment uses one DataNode with replication factor 1. It does not demonstrate distributed storage fault tolerance.

2. **Single Kafka broker:** The Kafka deployment uses one broker and replication factor 1. Broker-level redundancy is not demonstrated.

3. **Local MapReduce execution:** MapReduce is configured with LocalJobRunner. A distributed YARN cluster has not been implemented.

4. **Dataset scope:** Only the Wednesday-workingHours file from CIC-IDS2017 was selected. The complete dataset was not processed.

5. **Synthetic demonstration records:** Kafka events, Flume authentication logs, and MySQL records were created for testing. They must not be presented as real-world incidents or as records extracted from CIC-IDS2017.

6. **Cleaning methodology:** Duplicate detection uses row fingerprints, and numeric missing values are imputed using chunk-level medians. These choices have methodological limitations.

7. **Class distribution changes:** Duplicate removal affects the distribution of traffic labels. The cleaning process removed a substantial number of records, particularly from the DoS Hulk class. This must be considered in any later machine-learning evaluation.

8. **Flume file monitoring:** TAILDIR can encounter duplicate-event behavior when monitored files are replaced or their inodes change.

9. **Kafka delivery semantics:** The consumer provides at-least-once delivery rather than exactly-once processing.

These limitations define the scope of the current implementation and provide opportunities for future improvements.

## 11. Evidence and Supporting Documentation

Technical evidence is maintained in the repository under:

`docs/evidence/`

Supporting installation and validation documentation is available under:

`docs/installation/`

Relevant documents include:

- `reference-environment.md`
- `kafka-validation.md`
- `kafka-hdfs-validation.md`
- `flume-validation.md`
- `sqoop-validation.md`
- `mysql/mysql-validation.md`

The repository also contains the scripts used for Kafka consumption, CIC-IDS2017 analysis, cleaning, and visualization.

## 12. Conclusion

The integration tests demonstrate that Apache Kafka, Apache Flume, and Apache Sqoop can successfully transfer their respective demonstration data into HDFS.

The selected CIC-IDS2017 dataset was also stored, cleaned, analyzed, and verified in HDFS.

The project therefore demonstrates multiple Big Data ingestion approaches applied to a cybersecurity analytics use case.

Although the current deployment is a single-node environment and does not provide distributed fault tolerance or a full YARN cluster, it provides a functional foundation for demonstrating data ingestion, storage, preparation, and analysis.

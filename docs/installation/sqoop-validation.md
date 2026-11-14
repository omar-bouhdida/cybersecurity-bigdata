# Sqoop Validation: MySQL to HDFS

## 1. Environment

| Component | Version |
|---|---|
| Apache Sqoop | 1.4.7 |
| Apache Hadoop | 3.3.6 |
| Java | OpenJDK 11 |
| MySQL Server | 8.4.13 |
| MySQL Connector/J | 9.5.0 |

## 2. Objective

Validate the transfer of cybersecurity event records from a MySQL relational database into Hadoop Distributed File System (HDFS) using Apache Sqoop.

## 3. Source Database

- Database: `cybersecurity_db`
- Table: `security_events`
- Initial number of records: 8
- Database connection: JDBC

The records are synthetic demonstration events created for this academic project.

## 4. Import Command

```bash
sqoop import \
  -libjars /home/vboxuser/bigdata-downloads/generated-classes/security_events.jar \
  --connect jdbc:mysql://localhost:3306/cybersecurity_db \
  --username sqoop_user \
  -P \
  --table security_events \
  --target-dir /cybersecurity/raw/sqoop/security_events \
  --num-mappers 1
```

## 5. HDFS Destination

```text
/cybersecurity/raw/sqoop/security_events/
├── _SUCCESS
└── part-m-00000
```

## 6. Validation Results

| Test | Result |
|---|---|
| MySQL JDBC connection | PASS |
| Sqoop code generation | PASS |
| MapReduce execution | PASS |
| HDFS data transfer | PASS |
| Imported records | 8 |
| Output file created | PASS |

The Sqoop job completed successfully and transferred 8 records (approximately 1.11 KB) to HDFS.

## 7. Conclusion

The MySQL-to-HDFS ingestion pipeline using Apache Sqoop 1.4.7 was successfully validated.

The test demonstrates how structured cybersecurity event records stored in a relational database can be transferred into HDFS for centralized Big Data storage and subsequent analysis.

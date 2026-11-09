# Team Responsibilities

## Omar — Project lead, integration and documentation

Owns repository structure, architecture, integration planning, Hadoop/HDFS setup, compatibility decisions, end-to-end demo coordination, final report, annex and presentation.

**Documentation ownership:** Omar writes and maintains the final project documentation. Every technical owner must still provide commands, configuration, version details, screenshots, test results and errors/fixes. Omar should not have to reconstruct undocumented work.

## Mohamed Ali — Kafka and Flume

Owns Kafka producer/consumer scripts and event format, Flume configuration, sample log ingestion, initial simple sink test, then HDFS sink integration when HDFS is ready.

Deliverables: tested scripts/configuration, successful test evidence, version details and short troubleshooting notes.

## Sadek Amine — Dataset and MySQL preparation (focused/easier scope)

Owns obtaining the agreed CIC-IDS2017 sample, recording the official source and selected files, inspecting columns and labels, preparing a small documented CSV subset, creating the MySQL schema, loading the sample and verifying row counts.

Deliverables: reproducible preparation steps/script, `sql/schema.sql`, small sample if licensing permits, row-count checks and screenshots.

Sqoop compatibility and final integration remain with Omar unless the team later agrees otherwise. This keeps Sadek's scope focused and avoids assigning him the more complex legacy Hadoop/Sqoop compatibility work.

## Shared rules

1. Work on separate feature branches.
2. Commit scripts and configs, not credentials or large raw datasets.
3. Test each component independently.
4. Record exact commands and software versions.
5. Provide screenshots or terminal output for successful tests.
6. Report blockers early; do not silently alter shared configuration.

Suggested branches:
- `feature/hadoop-hdfs`
- `feature/kafka-flume`
- `feature/dataset-mysql`

## Integration checkpoints

1. Each owner demonstrates a standalone component test.
2. Omar reviews configuration and version compatibility.
3. Integrate one component at a time.
4. Run the complete demonstration.
5. Omar assembles the final report and presentation from evidence supplied by the team.

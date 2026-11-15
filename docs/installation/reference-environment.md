# Reference Environment Validation

## 1. System

- Operating system: Ubuntu 26.04.1 LTS
- Architecture: x86_64
- User: vboxuser

## 2. Hardware Resources

| Resource | Configuration |
|---|---|
| CPU | 6 vCPU |
| RAM | 15 GiB |
| Swap | 4 GiB |
| Disk capacity | 49 GB |
| Disk used | 23 GB |
| Disk available | 25 GB |
| Disk utilization | 48% |

Resource measurements were collected on November 15, 2026.

## 3. Software Environment

| Component | Version |
|---|---|
| Git | 2.53.0 |
| Docker Engine | 29.1.3 |
| Docker Compose | 2.40.3 |
| Python | 3.14.4 |
| Java | OpenJDK 11 |
| Hadoop | 3.3.6 |
| Apache Kafka | 4.1.1 |
| Apache Flume | 1.11.0 |
| Apache Sqoop | 1.4.7 |
| MySQL Server | 8.4.13 |

## 4. Environment Validation

| Component | Result |
|---|---|
| Ubuntu operating system | PASS |
| CPU resources | PASS |
| Memory availability | PASS |
| Disk availability | PASS |
| Docker permissions | PASS |
| Docker daemon | PASS |
| Docker Compose | PASS |
| Git | PASS |
| Python | PASS |
| Hadoop HDFS | PASS |

## 5. Resource Considerations

The environment runs inside an Oracle VirtualBox virtual machine.

Although the VM has 15 GiB of RAM, memory usage must be monitored when multiple services run simultaneously.

The project uses a single-node Hadoop HDFS deployment with one DataNode and replication factor 1. MapReduce uses LocalJobRunner rather than a distributed YARN cluster.

The environment is suitable for academic development, component integration, functional testing, and demonstrations.

## 6. Conclusion

The reference development environment is operational.

The project's Big Data components have been installed and validated individually, with successful integration tests for:

- Kafka → HDFS
- Flume → HDFS
- MySQL → HDFS through Sqoop

The environment supports academic development, component integration,
functional testing, and project demonstrations.

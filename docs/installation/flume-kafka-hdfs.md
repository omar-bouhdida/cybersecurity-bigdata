# Pipelines Flume -> HDFS et Kafka -> HDFS

Environnement : Ubuntu 24.04.4, OpenJDK 11, Hadoop 3.3.6 (HDFS sur localhost:9000),
Docker, Flume 1.11.0, Kafka 4.1.1.

## Prerequis

HDFS ne redemarre pas automatiquement avec la VM :

    start-dfs.sh
    jps

jps doit lister NameNode, DataNode et SecondaryNameNode.

## Flume -> HDFS

Construire et demarrer :

    docker build -t cybersecurity-flume:1.11.0 -f flume/Dockerfile flume
    docker compose up -d flume

Tester : ajouter une ligne a data/sample-logs/auth.log (puis git checkout du fichier), attendre environ 45 s :

    docker logs bigdata-flume 2>&1 | grep -v "Processing:" | tail -30
    hdfs dfs -ls -R /cybersecurity/raw/flume/
    hdfs dfs -cat /cybersecurity/raw/flume/*/*

Arreter :

    docker compose stop flume

## Kafka -> HDFS

Demarrer Kafka et creer le topic :

    docker compose up -d kafka
    docker exec bigdata-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic security-logs --partitions 3 --replication-factor 1

Installer et lancer le consommateur :

    python3 -m venv kafka-consumer/.venv
    kafka-consumer/.venv/bin/pip install kafka-python-ng
    kafka-consumer/.venv/bin/python kafka-consumer/consumer.py

Produire des evenements :

    echo '{"event":"test"}' | docker exec -i bigdata-kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic security-logs

Verifier :

    hdfs dfs -ls -R /cybersecurity/raw/kafka/
    hdfs dfs -cat /cybersecurity/raw/kafka/*/*

Arreter : Ctrl+C (arret propre, le dernier lot est ecrit), puis :

    docker compose stop kafka

## Resultats des tests

- Flume : 9 lignes initiales + 1 ligne ajoutee apres demarrage presentes dans HDFS.
- Kafka : 1 evenement, puis lot A (10 evenements) : 10 dans HDFS.
  Consommateur arrete, lot B (5 evenements) produit, redemarrage : 5 dans HDFS, A reste a 10.

## Erreurs rencontrees

1. Flume NoClassDefFoundError (SequenceFile$CompressionType) : le hadoop-env.sh monte
   fixait JAVA_HOME au chemin de la VM, absent du conteneur, donc hadoop classpath echouait.
   Solution : lien symbolique /usr/lib/jvm/java-11-openjdk-amd64 -> /opt/java/openjdk.
2. Flume OutOfMemoryError : flume-ng utilise -Xmx20m par defaut. Solution : -Xms256m -Xmx512m.
3. Connection refused sur localhost:9000 : HDFS arrete. Solution : start-dfs.sh.

## Limites

- Flume : network_mode host et montage de /opt/hadoop specifiques a cette VM
  (chemins et HADOOP_USER_NAME a adapter). Avertissement SLF4J en double sans impact.
- Kafka : semantique at-least-once (offsets valides apres ecriture HDFS). Un crash entre
  l'ecriture et le commit peut creer des doublons ; non teste.
- Chaque lot cree un fichier : beaucoup de petits fichiers HDFS (a compacter plus tard).
- Si l'ecriture HDFS echoue, le lot est conserve en memoire et reessaye ; il est perdu
  si le processus est tue.
- Donnees de test synthetiques, pas CIC-IDS2017.
- Flume (Taildir) : si auth.log est remplace (git checkout change l inode), le fichier est relu depuis le debut et les lignes sont dupliquees dans HDFS (voir flume-hdfs-content.txt).

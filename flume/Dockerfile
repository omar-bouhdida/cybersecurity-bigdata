FROM eclipse-temurin:11-jre-jammy

ENV FLUME_HOME=/opt/flume
ENV PATH="${FLUME_HOME}/bin:${PATH}"
ENV JAVA_OPTS="-Xms128m -Xmx384m"

WORKDIR /opt

COPY downloads/apache-flume-1.11.0-bin /opt/flume

RUN mkdir -p /usr/lib/jvm && \
    ln -s /opt/java/openjdk /usr/lib/jvm/java-11-openjdk-amd64 && \
    groupadd -g 1000 vboxuser && \
    useradd -u 1000 -g 1000 -d /home/vboxuser -m -s /bin/bash vboxuser

RUN mkdir -p \
    /opt/flume/input \
    /opt/flume/data \
    /opt/flume/output

WORKDIR /opt/flume

CMD ["flume-ng", "agent", "--conf", "/opt/flume/conf", "--conf-file", "/opt/flume/conf/flume.conf", "--name", "agent", "-Dflume.root.logger=INFO,console"]

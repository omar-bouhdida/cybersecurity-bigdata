FROM eclipse-temurin:11-jre-jammy

ENV FLUME_HOME=/opt/flume
ENV PATH="${FLUME_HOME}/bin:${PATH}"
ENV JAVA_OPTS="-Xms128m -Xmx384m"

WORKDIR /opt

COPY downloads/apache-flume-1.11.0-bin /opt/flume

RUN mkdir -p \
    /opt/flume/input \
    /opt/flume/data \
    /opt/flume/output

WORKDIR /opt/flume

CMD ["flume-ng", "agent", "--conf", "/opt/flume/conf", "--conf-file", "/opt/flume/conf/flume.conf", "--name", "agent", "-Dflume.root.logger=INFO,console"]

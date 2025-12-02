FROM ontotext/graphdb:10.8.11

RUN mkdir /root/graphdb-import
RUN mkdir -p /opt/graphdb/home/data/repositories/abromics-kg

ENV JAVA_OPTS="-Xms32g -Xmx62g -XX:+UseG1GC -XX:MaxGCPauseMillis=200"

# -*- encoding: utf-8 -*-

#
##########################
# GLOBAL SERVER SETTINGS #
##########################

""" BUild ANd Add to REPO = buanarepo """
BUANAREPO = '/usr/bin/buanarepo'

"""Root privileges are necessary on the remote hosts"""
REMOTE_RSYNC_USER = 'root'
RSYNC_CMD = "sudo rsync -e 'ssh -o StrictHostKeyChecking=no' -r -l -t -D -v -h -z --progress --partial-dir={partialdir} --delete --exclude-from={excludefrom} {remoteuser}@{remotehost}:{remotedir} {localdir}; sudo chown -R buanarepo:buanarepo {localdir}"

"""The Following directories and files are created during the API install"""
EXCLUDE_FROM = '/opt/buanaserver/rsync/conf/exclude'
PARTIAL_DIR = '/opt/buanaserver/rsync/partial'
BASE_BUILD = '/srv/buanarepo-build'
BASE_JENKINS_BUILD = '/var/lib/jenkins/workspace'
URL_GIT = 'git@github.com:nebul4ck'

#
#######################
# BACKUP APP SETTINGS #
#######################

""" Rabbitma-server Settings """
"""Warning: the end slash ("/") is necessary"""
RABBITMQ_REMOTE_CONFIG_FILE = '/etc/rabbitmq/'
RABBITMQ_REMOTE_LOGROTATE = '/etc/logrotate.d/rabbitmq-server'
RABBITMQ_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/rabbitmq-server.service'
RABBITMQ_LOCAL_CONFIG_FILE = '{base_build}/rabbitmq/rabbitmq/etc/rabbitmq'.format(\
        base_build=BASE_BUILD)
RABBITMQ_LOCAL_LOGROTATE = '{base_build}/rabbitmq/rabbitmq/etc/logrotate.d/rabbitmq-server'.format(\
        base_build=BASE_BUILD)
RABBITMQ_LOCAL_SYSTEMD_FILE = '{base_build}/rabbitmq/rabbitmq/lib/systemd/system/rabbitmq-server.service'.format(\
        base_build=BASE_BUILD)

""" Nodered Settings """
"""Warning: the end slash ("/") is necessary"""
NODERED_REMOTE_CONFIG_FILE = '/opt/node-red/settings.js'
NODERED_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/node-red.service'
NODERED_REMOTE_FLOW_FILE = '/opt/node-red/flows/'

NODERED_LOCAL_CONFIG_FILE = '{base_build}/nodered/nodered/opt/node-red/settings.js'.format(\
        base_build=BASE_BUILD)
NODERED_LOCAL_SYSTEMD_FILE = '{base_build}/nodered/nodered/lib/systemd/system/node-red.service'.format(\
        base_build=BASE_BUILD)
NODERED_LOCAL_FLOW_FILE = '{base_build}/nodered/nodered/opt/node-red/flows'.format(\
        base_build=BASE_BUILD)
# """ Posgresql-10 Settings """
# """Warning: the end slash ("/") is necessary"""
# POSTGRESQL10_REMOTE_CONFIG_FILE = '/etc/postgresql/10/main/postgresql.conf'
# POSTGRESQL10_REMOTE_HBA_FILE = '/etc/postgresql/10/main/pg_hba.conf'

# POSTGRESQL10_LOCAL_CONFIG_FILE = '{base_build}/postgresql10/tmp/postgresql.conf'.format(\
#         base_build=BASE_BUILD)
# POSTGRESQL10_LOCAL_HBA_FILE = '{base_build}/postgresql10/tmp/pg_hba.conf'.format(\
#         base_build=BASE_BUILD)

# """ Posgresql-common Settings """
# """Warning: the end slash ("/") is necessary"""
# POSTGRESQLCOMMON_REMOTE_LOGROTATE = '/etc/logrotate.d/postgresql-common'
# POSTGRESQLCOMMON_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/postgresql*'

# POSTGRESQLCOMMON_LOCAL_LOGROTATE = '{base_build}/postgresqlcommon/etc/logrotate.d/postgresql-common'.format(\
#         base_build=BASE_BUILD)
# POSTGRESQLCOMMON_LOCAL_SYSTEMD_FILE = '{base_build}/postgresqlcommon/lib/systemd/system/'.format(\
#         base_build=BASE_BUILD)

""" Mosquitto Settings """
"""Warning: the end slash ("/") is necessary"""
MOSQUITTO_REMOTE_CONFIG_FILE = '/etc/mosquitto/mosquitto.conf'
MOSQUITTO_REMOTE_CONFIG_DIR = '/etc/mosquitto/conf.d/'
MOSQUITTO_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/mosquitto.service'
MOSQUITTO_REMOTE_LOGROTATE = '/etc/logrotate.d/mosquitto'
MOSQUITTO_LOCAL_CONFIG_FILE = '{base_build}/mosquitto/mosquitto/etc/mosquitto/mosquitto.conf'.format(\
        base_build=BASE_BUILD)
MOSQUITTO_LOCAL_CONFIG_DIR = '{base_build}/mosquitto/mosquitto/etc/mosquitto/conf.d'.format(\
        base_build=BASE_BUILD)
MOSQUITTO_LOCAL_SYSTEMD_FILE = '{base_build}/mosquitto/mosquitto/lib/systemd/system/mosquitto.service'.format(\
        base_build=BASE_BUILD)
MOSQUITTO_LOCAL_LOGROTATE = '{base_build}/mosquitto/mosquitto/etc/logrotate.d/mosquitto'.format(\
        base_build=BASE_BUILD)

""" InfluxDB Settings """
"""Warning: the end slash ("/") is necessary"""
INFLUXDB_REMOTE_CONFIG_FILE = '/etc/influxdb/influxdb.conf'
INFLUXDB_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/influxdb.service'
INFLUXDB_REMOTE_LOGROTATE = '/etc/logrotate.d/influxdb'
INFLUXDB_REMOTE_RSYSLOG = '/etc/rsyslog.d/49-influxdb.conf'
INFLUXDB_LOCAL_CONFIG_FILE = '{base_build}/influxdb/influxdb/etc/influxdb/influxdb.conf'.format(\
        base_build=BASE_BUILD)
INFLUXDB_LOCAL_SYSTEMD_FILE = '{base_build}/influxdb/influxdb/usr/lib/influxdb/scripts/influxdb.service'.format(\
        base_build=BASE_BUILD)
INFLUXDB_LOCAL_LOGROTATE = '{base_build}/influxdb/influxdb/etc/logrotate.d/influxdb'.format(\
        base_build=BASE_BUILD)
INFLUXDB_LOCAL_RSYSLOG = '{base_build}/influxdb/influxdb/etc/rsyslog.d/49-influxdb.conf'.format(\
        base_build=BASE_BUILD)

# """ MongoDB Settings """
# """Warning: the end slash ("/") is necessary"""
# MONGODB_REMOTE_CONFIG_FILE = '/etc/mongod.conf'
# MONGODB_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/mongod.service'
# MONGODB_REMOTE_LOGROTATE = '/etc/logrotate.d/mongodb-server'
# MONGODB_LOCAL_CONFIG_FILE = '{base_build}/mongodb/mongodb/etc/mongod.conf'.format(\
#         base_build=BASE_BUILD)
# MONGODB_LOCAL_SYSTEMD_FILE = '{base_build}/mongodb/mongodb/lib/systemd/system/mongod.service'.format(\
#         base_build=BASE_BUILD)
# MONGODB_LOCAL_LOGROTATE = '{base_build}/mongodb/mongodb/etc/logrotate.d/mongodb-server'.format(\
#         base_build=BASE_BUILD)

""" Kafka Settings """
"""Warning: the end slash ("/") is necessary"""
KAFKA_REMOTE_APP_DIR = '/opt/kafka/'
KAFKA_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/kafka.service'
KAFKA_REMOTE_BINS = '/usr/bin/kafka-*'
KAFKA_REMOTE_LOGROTATE = '/etc/logrotate.d/kafka'
KAFKA_LOCAL_LOGROTATE = '{base_build}/kafka/kafka/etc/logrotate.d/kafka'.format(\
        base_build=BASE_BUILD)
KAFKA_LOCAL_APP_DIR = '{base_build}/kafka/kafka/opt/kafka'.format(\
        base_build=BASE_BUILD)
KAFKA_LOCAL_SYSTEMD_FILE = '{base_build}/kafka/kafka/lib/systemd/system/'.format(\
        base_build=BASE_BUILD)
KAFKA_LOCAL_BINS = '{base_build}/kafka/kafka/usr/bin/'.format(\
        base_build=BASE_BUILD)

""" Zookeeper Settings """
"""Warning: the end slash ("/") is necessary"""
ZOOKEEPER_REMOTE_APP_DIR = '/opt/zookeeper/'
ZOOKEEPER_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/zookeeper.service'
ZOOKEEPER_REMOTE_LOGROTATE = '/etc/logrotate.d/zookeeper'
ZOOKEEPER_LOCAL_LOGROTATE = '{base_build}/zookeeper/zookeeper/etc/logrotate.d/zookeeper'.format(\
        base_build=BASE_BUILD)
ZOOKEEPER_LOCAL_APP_DIR = '{base_build}/zookeeper/zookeeper/opt/zookeeper'.format(\
        base_build=BASE_BUILD)
ZOOKEEPER_LOCAL_SYSTEMD_FILE = '{base_build}/zookeeper/zookeeper/lib/systemd/system'.format(\
        base_build=BASE_BUILD)

""" Hadoop Settings """
"""Warning: the end slash ("/") is necessary"""
HADOOP_REMOTE_APP_DIR = '/opt/hadoop/'
HADOOP_REMOTE_SYSTEMD_FILES = ['/lib/systemd/system/namenode.service',\
'/lib/systemd/system/secondarynamenode.service','/lib/systemd/system/datanode.service']
HADOOP_REMOTE_LOGROTATE_FILE = '/etc/logrotate.d/hdfs'
HADOOP_LOCAL_APP_DIR = '{base_build}/hdfs/hdfs/opt/hadoop'.format(\
        base_build=BASE_BUILD)
HADOOP_LOCAL_SYSTEMD_FILE = '{base_build}/hdfs/hdfs/lib/systemd/system'.format(\
        base_build=BASE_BUILD)
HADOOP_LOCAL_LOGROTATE_FILE = '{base_build}/hdfs/hdfs/etc/logrotate.d'.format(\
        base_build=BASE_BUILD)

""" Druid Settings """
"""Warning: the end slash ("/") is necessary"""
DRUID_REMOTE_APP_DIR = '/opt/druid/'
DRUID_REMOTE_SYSTEMD_FILES = ['/lib/systemd/system/overlord.service',\
'/lib/systemd/system/middlemanager.service','/lib/systemd/system/broker.service',\
'/lib/systemd/system/historical.service','/lib/systemd/system/coordinator.service']
DRUID_REMOTE_BINS = '/usr/bin/druid_*'
DRUID_REMOTE_LOGROTATE = '/etc/logrotate.d/druid'
DRUID_LOCAL_LOGROTATE = '{base_build}/druid/druid/etc/logrotate.d/druid'.format(\
        base_build=BASE_BUILD)
DRUID_LOCAL_APP_DIR = '{base_build}/druid/druid/opt/druid'.format(\
        base_build=BASE_BUILD)
DRUID_LOCAL_SYSTEMD_FILE = '{base_build}/druid/druid/lib/systemd/system'.format(\
        base_build=BASE_BUILD)
DRUID_LOCAL_BINS = '{base_build}/druid/druid/usr/bin/'.format(\
        base_build=BASE_BUILD)

# """ Tranquility Settings """
# """Warning: the end slash ("/") is necessary"""
# TRANQUILITY_REMOTE_APP_DIR = '/opt/tranquility/'
# TRANQUILITY_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/tranquility-rt-tasks.service'
# TRANQUILITY_LOCAL_APP_DIR = '{base_build}/tranquility/opt/tranquility'.format(\
#         base_build=BASE_BUILD)
# TRANQUILITY_LOCAL_SYSTEMD_FILE = '{base_build}/tranquility/lib/systemd/system'.format(\
#         base_build=BASE_BUILD)

""" Spark Settings """
"""Warning: the end slash ("/") is necessary"""
SPARK_REMOTE_APP_DIR = '/opt/spark/'
SPARK_REMOTE_SYSTEMD_FILES = ['/lib/systemd/system/spark-master.service',\
'/lib/systemd/system/spark-worker.service']
SPARK_REMOTE_LOGROTATE = '/etc/logrotate.d/spark'
SPARK_LOCAL_LOGROTATE = '{base_build}/spark/spark/etc/logrotate.d/spark'.format(\
        base_build=BASE_BUILD)
SPARK_LOCAL_APP_DIR = '{base_build}/spark/spark/opt/spark'.format(\
        base_build=BASE_BUILD)
SPARK_LOCAL_SYSTEMD_FILE = '{base_build}/spark/spark/lib/systemd/system'.format(\
        base_build=BASE_BUILD)

""" Cerebro Settings """
"""Warning: the end slash ("/") is necessary"""
CEREBRO_REMOTE_APP_DIR = '/opt/cerebro/'
CEREBRO_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/cerebro.service'
CEREBRO_REMOTE_LOGROTATE = '/etc/logrotate.d/cerebro'
CEREBRO_LOCAL_LOGROTATE = '{base_build}/cerebro/cerebro/etc/logrotate.d/cerebro'.format(\
        base_build=BASE_BUILD)
CEREBRO_LOCAL_APP_DIR = '{base_build}/cerebro/cerebro/opt/cerebro'.format(\
        base_build=BASE_BUILD)
CEREBRO_LOCAL_SYSTEMD_FILE = '{base_build}/cerebro/cerebro/lib/systemd/system'.format(\
        base_build=BASE_BUILD)

""" Redis Settings """
"""Warning: the end slash ("/") is necessary"""
REDIS_REMOTE_CONF_FILE = '/etc/redis/redis.conf'
REDIS_REMOTE_LOGROTATE_FILE = '/etc/logrotate.d/redis-server'
REDIS_REMOTE_DEFAULT_FILE = '/etc/default/redis-server'
REDIS_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/redis-server.service'
REDIS_REMOTE_INITD_FILE = '/etc/init.d/redis-server'
REDIS_LOCAL_CONF_FILE = '{base_build}/redis/redis/etc/redis'.format(\
        base_build=BASE_BUILD)
REDIS_LOCAL_SYSTEMD_FILE = '{base_build}/redis/redis/lib/systemd/system'.format(\
        base_build=BASE_BUILD)
REDIS_LOCAL_DEFAULT_FILE = '{base_build}/redis/redis/etc/default'.format(\
        base_build=BASE_BUILD)
REDIS_LOCAL_LOGROTATE_FILE = '{base_build}/redis/redis/etc/logrotate.d'.format(\
        base_build=BASE_BUILD)
REDIS_LOCAL_INITD_FILE = '{base_build}/redis/redis/etc/init.d'.format(\
        base_build=BASE_BUILD)

# """ Kaa-node Settings """
# """Warning: the end slash ("/") is necessary"""
# KAA_REMOTE_FILES = '/usr/lib/kaa-node/'
# KAA_REMOTE_DEFAULT_FILE = '/etc/default/kaa-node'
# KAA_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/kaa.service'
# KAA_LOCAL_FILES = '{base_build}/kaa/usr/lib/kaa-node'.format(\
#         base_build=BASE_BUILD)
# KAA_LOCAL_SYSTEMD_FILE = '{base_build}/kaa/lib/systemd/system'.format(\
#         base_build=BASE_BUILD)
# KAA_LOCAL_DEFAULT_FILE = '{base_build}/kaa/etc/default'.format(\
#         base_build=BASE_BUILD)

""" Logstash-node Settings """
"""Warning: the end slash ("/") is necessary"""
LOGSTASH_REMOTE_CONF_FILES = '/etc/logstash/conf.d/'
LOGSTASH_REMOTE_DEFAULT_FILE = '/etc/default/logstash'
LOGSTASH_REMOTE_SYSTEMD_FILE = '/etc/init.d/logstash'
LOGSTASH_REMOTE_LOGROTATE_FILE = '/etc/logrotate.d/logstash'
LOGSTASH_LOCAL_CONF_FILES = '{base_build}/logstash/logstash/etc/logstash/conf.d'.format(\
        base_build=BASE_BUILD)
LOGSTASH_LOCAL_SYSTEMD_FILE = '{base_build}/logstash/logstash/etc/init.d'.format(\
        base_build=BASE_BUILD)
LOGSTASH_LOCAL_DEFAULT_FILE = '{base_build}/logstash/logstash/etc/default'.format(\
        base_build=BASE_BUILD)
LOGSTASH_LOCAL_LOGROTATE_FILE = '{base_build}/logstash/logstash/etc/logrotate.d'.format(\
        base_build=BASE_BUILD)

""" Elasticsearch Settings """
"""Warning: the end slash ("/") is necessary"""
ELASTICSEARCH_REMOTE_CONF_FILES = '/etc/elasticsearch/'
ELASTICSEARCH_REMOTE_DEFAULT_FILE = '/etc/default/elasticsearch'
ELASTICSEARCH_REMOTE_LOGROTATE_FILE = '/etc/logrotate.d/elasticsearch'
ELASTICSEARCH_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/elasticsearch.service'
ELASTICSEARCH_REMOTE_SHARE = '/usr/share/elasticsearch/'
ELASTICSEARCH_LOCAL_CONF_FILES = '{base_build}/elasticsearch/elasticsearch/etc/elasticsearch'.format(\
        base_build=BASE_BUILD)
ELASTICSEARCH_LOCAL_SYSTEMD_FILE = '{base_build}/elasticsearch/elasticsearch/lib/systemd/system'.format(\
        base_build=BASE_BUILD)
ELASTICSEARCH_LOCAL_DEFAULT_FILE = '{base_build}/elasticsearch/elasticsearch/etc/default'.format(\
        base_build=BASE_BUILD)
ELASTICSEARCH_LOCAL_LOGROTATE_FILE = '{base_build}/elasticsearch/elasticsearch/etc/logrotate.d'.format(\
        base_build=BASE_BUILD)
ELASTICSEARCH_LOCAL_SHARE = '{base_build}/elasticsearch/elasticsearch/usr/share/elasticsearch'.format(\
        base_build=BASE_BUILD)

""" Curator Settings """
"""Warning: the end slash ("/") is necessary"""
CURATOR_REMOTE_CONF_FILES = '/opt/elasticsearch-curator/'
CURATOR_REMOTE_CRON_FILES = '/var/spool/cron/crontabs/curator'
CURATOR_REMOTE_LOGROTATE_FILE = '/etc/logrotate.d/elasticsearch-curator'
CURATOR_LOCAL_CONF_FILES = '{base_build}/curator/curator/opt/elasticsearch-curator'.format(\
        base_build=BASE_BUILD)
CURATOR_LOCAL_CRON_FILES = '{base_build}/curator/curator/var/spool/cron/crontabs/curator'.format(\
        base_build=BASE_BUILD)
CURATOR_LOCAL_LOGROTATE_FILES = '{base_build}/curator/curator/etc/logrotate.d/elasticsearch-curator'.format(\
        base_build=BASE_BUILD)


""" Kibana Settings """
"""Warning: the end slash ("/") is necessary"""
KIBANA_REMOTE_CONF_FILE = '/etc/kibana/kibana.yml'
KIBANA_REMOTE_DEFAULT_FILE = '/etc/default/kibana'
KIBANA_REMOTE_LOGROTATE_FILE = '/etc/logrotate.d/kibana'
KIBANA_REMOTE_INIT_FILE = '/etc/init.d/kibana'
KIBANA_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/kibana.service'
KIBANA_LOCAL_CONF_FILE = '{base_build}/kibana/kibana/etc/kibana'.format(\
        base_build=BASE_BUILD)
KIBANA_LOCAL_INIT_FILE = '{base_build}/kibana/kibana/etc/init.d'.format(\
        base_build=BASE_BUILD)
KIBANA_LOCAL_SYSTEMD_FILE = '{base_build}/kibana/kibana/lib/systemd/system'.format(\
        base_build=BASE_BUILD)
KIBANA_LOCAL_DEFAULT_FILE = '{base_build}/kibana/kibana/etc/default'.format(\
        base_build=BASE_BUILD)
KIBANA_LOCAL_LOGROTATE_FILE = '{base_build}/kibana/kibana/etc/logrotate.d'.format(\
        base_build=BASE_BUILD)

""" Centreon Settings """
"""Warning: the end slash ("/") is necessary"""
CENTREON_REMOTE_CONF_FILE = '/usr/local/nagios/etc/nrpe.cfg'
CENTREON_LOCAL_CONF_FILE = '{base_build}/centreon/centreon/usr/local/nagios/etc'.format(\
        base_build=BASE_BUILD)

""" VerneMQ Settings """
"""Warning: the end slash ("/") is necessary"""
VERNEMQ_REMOTE_CONF_FILES = '/etc/vernemq/'
VERNEMQ_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/vernemq.service'
VERNEMQ_REMOTE_INITD = '/etc/init.d/vernemq'
VERNEMQ_REMOTE_SHARE = '/usr/share/vernemq/'
VERNEMQ_LOCAL_CONF_FILES = '{base_build}/vernemq/vernemq/etc/vernemq'.format(\
        base_build=BASE_BUILD)
VERNEMQ_LOCAL_SYSTEMD_FILE = '{base_build}/vernemq/vernemq/lib/systemd/system'.format(\
        base_build=BASE_BUILD)
VERNEMQ_LOCAL_INITD = '{base_build}/vernemq/vernemq/etc/init.d/vernemq'.format(\
        base_build=BASE_BUILD)
VERNEMQ_LOCAL_SHARE = '{base_build}/vernemq/vernemq/usr/share/vernemq'.format(\
        base_build=BASE_BUILD)

""" Haproxy Settings """
"""Warning: the end slash ("/") is necessary"""
HAPROXY_REMOTE_CONF_FILES = '/etc/haproxy/'
HAPROXY_REMOTE_DEFAULT_FILE = '/etc/default/haproxy'
HAPROXY_REMOTE_LOGROTATE_FILE = '/etc/logrotate.d/haproxy'
HAPROXY_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/haproxy.service'
HAPROXY_REMOTE_RSYSLOG = '/etc/rsyslog.d/49-haproxy.conf'
HAPROXY_LOCAL_CONF_FILES = '{base_build}/haproxy/haproxy/etc/haproxy'.format(\
        base_build=BASE_BUILD)
HAPROXY_LOCAL_SYSTEMD_FILE = '{base_build}/haproxy/haproxy/lib/systemd/system'.format(\
        base_build=BASE_BUILD)
HAPROXY_LOCAL_DEFAULT_FILE = '{base_build}/haproxy/haproxy/etc/default'.format(\
        base_build=BASE_BUILD)
HAPROXY_LOCAL_LOGROTATE_FILE = '{base_build}/haproxy/haproxy/etc/logrotate.d'.format(\
        base_build=BASE_BUILD)
HAPROXY_LOCAL_RSYSLOG = '{base_build}/haproxy/haproxy/etc/rsyslog.d'.format(\
        base_build=BASE_BUILD)

""" DNSmasq Settings """
"""Warning: the end slash ("/") is necessary"""
DNSMASQ_REMOTE_CONF_FILE = '/etc/dnsmasq.conf'
DNSMASQ_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/dnsmasq.service'
DNSMASQ_REMOTE_LOGROTATE = '/etc/logrotate.d/dnsmasq'
DNSMASQ_LOCAL_LOGROTATE = '{base_build}/dnsmasq/dnsmasq/etc/logrotate.d/dnsmasq'.format(\
        base_build=BASE_BUILD)
DNSMASQ_LOCAL_CONF_FILE = '{base_build}/dnsmasq/dnsmasq/etc'.format(\
        base_build=BASE_BUILD)
DNSMASQ_LOCAL_SYSTEMD_FILE = '{base_build}/dnsmasq/dnsmasq/lib/systemd/system'.format(\
        base_build=BASE_BUILD)

""" Apache NiFi Settings """
"""Warning: the end slash ("/") is necessary"""
NIFI_REMOTE_CONF_FILES = '/opt/nifi/conf/'
NIFI_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/nifi.service'
NIFI_REMOTE_SSL_TRUSTORE = '/opt/nifi/ssl/nificluster_trustore.jks'
NIFI_REMOTE_FLOW_FILE = '/opt/store/nifi/flows/flow.xml.gz'
NIFI_LOCAL_CONF_FILES = '{base_build}/nifi/nifi/opt/nifi/conf'.format(\
        base_build=BASE_BUILD)
NIFI_LOCAL_SYSTEMD_FILE = '{base_build}/nifi/nifi/lib/systemd/system'.format(\
        base_build=BASE_BUILD)
NIFI_LOCAL_SSL_TRUSTORE = '{base_build}/nifi/nifi/opt/nifi/ssl'.format(\
        base_build=BASE_BUILD)
NIFI_LOCAL_FLOW_FILE = '{base_build}/nifi/nifi/opt/store/nifi/flows/'.format(\
        base_build=BASE_BUILD)

""" Apache NiFi-Registry Settings """
"""Warning: the end slash ("/") is necessary"""
NIFI_REGISTRY_REMOTE_CONF_FILES = '/opt/nifi-registry/conf/'
NIFI_REGISTRY_REMOTE_SSL_TRUSTORE = '/opt/nifi-registry/ssl/nificluster_trustore.jks'
NIFI_REGISTRY_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/nifi-registry.service'
NIFI_REGISTRY_LOCAL_CONF_FILES = '{base_build}/nifi-registry/nifi-registry/opt/nifi-registry/conf'.format(\
        base_build=BASE_BUILD)
NIFI_REGISTRY_LOCAL_SSL_TRUSTORE = '{base_build}/nifi-registry/nifi-registry/opt/nifi-registry/ssl'.format(\
        base_build=BASE_BUILD)
NIFI_REGISTRY_LOCAL_SYSTEMD_FILE = '{base_build}/nifi-registry/nifi-registry/lib/systemd/system'.format(\
        base_build=BASE_BUILD)

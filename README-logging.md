## Logging Pipeline

### Nginx

1.  Add config files to define a JSON log format and `logfmt` log format.
2.  By convention, nginx config files are placed in /etc/nginx/conf.d and then `include`d in the main nginx.conf file.
    So, in your project define a `nginx/conf/conf.d` directory to contain these files.
3.  Modify the base `nginx.conf` file to add two things:
    - include the files:  `include /etc/nginx/conf.d/json_format.conf;` and another include for `logfmt_format.conf`
    - designate one as log format: `access_log  /dev/stdout json_combined;`

### Loki

Loki provides log processing, storage, and query capability.  Define a service (container) for it
using the `grafana/loki` image on Dockerhub.

> Dockerhub also has a plain `loki` image that is "hardened". Once logging works well, try that.

### Promtail

Promtail is a "log shipper".  It will read Nginx's logs, reformat some fields, and ship to the Loki container.

## Run Containers and View Logs

Start containers.  If you have old containers, it may help to remove them using "compose down".
```
docker compose up -d
```

Query Loki using the LogQL API. This is the only readable way to directly access Loki data.
 
```shell
curl -G http://localhost:3100/loki/api/v1/query_range \
  --data-urlencode 'query={container="nginx"}' \
  --data-urlencode 'limit=10'
```

or enter it in a web browser:
```
http://localhost:3100/loki/api/v1/query_range?query=%7Bcontainer%3D%22nginx%22%7D&limit=10
```


### To Do

1.  Try **Vector** instead of Promtail.  It appears to be more efficient.
2.  Consider whether it is better to put the log shipper (Promtail or Vector) in same container as Nginx.
3.  Compare OpenSearch to Loki.  OpenSearch may have more useful query capabilities.

### Labeling of Logs

This example uses conventional labels for the components of an Nginx log entry.

Where are these defined?

Does OpenTelemetry define labels for HTTP server log data?
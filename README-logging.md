## Logging Pipeline

### Nginx

1.  Add config files to define a JSON log format and `logfmt` log format.
2.  By convention, nginx config files are placed in /etc/nginx/conf.d and then `include`d in the main nginx.conf file.
    So, in your project define a `nginx/conf/conf.d` directory to contain these files.
3.  Modify the base `nginx.conf` file to add two things:
    - include the files:  `include /etc/nginx/conf.d/json_format.conf;` and another include for `logfmt_format.conf`
    - designate one as log format: `access_log  /dev/stdout json_combined;`

### Promtail

Promtail is a "log shipper".  It will read Nginx's logs, reformat some fields, 
and push them to the Loki container.

### Loki

Loki provides log processing, storage, and query capability.  Define a service (container) for it
using the `grafana/loki` image on Dockerhub.

> Dockerhub also has a plain `loki` image that is "hardened". Once logging works well, try that.

### Grafana

Grafana retrieves data from Loki (defined as a "datasource" in `grafana/provisioning/datasources/loki`)

Use Grafana to interactively view and query logs from multiple sources.

If metrics or traces are available, use Grafana to view, query, or monitor those as well.


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

### Step-by-step Debugging

> To get the **container names** use `compose ps` or `docker ps` to Docker Desktop UI.

If you don't see logs, try this:

1.  Verify **nginx** is emitting logs in JSON format:
    ```
    docker logs <nginx-container-name>
    ```

2.  Verify Promtail is receiving logs:
    ```
    docker logs <promtail-container>
    ```

3.  Verify the log file path exists in the Promtail container:
    ```
    docker exec -it <promtail-container> ls /var/lib/docker/containers
    ```

### To Do

1.  Try **Vector** instead of Promtail.  It appears to be more efficient.
2.  Consider whether it is better to put the log shipper (Promtail or Vector) in same container as Nginx.
3.  Compare OpenSearch to Loki.  OpenSearch may have more useful query capabilities.
4.  Limit access to Loki and Grafana.
5.  For Grafana, use Nginx as a proxy and restrict access via Nginx.
    - Grafana is for use by staff in visualizing data, not for end users.
    - Hence, Grafana may run on a separate server or be behind a separate Nginx proxy.



### Labeling of Logs

This example uses conventional labels for the components of an Nginx log entry.

Where are these defined?

Does OpenTelemetry define labels for HTTP server log data?
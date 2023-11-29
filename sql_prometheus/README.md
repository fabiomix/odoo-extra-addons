# SQL Prometheus
Define high-level application metrics for Prometheus using SQL query.

## Features
This module is used to generate Prometheus-compatible metrics through SQL
queries.  The metrics are at application/instance level (number of users,
pickings delivered, ongoing production orders, etc.) and NOT system metrics
(resources used, average http response time, etc.).

Each row of the query result generates a metric, and the extra columns are
converted into labels.

### Example
This query can be used to track the status of queue.job asynchronous tasks,
to monitor spikes in errors or slowdowns.

```sql
SELECT state, channel, COUNT(id) AS value
FROM queue_job
WHERE state != 'done'
GROUP BY state, channel
ORDER BY state, channel;
```

### Output
```
odoo_queue_job_count{state="failed",channel="root.ch_1"} 5
odoo_queue_job_count{state="failed",channel="root.ch_2"} 4
odoo_queue_job_count{state="pending",channel="root.ch_1"} 17
odoo_queue_job_count{state="pending",channel="root.ch_2"} 13
odoo_queue_job_count{state="started",channel="root.ch_1"} 1
odoo_queue_job_count{state="started",channel="root.ch_2"} 1
```

## Known issues / Roadmap
- migrate to the official Prometheus Python client library
- export basic system metrics
- missing feedback if the test button doesn't raise errors

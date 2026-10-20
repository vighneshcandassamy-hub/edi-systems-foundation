# Operating-envelope assessment

## Workload

Define offered input, accepted work, bytes, samples, records/batches, source count/cardinality, payload distribution, bursts, history size, read/query mix, optional model work, retention and fault conditions. Record hardware, OS, backend, runtime/configuration and version before reporting measurements. Separate target, analytical estimate, simulation and measured result.

## Time and resource cost

Count queueing, transfer, parsing, model invocation, persistence barriers and retries in the latency boundary. Report tail percentiles as well as throughput; distinguish complete artifact latency from chunk latency. Bound RAM, disk spool, candidate search, graph expansion and recursive parsing. Include checkpointing, compaction, index building, restoration and long-term growth.

Approximate backlog growth as max(0, arrival - service) * time in consistent units. Estimate spool from input bytes/s * supported outage plus overhead/reserve. Estimate retained storage from bytes/s * retention * replica factor, then add metadata/indexes and measured compression. Averages hide bursts and hot sources.

## Tokens and learned processing

Count mandatory and optional model calls separately. A reasoning component may legitimately require substantial inference; justify it against its own purpose. Zero mandatory observation-path tokens does not imply zero total cost or lower downstream task tokens. For comparative claims include prompts, retrieved content, images/audio, tool results, failed calls, retries and context reconstruction on matched tasks. Measure energy/compute separately rather than infer them from token count.

## Availability and durability

Separate availability, correctness, durability, freshness and recoverability. State requested acknowledgement level, failure domains, failover authority/fencing, replication coverage, RPO/RTO and backups. A single host with backup is a recovery profile, not automatically HA. Database replication does not automatically protect independent payloads. State partition behavior and which operations can remain available.

Define SLI denominators prospectively. Count eligible offered requests that fail, time out or are rejected within capacity as failures; do not remove them to improve the result. Include client-side probes so server silence does not erase outages. An SLO is a target over a window, not a result from one short run.

## Expansion

Use qualified capacity profiles, not unlimited-scale promises. Identify partition keys, hot-source handling, ordering scope, cross-shard operations, authority and historical retrieval cost. Add infrastructure only after measured need or an explicit resilience requirement. State a scaling discriminator and its fixed per-node resource/latency/fidelity conditions. Preserve semantics when changing backend or topology.

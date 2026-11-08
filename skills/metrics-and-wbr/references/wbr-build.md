# Building the WBR yourself, with agents (appendix for builders)

This is for whoever builds the pipeline. A PM running the WBR does not need it.

This pattern runs in production for a two-person company. Follow the steps in order:

1. **PR/FAQ for the warehouse** (`working-backwards` skill). Answer "Why not a BI tool like Looker?" in the FAQ. The usual answer: a GUI tool can't be built or changed by an agent, and a data hire isn't justified yet.
2. **Metrics taxonomy.** One row per metric, with these columns:
   - audience
   - lifecycle stage
   - category
   - metric
   - definition
   - why it matters
   - calculation
   - data source
   - target, RAG level and direction
   - chart type
   - priority (Now / Later / Future)
   - reporting layer
   - owner
   - notes

   At company scale, aim for 120–180 metrics with 40–60 marked Now. **A pre-launch micro-team should mark 10–15 as Now.** Validate it in code. Any metric without a data source gets `NEEDS INSTRUMENTATION`. Put the gaps on a heatmap, which becomes the tracking backlog.
3. **Data-source map.** Have an agent read the production schema and map every metric to the table and column it comes from. Flag the traps, e.g. values that are derived rather than stored, or duplicate IDs.
4. **Warehouse.** Sync production tables nightly into a separate analytics database. Model them with dbt in three layers: staging → intermediate → marts, one mart per WBR section. Add shared macros: period-over-period and a date spine.
5. **Pipeline.** Run it on a schedule: sync → dbt run → dbt test. Stop on any failure. Show a "data is stale" panel instead of wrong numbers.
6. **One metric registry.** Keep chart type, targets and RAG thresholds in ONE config that both the backend and the UI read. Hand-copying it between YAML and TypeScript drifts.
7. **Portal.** Use the same layout every week:
   - each chart shows 6 weeks next to 12 months, with the prior year overlaid
   - each metric has a callout row: last week, week-on-week, YoY, MTD, QTD, YTD, plus their YoY comparisons
   - a RAG badge against the target
8. **Next level (specify before building):**
   - an exceptions page listing anomalies against the normal range
   - forecasts
   - alerts that pull the "Andon cord" in Slack
   - an LLM-drafted callout narrative with a *hypothesis* for each exception, for the metric owner to edit, never to publish unedited

**At scale** (100+ metrics):
- **Ingestion:** one ingest base class with a connector per source (app database via schema discovery, Stripe, PostHog, GA4, ads, Zendesk, video, Jira). Each lands as Parquet in object storage, then loads into raw warehouse tables. A credential gate skips any source whose credentials are missing.
- **dbt layers:** staging → intermediate → marts → **export**, with one model per metric carrying its weekly and monthly series, callouts and RAG → curated **ask** views behind a read-only role.
- **Metric registry:** a seed CSV holding key, category, priority, chart type, target / acceptable / poor, invert flag, seasonal flag and unit. Seasonal thresholds live in their own seed. Leave targets as *draft* until someone owns them. Never invent them.
- **Guard:** a freshness check, an empty-table check and a metric-count tripwire, all run before export. Failures alert Slack.
- **Serving:** export per-metric JSON plus a manifest to a CDN. The UI reads static files, so there's no live query load on the warehouse.
- **AI layers:**
  1. a weekly briefing draft (tldr, highlights, lowlights, asks, next focus) built from the WBR plus Slack, GitHub and Jira. A human edits and publishes it.
  2. "Ask AI": natural language → catalogue selection → deterministic SQL compile → validator → read-only role, with every figure checked against the data (grounding).

**Gaps worth building next:** anomaly detection, forecasts, hypothesis callouts, an exceptions page, and an input/output label on every metric.

Agents write the SQL, the pipeline and the charts. Humans own the spec, the targets and the hypotheses.


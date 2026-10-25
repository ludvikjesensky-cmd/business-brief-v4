-- Business Brief v4: covering indexes for Fast Editorial v1 foreign keys.

create index if not exists fast_editorial_issues_edition_idx
  on fast_editorial.issues(edition_id) where edition_id is not null;
create index if not exists fast_editorial_issues_source_idx
  on fast_editorial.issues(source_id) where source_id is not null;
create index if not exists fast_editorial_issues_frozen_snapshot_idx
  on fast_editorial.issues(frozen_snapshot_id) where frozen_snapshot_id is not null;
create index if not exists fast_editorial_topic_sources_item_idx
  on fast_editorial.topic_sources(issue_item_id);
create index if not exists fast_editorial_deep_read_day_idx
  on fast_editorial.deep_read_notes(day_id);
create index if not exists fast_editorial_brief_topics_topic_idx
  on fast_editorial.brief_topics(topic_id);
create index if not exists fast_editorial_brief_issues_issue_idx
  on fast_editorial.brief_issues(issue_id);
create index if not exists fast_editorial_notes_issue_idx
  on fast_editorial.editorial_notes(issue_id) where issue_id is not null;
create index if not exists fast_editorial_notes_topic_idx
  on fast_editorial.editorial_notes(topic_id) where topic_id is not null;
create index if not exists fast_editorial_notes_brief_idx
  on fast_editorial.editorial_notes(brief_id) where brief_id is not null;
create index if not exists fast_editorial_artifacts_issue_idx
  on fast_editorial.artifacts(issue_id) where issue_id is not null;
create index if not exists fast_editorial_artifacts_topic_idx
  on fast_editorial.artifacts(topic_id) where topic_id is not null;
create index if not exists fast_editorial_artifacts_brief_idx
  on fast_editorial.artifacts(brief_id) where brief_id is not null;
create index if not exists fast_editorial_handover_verified_brief_idx
  on fast_editorial.handover_state(last_verified_brief_id)
  where last_verified_brief_id is not null;

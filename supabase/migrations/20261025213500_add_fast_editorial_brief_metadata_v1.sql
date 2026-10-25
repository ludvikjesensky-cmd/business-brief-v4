-- Business Brief v4: queryable Master Brief metadata v1.

alter table fast_editorial.briefs
  add column if not exists title text,
  add column if not exists deck text,
  add column if not exists language text not null default 'cs'
    check (btrim(language) <> ''),
  add column if not exists editorial_summary text;

comment on column fast_editorial.briefs.title is
'Queryable reader-facing title for this exact Master Editorial Truth version.';
comment on column fast_editorial.briefs.deck is
'Queryable reader-facing deck/subtitle for this exact Master Editorial Truth version.';
comment on column fast_editorial.briefs.language is
'Primary language of the Master Editorial Truth version.';
comment on column fast_editorial.briefs.editorial_summary is
'Short operational/editorial summary of the verified Brief version; not a substitute for the full Master Editorial Truth.';

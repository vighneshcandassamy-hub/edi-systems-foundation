
PRAGMA foreign_keys=ON;
CREATE TABLE corpus_meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE sources(source_id TEXT PRIMARY KEY,title TEXT NOT NULL,publisher TEXT NOT NULL,source_url TEXT NOT NULL,license_note TEXT NOT NULL,role TEXT NOT NULL,scope_note TEXT NOT NULL);
CREATE TABLE knowledge_areas(area_id TEXT PRIMARY KEY,description TEXT NOT NULL);
CREATE TABLE evidence_files(file_id TEXT PRIMARY KEY,path TEXT UNIQUE NOT NULL,source_id TEXT NOT NULL REFERENCES sources,sha256 TEXT NOT NULL,size_bytes INTEGER NOT NULL,format TEXT NOT NULL,origin TEXT NOT NULL,role TEXT NOT NULL,description TEXT NOT NULL,retrieved_at TEXT NOT NULL,root_evidence_group TEXT NOT NULL);
CREATE TABLE file_areas(file_id TEXT REFERENCES evidence_files,area_id TEXT REFERENCES knowledge_areas,PRIMARY KEY(file_id,area_id));
CREATE TABLE lineage(child_file_id TEXT REFERENCES evidence_files,parent_file_id TEXT REFERENCES evidence_files,relation TEXT NOT NULL,details TEXT NOT NULL,PRIMARY KEY(child_file_id,parent_file_id));
CREATE TABLE records(record_id TEXT PRIMARY KEY,file_id TEXT NOT NULL REFERENCES evidence_files,selector TEXT NOT NULL,series TEXT NOT NULL,event_time TEXT,event_year INTEGER,latitude REAL,longitude REAL,payload_json TEXT NOT NULL,UNIQUE(file_id,selector));
CREATE INDEX records_series_time ON records(series,event_time);
CREATE INDEX records_year ON records(event_year);
CREATE INDEX records_location ON records(latitude,longitude);
CREATE TABLE text_blocks(block_id TEXT PRIMARY KEY,file_id TEXT NOT NULL REFERENCES evidence_files,selector TEXT NOT NULL,text TEXT NOT NULL,role TEXT NOT NULL);
CREATE VIRTUAL TABLE text_search USING fts5(block_id UNINDEXED,file_id UNINDEXED,text);
CREATE TABLE evidence_gaps(gap_id TEXT PRIMARY KEY,area_id TEXT REFERENCES knowledge_areas,description TEXT NOT NULL,consequence TEXT NOT NULL);
CREATE VIEW observation_files AS SELECT * FROM evidence_files WHERE role='observation';
CREATE VIEW reference_files AS SELECT * FROM evidence_files WHERE role='reference';

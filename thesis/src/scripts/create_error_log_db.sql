-- Comandos para SQlite
-- cat $SRC/scripts/create_error_log_db.sql  | sqlite3 $BIOSCOPE/bioscope.db

create table hc_learning_errors_heldout  (
	document_id text,
	sentence_id text,
	run integer,
primary key (document_id,sentence_id,run)
);

create index i_hc_learning_errors_heldout1 on hc_learning_errors_heldout (run);

create table hc_learning_errors  (
	document_id text,
	sentence_id text,
	run integer,
primary key (document_id,sentence_id,run)
);

create index i_hc_learning_errors1 on hc_learning_errors (run);

create table scope_learning_errors_heldout  (
	document_id text,
	sentence_id text,
	hc_start integer,
	runx integer,
primary key (document_id,sentence_id,hc_start,runx)
);

create index i_scope_learning_errors_heldout1 on scope_learning_errors_heldout (runx);

create table scope_learning_errors  (
	document_id text,
	sentence_id text,
	hc_start integer,
	runx integer,
primary key (document_id,sentence_id,hc_start,runx)
);

create index i_scope_learning_errors1 on scope_learning_errors (runx);


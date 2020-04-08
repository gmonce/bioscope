-- Comandos para SQlite
-- cat $SRC/scripts/create_db.sql  | sqlite3 $BIOSCOPE/bioscope.db

drop table if exists bioscope_train;
drop table if exists bioscope_test;

-- Tabla principal para el corpus de entrenamiento
create table bioscope_train (
document_id text, -- identificador del documento
sentence_id text, -- identificador de la oracion
token_num integer, -- número de token dentro de la oración 
sentence_type char, -- TRAIN o TEST, para la división del corpus de entrenamiento sacando el corpus held out 
word text, -- token
lemma text, -- lemma del token, 
POS text, 
CHUNK text, --  resultado del chunker
NER text, -- proteína, gen, etc., 
hedge_cue text, -- marca de especulacion (B-SPECCUE, I_SPECCUE, O)
hedge_cue1 text, -- marca de especulación, pero reflejando marcas anidadas
hedge_cue2 text, 
hedge_cue3 text, 
hedge_scope1 text,-- alcance de la primer marca de especulación
hedge_scope2 text,-- alcance de la segunda marca (si está anidada)
hedge_scope3 text,-- alcance de la tercera marca (si está anidada)
guessed_hedge_cue text, -- guessed hedge cue, only for the TEST sentences
guessed_hc_token_guess_confidence real, -- confidence in hedge cue guessing, for each token
guessed_hc_seq_guess_confidence real, -- confidence in hedge cue guessing, for the whole sentence 
primary key (document_id,sentence_id,token_num));

create index i_bioscope_train1 on bioscope_train (word);



-- Tabla principal para el corpus de evaluación
create table bioscope_test (
document_id text, -- identificador del documento
sentence_id text, -- identificador de la oracion
token_num integer, -- número de token dentro de la oración 
word text, -- token
lemma text, -- lemma del token, 
POS text, 
CHUNK text, --  resultado del chunker
NER text, -- proteína, gen, etc., 
hedge_cue text, -- marca de especulacion (B-SPECCUE, I_SPECCUE, O)
hedge_cue1 text, -- marca de especulación, pero reflejando marcas anidadas
hedge_cue2 text, 
hedge_cue3 text, 
hedge_scope1 text,-- alcance de la primer marca de especulación
hedge_scope2 text,-- alcance de la segunda marca (si está anidada)
hedge_scope3 text,-- alcance de la tercera marca (si está anidada)
guessed_hedge_cue text, -- guessed hedge cue, only for the TEST sentences
guessed_hc_token_guess_confidence real, -- confidence in hedge cue guessing, for each token
guessed_hc_seq_guess_confidence real, -- confidence in hedge cue guessing, for the whole sentence 
primary key (document_id,sentence_id,token_num));

create index i_bioscope_test1 on bioscope_test (word);


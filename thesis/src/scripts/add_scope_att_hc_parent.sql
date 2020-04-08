-- Comandos para SQlite
-- Agrega las columnas para el atributo HC parent, en las tablas de scope
-- Ojo que esto se pierde si se regeneran
-- cat add_att_hc_parent.sql  | sqlite3 $BIOSCOPE/bioscope_devel/attributes.db

alter table bioscope80_scope add column hc_parent_POS text; -- POS del padre del primer token de la hedge cue 
alter table bioscope80_scope add column in_hc_parent_scope text ; -- Y/N: indica si el token está dentro del scope del padre del primer token de la hedge cue
alter table bioscope80_scope add column scope_2 text ; -- scope que en lugar de F tiene una X si coincide con el alcance del padre de la hc
alter table bioscope80_scope add column hc_gparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope80_scope add column in_hc_gparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope80_scope add column hc_ggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope80_scope add column in_hc_ggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope80_scope add column in_nextS_scope text ; -- Y/N: indica si el token está dentro del scope del próximo S o SBAR
alter table bioscope80_scope add column passive_voice text; --Y/N: indica si hay una voz pasiva asociada al hedge
alter table bioscope80_scope add column hc_gggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope80_scope add column in_hc_gggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue



alter table bioscope20_scope add column hc_parent_POS text; -- POS del padre del primer token de la hedge cue 
alter table bioscope20_scope add column in_hc_parent_scope text ; -- Y/N: indica si el token está dentro del scope del padre del primer token de la hedge cue
alter table bioscope20_scope add column hc_gparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope20_scope add column in_hc_gparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope20_scope add column hc_ggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope20_scope add column in_hc_ggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope20_scope add column in_nextS_scope text ; -- Y/N: indica si el token está dentro del scope del próximo S o SBAR
alter table bioscope20_scope add column passive_voice text; --Y/N: indica si hay una voz pasiva asociada al hedge
alter table bioscope20_scope add column hc_gggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope20_scope add column in_hc_gggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue

alter table bioscope20_ghc_scope add column hc_parent_POS text; -- POS del padre del primer token de la hedge cue 
alter table bioscope20_ghc_scope add column in_hc_parent_scope text ; -- Y/N: indica si el token está dentro del scope del padre del primer token de la hedge cue
alter table bioscope20_ghc_scope add column hc_gparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope20_ghc_scope add column in_hc_gparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope20_ghc_scope add column hc_ggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope20_ghc_scope add column in_hc_ggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope20_ghc_scope add column in_nextS_scope text ; -- Y/N: indica si el token está dentro del scope del próximo S o SBAR
alter table bioscope20_ghc_scope add column passive_voice text; --Y/N: indica si hay una voz pasiva asociada al hedge
alter table bioscope20_ghc_scope add column hc_gggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope20_ghc_scope add column in_hc_gggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue


alter table bioscope_train_scope add column hc_parent_POS text; -- POS del padre del primer token de la hedge cue 
alter table bioscope_train_scope add column in_hc_parent_scope text ; -- Y/N: indica si el token está dentro del scope del padre del primer token de la hedge cue
alter table bioscope_train_scope add column scope_2 text ; -- scope que en lugar de F tiene una X si coincide con el alcance del padre de la hc
alter table bioscope_train_scope add column hc_gparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope_train_scope add column in_hc_gparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope_train_scope add column hc_ggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope_train_scope add column in_hc_ggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope_train_scope add column in_nextS_scope text ; -- Y/N: indica si el token está dentro del scope del próximo S o SBAR
alter table bioscope_train_scope add column passive_voice text; --Y/N: indica si hay una voz pasiva asociada al hedge
alter table bioscope_train_scope add column hc_gggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope_train_scope add column in_hc_gggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue


alter table bioscope_test_scope add column hc_parent_POS text; -- POS del padre del primer token de la hedge cue 
alter table bioscope_test_scope add column in_hc_parent_scope text ; -- Y/N: indica si el token está dentro del scope del padre del primer token de la hedge cue
alter table bioscope_test_scope add column hc_gparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope_test_scope add column in_hc_gparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope_test_scope add column hc_ggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope_test_scope add column in_hc_ggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope_test_scope add column in_nextS_scope text ; -- Y/N: indica si el token está dentro del scope del próximo S o SBAR
alter table bioscope_test_scope add column passive_voice text; --Y/N: indica si hay una voz pasiva asociada al hedge
alter table bioscope_test_scope add column hc_gggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope_test_scope add column in_hc_gggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue

alter table bioscope_test_ghc_scope add column hc_parent_POS text; -- POS del padre del primer token de la hedge cue 
alter table bioscope_test_ghc_scope add column in_hc_parent_scope text ; -- Y/N: indica si el token está dentro del scope del padre del primer token de la hedge cue
alter table bioscope_test_ghc_scope add column hc_gparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope_test_ghc_scope add column in_hc_gparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope_test_ghc_scope add column hc_ggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope_test_ghc_scope add column in_hc_ggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue
alter table bioscope_test_ghc_scope add column in_nextS_scope text ; -- Y/N: indica si el token está dentro del scope del próximo S o SBAR
alter table bioscope_test_ghc_scope add column passive_voice text; --Y/N: indica si hay una voz pasiva asociada al hedge
alter table bioscope_test_ghc_scope add column hc_gggparent_POS text; -- POS del abuelo del primer token de la hedge cue 
alter table bioscope_test_ghc_scope add column in_hc_gggparent_scope text ; -- Y/N: indica si el token está dentro del scope del abuelo del primer token de la hedge cue

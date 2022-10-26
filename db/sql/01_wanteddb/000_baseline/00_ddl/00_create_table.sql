\c wanted_db

create table "company" (
  "id" serial primary key
  ,"company_ko" varchar(50)
  , "company_en" varchar(50)
  , "company_ja" varchar(50)
  , "tag_ko" varchar(50)
  , "tag_en" varchar(50)
  , "tag_ja" varchar(50)
  , "company_tw" varchar(50)
  , "tag_tw" varchar(50)
) ;
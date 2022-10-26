\c wanted_db

-- エリアマスタ
\COPY company ("id","company_ko","company_en","company_ja","tag_ko","tag_en","tag_ja","company_tw","tag_tw") FROM '/docker-entrypoint-initdb.d/01_wanteddb/000_baseline/01_common/csv/company.csv' WITH CSV HEADER
#PostgreSQL
library(RPostgreSQL)

conn <- dbConnect(drv = 'PostgreSQL', host='localhost' , user= "postgres", password="101010", dbname="postgres", port=5432)

dbGetQuery(conn, "create schema CT_DB;")
dbGetQuery(conn, "set search_path = 'ct_db'")

#read table
dbReadTable(conn, "")

#save tble
dbWriteTable(conn, "")



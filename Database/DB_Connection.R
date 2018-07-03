#PostgreSQL
library(RPostgreSQL)

conn <- dbConnect(drv = 'PostgreSQL', host='localhost' , user= "postgres", password="*****", dbname="postgres", port=5432)

dbGetQuery(conn, "create schema schema_name;")
dbGetQuery(conn, "set search_path = '*****'")

#read table
dbReadTable(conn, "")

#save tble
dbWriteTable(conn, "")



#! /bin/bash
docker run -d --rm \
  --name dc_db \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_USER=admin \
  -e POSTGRES_DB=dc_db \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v /home/ernestlwt/data/dc_data/pgdata:/var/lib/postgresql/data/pgdata \
  postgres



## local test


### .local.env
```
MYSQL_HOST=db
MYSQL_PORT=3306
DATABASE_NAME=x-fit
MYSQL_ROOT_USER=root
MYSQL_ROOT_PASSWORD=x-fit

```
### docker compose

```
docker compose -f docker-compose-local.yml build
docker compose -f docker-compose-local.yml up -d


```

## dev test

### .dev.env
```
MYSQL_HOST=x-fit-dev.c9guns9brwvr.ap-northeast-2.rds.amazonaws.com
MYSQL_PORT=3306
DATABASE_NAME=x-fit
MYSQL_ROOT_USER=root
MYSQL_ROOT_PASSWORD=

```


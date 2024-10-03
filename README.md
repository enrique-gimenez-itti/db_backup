## commands
Hay dos formas de correr este proceso:

```
docker compose -d --build
```

o manualmente:

1. Backup
```
mysqldump --protocol=TCP --host={SOURCE_HOST} --port={SOURCE_PORT} --user={SOURCE_USER}--password={SOURCE_PASS} {SOURCE_DB} > {DEST_DIRECTORY}
```

2. Restore 
```
❯ mysql --protocol=TCP --host={DEST_HOST} --port={DEST_PORT} --user={DEST_USER} --password={DEST_PASS} {DEST_DB} < {BACKUP_FILE}
```
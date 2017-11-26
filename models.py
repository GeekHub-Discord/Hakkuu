import config
from peewee import *
import pymysql
from playhouse.shortcuts import RetryOperationalError

cfg = config.botConfig()

class MySQLDB(RetryOperationalError, MySQLDatabase):
    pass

class SqliteDB(SqliteDatabase):
    pass

if cfg.dbtype == 'sqlite':
    my_db = SqliteDB(f'{cfg.database}.db')
else:
    my_db = MySQLDB(
            cfg.database,
            host=cfg.dbhost,
            port=3306,
            user=cfg.dbuser,
            password=cfg.dbpasswd,
            charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = my_db


class Message(BaseModel):
    snowflake = BigIntegerField(null=False, primary_key=True)
    author = BigIntegerField(null=False)
    content = CharField(max_length=2000)
    deleted = BooleanField(null=False, default=False)
    deleted_by = BigIntegerField(null=True)


my_db.create_tables(
    [Message],
    safe=True)

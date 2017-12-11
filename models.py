from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute,
    MapAttribute, ListAttribute, BooleanAttribute
)


class LogRevision(MapAttribute):
    content = UnicodeAttribute(null=False)
    timestamp = UTCDateTimeAttribute()
    pinned = BooleanAttribute()


class LogEmbed(MapAttribute):
    title = UnicodeAttribute(null=True)
    em_type = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=True)
    url = UnicodeAttribute(null=True)
    timestamp = UTCDateTimeAttribute()


class LogAttachment(MapAttribute):
    attachid = NumberAttribute()
    size = NumberAttribute()
    height = NumberAttribute(null=True)
    width = NumberAttribute(null=True)
    filename = UnicodeAttribute()
    url = UnicodeAttribute()


class LogMessage(Model):
    class Meta:
        table_name = 'hakkuu_message'

    guild = NumberAttribute(hash_key=True)
    snowflake = NumberAttribute(range_key=True)
    author = NumberAttribute()
    channel = NumberAttribute()
    revisions = ListAttribute(of=LogRevision)
    embeds = ListAttribute(of=LogEmbed)
    attachments = ListAttribute(of=LogAttachment)
    tts = BooleanAttribute(null=True)
    deleted = BooleanAttribute(null=True)
    deleted_by = BooleanAttribute(null=True)

class Settings(Model):
    class Meta:
        table_name = 'hakkuu_settings'

    guild = NumberAttribute(hash_key=True)
    log_channel = NumberAttribute()

if not LogMessage.exists():
    LogMessage.create_table(
        read_capacity_units=1, write_capacity_units=1, wait=True)

if not Settings.exists():
    Settings.create_table(
        read_capacity_units=1, write_capacity_units=1, wait=True)

from pynamodb.models import model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute,
    MapAttribute, ListAttribute
)


class LogRevision(MapAttribute):
    content = UnicodeAttribute()
    timestamp = UTCDateTimeAttribute()


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
    content = UnicodeAttribute()
    pinned = BooleanAttribute()
    tts = BooleanAttribute()
    deleted = BooleanAttribute(null=True)
    deleted_by = BooleanAttribute(null=True)

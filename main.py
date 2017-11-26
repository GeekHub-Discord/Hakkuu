import config
import discord
import datetime as dt
from error_handler import get_logger
from models import *

cfg = config.botConfig()

client = discord.Client()

logger = get_logger('betterlogbot')

@client.event
async def on_ready():
    # Bots ready
    logger.info(f"{client.user.name} ({client.user.id}) is now online.")


@client.event
async def on_message(message):
    m, created = Message.get_or_create(
        snowflake=message.id,
        defaults={
            'author': message.author.id,
            'content': message.content
        }
    )


@client.event
async def on_message_delete(message):
    now = dt.datetime.utcnow()
    logger.info("Updating DB")
    m, created = Message.get_or_create(
        snowflake=message.id,
        defaults={
            'author': message.author.id,
            'content': message.content,
            'deleted': True
        }
    )
    if not created:
        m.deleted = True
        m.save()
    logger.info("Grabbing audit logs")
    entries = await message.guild.audit_logs(
        limit=1,
        action=discord.AuditLogAction.message_delete
    ).flatten()
    logger.info("Audit log get!")
    entry = entries[0]
    logger.info("Now: {int(now)}, entry: {int(entry.created_at)}")
    await client.get_channel(384194130894389249).send(
        f'Message from {entry.target} deleted by {entry.user.name}: {message.content}'
    )

client.run(cfg.token)

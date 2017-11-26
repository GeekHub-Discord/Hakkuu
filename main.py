import config
import discord
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
    entries = await message.guild.audit_log(
        limit=50,
        action=discord.AuditLogAction.message_delete
    )
    logger.info("Audit log get!")
    message = entries[0].target
    print(message)

client.run(cfg.token)

import config
import discord
import datetime as dt
import dateutil.parser
import pprint
import time
from error_handler import get_logger, logexcept
from models import LogMessage, LogEmbed, LogRevision, LogAttachment, Settings

cfg = config.botConfig()

client = discord.Client()

logger = get_logger('betterlogbot')

@client.event
async def on_ready():
    # Bots ready
    logger.info(f"{client.user.name} ({client.user.id}) is now online.")

@logexcept
async def process_cmd(message):
    if not message.content.startswith(client.user.mention):
        return
    sm = message.content.split(' ')
    cmd = sm[1]
    args = sm[2:]

    # Query a single message
    if cmd == 'query':
        message_id = int(args[0])
        m = LogMessage.get(message.guild.id, message_id)
        author = message.guild.get_member(m.author)
        if not author:
            author = await client.get_user_info(m.author)
        channel = message.guild.get_channel(m.channel)
        if channel:
            channel_name = channel.name
        else:
            channel_name = 'DELETED-CHANNEL'

        em = discord.Embed(
            title='Message Info',
            type='rich'
        )
        em.set_author(
            name=f'{author.name}#{author.discriminator}'
        )

        em.add_field(name="Channel", value=f"#{channel_name}")
        if m.tts:
            em.add_field(name="TTS", value="True")
        else:
            em.add_field(name="TTS", value="False")

        if m.deleted:
            em.add_field(name="Deleted", value="True")
        else:
            em.add_field(name="Deleted", value="False")


        last_pin_status = False
        pin_status = {False: "Unpinned", True: "Pinned"}
        for r in m.revisions:
            if not r.pinned == last_pin_status:
                em.add_field(
                    name=f"{r.timestamp.strftime('%c')}",
                    value=pin_status[r.pinned],
                    inline=False)
            else:
                em.add_field(
                    name=f"{r.timestamp.strftime('%c')}",
                    value=r.content,
                    inline=False)
            last_pin_status = r.pinned
        await message.channel.send(embed=em)


@client.event
@logexcept
async def on_message(message):
    if message.author.bot:
        return
    embeds = []
    for e in message.embeds:
        embeds.append(
            LogEmbed(
                title=e.title,
                em_type=e.type,
                description=e.description,
                url=e.url,
                timestamp=e.timestamp if e.timestamp else None
            )
        )
    attachments = []
    for a in message.attachments:
        attachments.append(
            LogAttachment(
                attachid=a.id,
                size=a.size,
                height=a.height,
                width=a.width,
                filename=a.filename,
                url=a.url
            )
        )
    rev = LogRevision(
        content=message.content if message.content else None,
        timestamp=message.created_at,
        pinned=message.pinned
    )
    msg_item = LogMessage(
        guild=message.guild.id,
        snowflake=message.id,
        author=message.author.id,
        channel=message.channel.id,
        revisions=[rev],
        embeds=embeds,
        attachments=attachments,
        tts = message.tts if message.tts else None
    )
    msg_item.save()

    await process_cmd(message)


@client.event
@logexcept
async def on_raw_message_edit(message_id, data):
    channel = client.get_channel(int(data['channel_id']))
    try:
        m = LogMessage.get(channel.guild.id, message_id)
    except LogMessage.DoesNotExist as e:
        return
    try:
        ts = dateutil.parser.parse(data['edited_timestamp'])
    except KeyError as e:
        ts = dt.datetime.utcnow()
    if 'content' in data:
        rev = LogRevision(
            content=data['content'],
            timestamp=ts,
            pinned=data['pinned']
        )
    else:
        rev = LogRevision(
            timestamp=ts,
            pinned=data['pinned']
        )
    m.revisions.append(rev)
    m.save()
    # pp = pprint.PrettyPrinter(depth=4)
    # pp.pprint(data)
    s = Settings.get(channel.guild.id)
    logchannel = client.get_channel(s.log_channel)
    logchannel.send(f'Message {message_id} has been edited')



@client.event
async def on_raw_message_delete(message_id, channel_id):
    channel = client.get_channel(channel_id)
    try:
        m = LogMessage.get(channel.guild.id, message_id)
    except LogMessage.DoesNotExist as e:
        return
    if m:
        m.deleted = True
        m.save()
    s = Settings.get(channel.guild.id)
    logchannel = client.get_channel(s.log_channel)
    logchannel.send(f'Message {message_id} has been deleted')


client.run(cfg.token)

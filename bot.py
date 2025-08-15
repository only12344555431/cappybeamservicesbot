import asyncio
import discord
from discord.ext import tasks

# -----------------------
# BOT TOKEN
TOKEN = "MTQwNTkzMjI5MjkzMjc2NzgwNA.Gp4WHv.S4aqmoE_05PQKFvEZOc6XibE_R4MEHl3cmTWWc"
# Sunucular ve ses kanalları
SERVERS = {
    1376961674933829692: 1401978189802377390,  # SunucuID : Ses KanalID
    1398043289105731705: 1398044316940767333  # İkinci sunucu örnek
}
# -----------------------

INTENTS = discord.Intents.default()
INTENTS.guilds = True
INTENTS.voice_states = True

client = discord.Client(intents=INTENTS)

voice_clients = {}  # guild_id : VoiceClient

async def connect_all():
    for guild_id, channel_id in SERVERS.items():
        guild = client.get_guild(guild_id)
        if not guild:
            print(f"[WARN] Sunucu bulunamadı: {guild_id}")
            continue
        channel = guild.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            print(f"[WARN] Ses kanalı bulunamadı: {channel_id}")
            continue
        try:
            if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
                vc = await channel.connect(reconnect=True)
                voice_clients[guild_id] = vc
                print(f"[INFO] {guild.name} ses kanalına bağlandı.")
        except Exception as e:
            print(f"[ERROR] {guild.name} bağlanamadı: {e}")

@tasks.loop(seconds=60)
async def ensure_voice():
    await connect_all()

@client.event
async def on_ready():
    print(f"Giriş yapıldı: {client.user}")
    await connect_all()
    ensure_voice.start()

@client.event
async def on_voice_state_update(member, before, after):
    # Eğer bot kanaldan düşerse yeniden bağlan
    if member.id != client.user.id:
        return
    guild_id = member.guild.id
    if guild_id in SERVERS:
        if after.channel is None:
            await asyncio.sleep(3)
            guild = client.get_guild(guild_id)
            channel = guild.get_channel(SERVERS[guild_id])
            try:
                vc = await channel.connect(reconnect=True)
                voice_clients[guild_id] = vc
                print(f"[INFO] {guild.name} tekrar bağlandı.")
            except Exception as e:
                print(f"[ERROR] {guild.name} yeniden bağlanamadı: {e}")

client.run("MTQwNTkzMjI5MjkzMjc2NzgwNA.Gp4WHv.S4aqmoE_05PQKFvEZOc6XibE_R4MEHl3cmTWWc")

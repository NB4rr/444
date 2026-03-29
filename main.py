import discord
import os
import asyncio
import random

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("❌ ERROR: No TOKEN in Railway vars!")
    exit(1)

print(f"🔑 Token loaded: {TOKEN[:15]}... ({len(TOKEN)} chars)")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents, self_bot=True)

@client.event
async def on_ready():
    print(f"✅ CONNECTED: {client.user} (ID: {client.user.id})")
    print("🎉 Send <@your_id> help to test")

@client.event
async def on_message(message):
    if message.author.id == client.user.id: return
    
    content = message.content.lower()
    my_id = str(client.user.id)
    
    # Help
    if f'<@{my_id}>' in content and 'help' in content:
        embed = discord.Embed(title="🤖 SelfBot v2.0", color=0x5865F2)
        embed.set_thumbnail(url="https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif")
        embed.description = "**Voice:** `<@> join [vc_id]` | `<@> leave`\n**React:** `<@> dir @user` (ON) | `<@> 7yd @user` (OFF)\n**Text:** `<@> say hi` | `<@> spam 5 hi` | `<@> dm @user msg`"
        embed.set_footer(text="24/7 Railway • No limits")
        await message.reply(embed=embed, mention_author=False)
        return
    
    # Voice (auto or ID)
    if 'join' in content and f'<@{my_id}>' in content:
        if message.author.voice:
            vc = message.author.voice.channel
        else:
            parts = content.split()
            vc_id = parts[parts.index('join') + 1] if len(parts) > parts.index('join') + 1 else None
            vc = client.get_channel(int(vc_id)) if vc_id else None
        if vc:
            await vc.connect()
            await message.add_reaction('✅')
    
    if 'leave' in content and f'<@{my_id}>' in content:
        vc = discord.utils.get(client.voice_clients, guild=message.guild)
        if vc: await vc.disconnect()
        await message.add_reaction('👋')
    
    # Auto-react tracking
    cmd_parts = content.replace(f'<@{my_id}>', '').strip().split(maxsplit=2)
    if len(cmd_parts) >= 3 and cmd_parts[0] in ['dir', '7yd']:
        user_id = int(cmd_parts[1].replace('<@', '').replace('>', ''))
        if cmd_parts[0] == 'dir':
            globals()['auto_react_' + str(user_id)] = True
            await message.add_reaction('🔛')
        else:
            globals()['auto_react_' + str(user_id)] = False
            await message.add_reaction('⏹️')
    
    # Auto-react trigger
    if hasattr(message.author, 'id') and globals().get(f'auto_react_{message.author.id}', False):
        await message.add_reaction('❤️')

# CRITICAL: Selfbot login (NOT asyncio.run/main())
client.run(TOKEN, bot=False)
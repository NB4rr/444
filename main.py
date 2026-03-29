import discord
import os
import random
import re

TOKEN = os.getenv('TOKEN', '').strip()
if len(TOKEN) < 50:
    print("❌ Token trop court!")
    exit(1)
print(f"🔑 OK: {TOKEN[:15]}...")

client = discord.Client(self_bot=True)
auto_reacts = {}

@client.event
async def on_ready():
    print(f"✅ {client.user} EN LIGNE!")
    print("Utilise <@ID> help")

@client.event
async def on_message(message):
    if message.author.id == client.user.id: return
    
    content = message.content.lower()
    mention = f'<@{client.user.id}>'
    
    if mention in content:
        parts = content.replace(mention, '').strip().split(maxsplit=3)
        cmd = parts[0] if parts else ''
        
        # HELP
        if cmd == 'help':
            embed = discord.Embed(title="🤖 SELF BOT", color=0x00ff00)
            embed.add_field(name="🎵 VOICE", value="join [id] | leave", inline=False)
            embed.add_field(name="⚡ REACT", value="dir @user | 7yd @user", inline=False)
            embed.add_field(name="💬 TEXT", value="say msg | spam 5 msg | dm @user msg", inline=False)
            embed.add_field(name="👑 MOD", value="nick nom | ban @user | kick @user", inline=False)
            await message.reply(embed=embed)
            return
        
        # VOICE JOIN/LEAVE
        if cmd == 'join':
            if message.author.voice:
                await message.author.voice.channel.connect()
            await message.add_reaction('✅')
        if cmd == 'leave':
            vc = discord.utils.get(client.voice_clients, guild=message.guild)
            if vc: await vc.disconnect()
            await message.add_reaction('👋')
        
        # AUTO REACT dir/7yd
        if cmd in ['dir', '7yd'] and len(parts) >= 2:
            user_id = int(re.search(r'(\d+)', parts[1]).group(1))
            auto_reacts[user_id] = (cmd == 'dir')
            await message.add_reaction('✅' if cmd == 'dir' else '❌')
        
        # SAY / SPAM
        if cmd == 'say' and len(parts) >= 2:
            await message.channel.send(' '.join(parts[1:]))
        if cmd == 'spam' and len(parts) >= 3:
            count = int(parts[1])
            msg = ' '.join(parts[2:])
            for _ in range(count): await message.channel.send(msg)
        
        # DM
        if cmd == 'dm' and len(parts) >= 3:
            user_id = int(re.search(r'(\d+)', parts[1]).group(1))
            user = client.get_user(user_id)
            if user: await user.send(' '.join(parts[2:]))
    
    # AUTO-REACT SYSTEM
    if message.author.id in auto_reacts and auto_reacts[message.author.id]:
        emojis = ['👍','❤️','😂','🔥','😍']
        await message.add_reaction(random.choice(emojis))

client.run(TOKEN, bot=False)
import discord
import asyncio
import random
import os
from datetime import datetime

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("ERROR: Set TOKEN in Railway Variables!")
    exit(1)

print("Starting Selfbot...")

client = discord.Client(self_bot=True)

def create_embed(title, desc, color=0x5865F2):
    embed = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now())
    embed.set_thumbnail(url='https://media.giphy.com/media/26ufnwz3wDUllvE0U/giphy.gif')
    embed.set_footer(text='Selfbot v4.0 - RAILWAY READY', icon_url='https://media.giphy.com/media/l0HlRnAWXxn0MhKLK/giphy.gif')
    return embed

@client.event
async def on_ready():
    print(f'🚀 {client.user} logged in!')
    client.auto_reacts = {}

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = message.content
    me = f'<@{client.user.id}>'
    
    if me in content:
        cmd = content.split(me)[1].strip().split()[0].lower()
        
        if cmd == 'join':
            await voice_join(message)
        elif cmd == 'leave':
            await voice_leave(message)
        elif cmd == 'say':
            await say_cmd(message)
        elif cmd == 'spam':
            await spam_cmd(message)
        elif cmd == 'dm':
            await dm_cmd(message)
        elif cmd == 'nick':
            await nick_cmd(message)
        elif cmd == 'role':
            await role_cmd(message)
        elif cmd == 'ban':
            await ban_cmd(message)
        elif cmd == 'kick':
            await kick_cmd(message)
        elif cmd == 'dir':
            await dir_react_cmd(message)
        elif cmd == '7yd':
            await sevenyd_react_cmd(message)
        elif cmd == 'pp':
            await pp_cmd(message)
        elif cmd == 'react':
            await react_cmd(message)
        elif cmd == 'help':
            await help_cmd(message)
    
    await handle_auto_react(message)

async def voice_join(message):
    channel_id = next((int(w) for w in message.content.split() if w.isdigit() and len(w) in [18,19]), None)
    vc = discord.utils.get(message.guild.voice_channels, id=channel_id) if channel_id else None
    if not vc and message.author.voice:
        vc = message.author.voice.channel
    if not vc:
        vc = next((ch for ch in message.guild.voice_channels if ch.permissions_for(message.guild.me).connect), None)
    if not vc:
        return await message.reply(embed=create_embed('❌', 'No voice channel!', 0xff0000))
    await vc.connect()
    await message.reply(embed=create_embed('✅', f'Joined #{vc.name}', 0x00ff00))

async def voice_leave(message):
    if client.voice_clients:
        vc = client.voice_clients[0]
        await vc.disconnect()
        await message.reply(embed=create_embed('👋', f'Left #{vc.channel.name}', 0xff9900))
    else:
        await message.reply(embed=create_embed('❌', 'Not in VC!', 0xff0000))

async def say_cmd(message):
    await message.delete()
    text = message.content.split(f'<@{client.user.id}> say ', 1)[1]
    await message.channel.send(text)

async def spam_cmd(message):
    parts = message.content.split()
    count = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 5
    text = ' '.join(parts[2:-1]) or '🗿'
    await message.delete()
    for _ in range(count):
        await message.channel.send(text)
        await asyncio.sleep(0.5)

async def dm_cmd(message):
    parts = message.content.split()
    user_id = int(parts[2].replace('<@', '').replace('>', ''))
    text = ' '.join(parts[3:])
    user = await client.fetch_user(user_id)
    await user.send(text)
    await message.reply(embed=create_embed('✅', f'DM to {user.name}!'))

async def nick_cmd(message):
    nick = ' '.join(message.content.split()[2:])
    await message.guild.me.edit(nickname=nick)
    await message.reply(embed=create_embed('✅', f'Nick: {nick}'))

async def role_cmd(message):
    role_name = ' '.join(message.content.split()[2:])
    role = discord.utils.get(message.guild.roles, name=role_name)
    if role:
        await message.guild.me.add_roles(role)
        await message.reply(embed=create_embed('✅', f'Role: {role.name}'))

async def ban_cmd(message):
    user_id = int(message.content.split()[2].replace('<@', '').replace('>', ''))
    user = message.guild.get_member(user_id)
    if user:
        await user.ban()
        await message.reply(embed=create_embed('🔨', f'Banned {user.name}'))

async def kick_cmd(message):
    user_id = int(message.content.split()[2].replace('<@', '').replace('>', ''))
    user = message.guild.get_member(user_id)
    if user:
        await user.kick()
        await message.reply(embed=create_embed('👢', f'Kicked {user.name}'))

async def dir_react_cmd(message):
    parts = message.content.split()
    if len(parts) < 4:
        return await message.reply(embed=create_embed('❌', '<@> dir @user 😂', 0xff0000))
    target_id = int(parts[2].replace('<@', '').replace('>', ''))
    emoji = parts[3]
    task_id = f"{target_id}_{emoji}"
    client.auto_reacts[task_id] = True
    user = message.guild.get_member(target_id)
    await message.reply(embed=create_embed('✅ DIR', f'{emoji} → {user.name}', 0x00ff00))

async def sevenyd_react_cmd(message):
    parts = message.content.split()
    if len(parts) < 4:
        return await message.reply(embed=create_embed('❌', '<@> 7yd @user 😂', 0xff0000))
    target_id = int(parts[2].replace('<@', '').replace('>', ''))
    emoji = parts[3]
    task_id = f"{target_id}_{emoji}"
    if task_id in client.auto_reacts:
        del client.auto_reacts[task_id]
        await message.reply(embed=create_embed('✅ 7YD', f'Stopped {emoji}'))
    else:
        await message.reply(embed=create_embed('❌', 'No auto-react!'))

async def pp_cmd(message):
    await message.reply('8' + '=' * random.randint(1, 15) + 'D')

async def react_cmd(message):
    emojis = ['😂', '🔥', '💯', '👍', '❤️']
    for emoji in random.sample(emojis, 3):
        try:
            await message.add_reaction(emoji)
        except:
            pass

async def help_cmd(message):
    embed = create_embed('🔥 SELF BOT v4.0', '')
    embed.add_field(name='Voice', value='`join` `leave`', inline=False)
    embed.add_field(name='Msg', value='`say` `spam` `dm`', inline=False)
    embed.add_field(name='Server', value='`nick` `role` `ban` `kick`', inline=False)
    embed.add_field(name='React', value='`dir @user emoji` `7yd @user emoji`', inline=False)
    embed.add_field(name='Fun', value='`pp` `react` `help`', inline=False)
    await message.reply(embed=embed)

async def handle_auto_react(message):
    client.auto_reacts = getattr(client, 'auto_reacts', {})
    for task_id in list(client.auto_reacts):
        if len(task_id.split('_')) == 2:
            target_id, emoji = task_id.split('_')
            if str(message.author.id) == target_id:
                try:
                    await message.add_reaction(emoji)
                except:
                    pass

async def main():
    await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
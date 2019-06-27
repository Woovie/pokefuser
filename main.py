import discord, aiohttp, configparser, asyncio
from bs4 import BeautifulSoup as bs

dConfig = configparser.ConfigParser()
dConfig.read('discordconfig.ini')

class discordClient(discord.Client):
    async def on_ready(self):
        print('Logged in as ', self.user)

    async def on_message(self, message):
        if message.author != self.user and message.content == 'pp!fuse':
            initMessage = await message.channel.send(f'Fusing for {message.author.mention}...')
            pagecontent = await getPkContent()
            pokeName = pagecontent.find(id="pk_name").string
            pokeImage = pagecontent.find(id="pk_img").get('src')
            pokeURL = pagecontent.find(id="permalink").get('value')
            pokeEmbed = discord.Embed(title=pokeName, url=pokeURL)
            pokeEmbed.set_image(url=pokeImage)
            pokeEmbed.set_footer(text="bot by Woovie#5555 | https://github.com/Woovie/pokefuser")
            await initMessage.delete()
            await message.channel.send(embed=pokeEmbed, content="")

async def getPkContent():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://pokemon.alexonsager.net/') as r:
            if r.status == 200:
                text = await r.read()
    return bs(text.decode('utf-8'), 'html.parser')

client = discordClient()

client.run(dConfig['discord']['token'])

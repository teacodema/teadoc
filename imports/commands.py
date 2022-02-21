import requests
from setup.actions import *

def init_bot_commands(params):

	bot = params['bot']
	discord = params['discord']
	
	@bot.event
	async def on_ready():
		try:
			print("We have logged in as {0.user}".format(bot))
			status = discord.Status.online
			activity = discord.Activity(type=discord.ActivityType.listening, name="to your commands")
			await bot.change_presence(status=status, activity=activity)
		except Exception as ex:
			print('----- on_ready(evt) -----')
			print(ex)

	def mdn_handle(config, key, term, embed):
		r = requests.get(url = config[key]['URL'], params = config[key]['PARAMS'])
		data = r.json()
		if 'documents' in data and len(data['documents']):
			for item in data['documents']:
				url = f"https://developer.mozilla.org/{item['mdn_url']}"
				value = f"{item['summary']}\n[See More ...]({url})"
				embed.add_field(name=f"{item['title']}", value=value, inline=False)
		else:
			embed.add_field(name=f"Results", value="Found 0 matches", inline=False)
		return embed	

	def sof_handle(config, key, term, embed):
		r = requests.get(url = config[key]['URL'], params = config[key]['PARAMS'])
		data = r.json()
		if 'items' in data and len(data['items']):
			for item in data['items']:
				value = f"[See More ...]({item['link']})"
				embed.add_field(name=f"{item['title']}", value=value, inline=False)
		else:
			embed.add_field(name=f"Results", value="Found 0 matches", inline=False)
		return embed

	def msdn_handle(config, key, term, embed):
		r = requests.get(url = config[key]['URL'], params = config[key]['PARAMS'])
		data = r.json()
		if 'results' in data and len(data['results']):
			for item in data['results']:
				description = item['description'] if ('description' in item) else ""
				value = f"{description[0:200]}\n[See More ...]({item['url']})"
				embed.add_field(name=f"{item['title']}", value=value, inline=False)
		else:
			embed.add_field(name=f"Results", value="Found 0 matches", inline=False)
		return embed

		
	@bot.command(name='docs', description='Get useful docs links')
	async def docs(ctx, *term):
		if not is_founders(ctx):
			await ctx.send('❌ Missing Permissions - Still on Testing phase')
			return
			
		if term:
			l = list(term)
			key = l.pop(0)
			if len(l) == 0:
				await ctx.send('❌ Provide a search term')
				return
			term = ' '.join(tuple(l))
			config = {
				'mdn': {
					'URL': 'https://developer.mozilla.org/api/v1/search',
					'PARAMS': {'q': term, 'locale': 'en-US', 'size': 5},
					'HANDLE': mdn_handle
				},
				'stackoverflow': {
					'URL': 'https://api.stackexchange.com/2.3/search/advanced',
					'PARAMS': {'order': 'desc', 'sort': 'activity', 'q': term, 'site': 'stackoverflow',},
					'HANDLE': sof_handle
				},
				'msdn': {
					'URL': 'https://docs.microsoft.com/api/search',
					'PARAMS': {'locale': 'en-us', 'search': term, '$top': 5},
					'HANDLE': msdn_handle
				}
			}
			embed = discord.Embed(color=0x1da1f2)
			embed.set_footer(text="🌐 Visit teacode.ma")
			embed.add_field(name=f"📋│Search results for : {term}", value=f'Source : {key}', inline=False)
			embed = config[key]['HANDLE'](config, key, term, embed)
			await ctx.send(embed=embed)
			return
		await ctx.send('❌ Provide a valid key and search term (\__docs mdn json, \__docs stackoverflow html)')

	@bot.command(name='help', description='This is a help command')
	async def help(ctx, *term):
		embed = discord.Embed(color=0x1da1f2)
		embed.set_footer(text="🌐 Visit teacode.ma")
		embed.add_field(name="Available bot commands", value='<@944662897429192775>', inline=False)
		for cmd in bot.commands:
			if cmd.name != 'help':
				embed.add_field(name=f'__{cmd.name}', value=cmd.description, inline=False)
		await ctx.send(embed=embed)
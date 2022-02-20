import requests

def init_bot_commands(params):

	bot = params['bot']
	# client2 = params['client2']
	discord = params['discord']
	# slash = params['slash']
	get = params['get']
	tasks = params['tasks']
	
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

	def mdn_handle(config, key, term):
		r = requests.get(url = config[key]['URL'], params = config[key]['PARAMS'])
		data = r.json()
		embed = discord.Embed(color=0x1da1f2)
		embed.set_footer(text=f"🌐 Visit teacode.ma")
		embed.add_field(name=f"📋│Search results for:", value=term, inline=False)
		if 'documents' in data and len(data['documents']):
			for item in data['documents']:
				url = f"https://developer.mozilla.org/{item['mdn_url']}"
				value = f"{item['summary']}\n[See More ...]({url})"
				embed.add_field(name=f"{item['title']}", value=value, inline=False)
		else:
			embed.add_field(name=f"Results", value="Found 0 matches", inline=False)
		return embed	

	def sof_handle(config, key, term):
		r = requests.get(url = config[key]['URL'], params = config[key]['PARAMS'])
		data = r.json()
		embed = discord.Embed(color=0x1da1f2)
		embed.set_footer(text=f"🌐 Visit teacode.ma")
		embed.add_field(name=f"📋│Search results for:", value=term, inline=False)
		if 'items' in data and len(data['items']):
			for item in data['items']:
				url = f"{item['link']}"
				value = f"[See More ...]({url})"
				embed.add_field(name=f"{item['title']}", value=value, inline=False)
		else:
			embed.add_field(name=f"Results", value="Found 0 matches", inline=False)
		return embed

	def msdn_handle(config, key, term):
		r = requests.get(url = config[key]['URL'], params = config[key]['PARAMS'])
		data = r.json()
		embed = discord.Embed(color=0x1da1f2)
		embed.set_footer(text=f"🌐 Visit teacode.ma")
		embed.add_field(name=f"📋│Search results for:", value=term, inline=False)
		if 'results' in data and len(data['results']):
			for item in data['results']:
				url = f"{item['url']}" 
				description = item['description'] if ('description' in item) else ""
				value = f"{description[0:200]}\n[See More ...]({url})"
				embed.add_field(name=f"{item['title']}", value=value, inline=False)
		else:
			embed.add_field(name=f"Results", value="Found 0 matches", inline=False)
		return embed

		
	@bot.command(name='docs', help='Get useful docs links')
	async def docs(ctx, *term):
		if term:
			l = list(term)
			key = l.pop(0)
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
			embed = config[key]['HANDLE'](config, key, term)
			await ctx.send(embed=embed)
			return
		await ctx.send('Provide a valid key and search term')
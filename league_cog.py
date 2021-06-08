# import discord
# from discord.ext import commands
# from riotwatcher import Lolwatcher
# from datetime import datetime


# class league_cog(commands.Cog):
#     def __init__(self, client, api_key):
#         self.watcher = Lolwatcher(api_key)
#         self.regions = {
#             'oce': 'oc1', 'oceania': 'oc1',
#             'euw': 'euw1', 'eun': 'eun1',
#             'jp': 'jp1', 'japan': 'jp1',
#             'kr': 'kr', 'korea': 'kr',
#             'na': 'na1', 'north america': 'na1',
#         }

#     # TODO check API for data format
#     @commands.command(name='rankedstats', help='**WIP**')
#     async def rankedstats(self, ctx, summoner_name, region):
#         user = self.watcher.summoner.by_name(self.regions[region], summoner_name)
#         stats = self.watcher.league.by_summoner(self.regions[region], user['id'])
        
#         tier = stats[0]['tier']
#         rank = stats[0]['rank']
#         lp = stats[0]['leaguePoints']
#         wins = int(stats[0]['wins'])
#         losses = int(stats[0]['losses'])

#         winrate = (wins / (wins + losses)) * 100

#         embed = discord.Embed(
#             title='', 
#             description=f'',
#             timestamp=datetime.utcnow()
#             )
#         embed.set_thumbnail(url='')
#         await ctx.send(embed=embed)
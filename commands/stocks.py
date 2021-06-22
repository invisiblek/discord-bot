import pprint as pp
import discord
from discord.ext import commands
from discord.ext.commands import bot
import requests
import logging
from datetime import datetime
import aiohttp
import asyncio
from os import environ, name


class stocks(commands.Cog, name="stocks"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.token = environ['STOCK_API_KEY']

    @commands.command(name='stocks', help='Use +stocks and the name of the company, i.e, +stocks GME.')
    async def stocks(self, context, symbol):
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = 'https://www.alphavantage.co/query'
        params = {
            f"function": "GLOBAL_QUOTE",
            f"symbol": symbol,
            f'apikey': self.token
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    stonks = await response.json()
                    symbol = stonks["Global Quote"]["01. symbol"]
                    open = stonks["Global Quote"]["02. open"]
                    high = stonks["Global Quote"]["03. high"]
                    low = stonks["Global Quote"]["04. low"]
                    price = stonks["Global Quote"]["05. price"]
                    volume = stonks['Global Quote']["06. volume"]
                    last_day = stonks["Global Quote"]["07. latest trading day"]
                    previous_close = stonks["Global Quote"]["08. previous close"]
                    change = stonks["Global Quote"]["09. change"]
                    change_percent = stonks["Global Quote"]["10. change percent"]
                    embed = discord.Embed(
                    )

                    embed.add_field(
                        name='symbol',  value=f"**{symbol}**"
                    )

                    embed.add_field(
                        name='open', value=f"**{open}**")

                    embed.add_field(
                        name='high', value=f"**{high}**")

                    embed.add_field(
                        name='low', value=f"**{low}**")

                    embed.add_field(
                        name='price', value=f"**{price}**")

                    embed.add_field(
                        name='volume', value=f"**{volume}**")

                    embed.add_field(
                        name='latest trading day', value=f"**{last_day}**")

                    embed.add_field(
                        name='previous close', value=f"**{previous_close}**")

                    embed.add_field(
                        name='change', value=f"**{change}**")

                    embed.add_field(
                        name='change percent', value=f"**{change_percent}**")

                    await context.reply(embed=embed)
                else:
                    await context.send(f'No company found!')


def setup(bot):
    bot.add_cog(stocks(bot))

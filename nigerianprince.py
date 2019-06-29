import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import random

BOT_PREFIX = ('+')
TOKEN = 'NTkzMjQ0NzQxMzUzNjAzMDcy.XRLKRQ.HxkDkECW7bACGK467Muq6GhKBc0'

bot = Bot(command_prefix=BOT_PREFIX)

convos = {'frequency': 1000}

@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(datetime.datetime.now().strftime('%m/%d %I:%M:%S %p'))
    print('------')

@bot.event
async def on_message(mes):
    # initiate convos
    if mes.guild and random.randrange(0,convos['frequency']) == 0:
        user = mes.author
        e_num = random.randint(1,7)
        email = []
        with open('email{}.txt'.format(e_num)) as email_f:
            for line in email_f:
                if '@' not in line:
                    email.append(line)
        try:
            await user.send(email[0])
            convos[mes.author.id] = {"email number": e_num, "next line": 1, "email text": email}
        except discord.errors.HTTPException:
            print('unable to send a message to {}'.format(user))
    # continue convos
    elif mes.guild == None and mes.author.id in convos:
        user = mes.author
        try:
            info = convos[mes.author.id]
            await user.send(info["email text"][info["next line"]])
            info["next line"] += 1
            if info["next line"] == len(info["email text"]):
                del convos[mes.author.id]
        except discord.errors.HTTPException:
            print('unable to send a message to {}'.format(user))
    await bot.process_commands(mes)

@bot.command()
async def change_frequency(ctx, new_freq):
    try:
        convos['frequency'] = int(new_freq)
    except Exception as error:
        await ctx.send('```error: {}```'.format(error))
        return
    await ctx.send('Frequency changed to one DM per {} messages.'.format(convos['frequency']))

bot.run(TOKEN)

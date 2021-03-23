import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import random, sys, getopt
from random import shuffle
import math
import time
from datetime import datetime
import csv
import os
import re
from Levenshtein import distance

levDistMin = 2
botColor = 0x2b006b
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Change the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='?', help_command = help_command)

def searchAbility(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('abilities.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c5].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
                return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchAC(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('actioncards.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6, c7, c8 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c8].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
                return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchAgenda(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('agendas.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c6].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
                return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchExplore(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('exploration.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6, c7, c8 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c8].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
                return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchLeader(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('leaders.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6, c7, c8 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c8].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
            	if search_string == 'nomad agent':
            	    suggestions.append(row[c1])
            	else:
                    return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchObjective(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('objectives.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6, c7 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c7].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
                return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchPlanet(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('planets.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c10].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
                return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchProm(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('promissories.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c6].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
            	if search_string in ['empyrean prom', 'empyrean promissory']:
            	    suggestions.append(row[c1])
            	else:
                    return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchRelic(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('relics.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c6].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
                return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchTech(cardname):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('techs.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6, c7 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c7].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
                return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

def searchUnit(unitname):
    search_string = unitname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open('units.csv', 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6, c7 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c7].split(", "))
            genAlias = []
            for index in range(0,len(row[c1])-len(search_string)+1):
                genAlias.append(row[c1].lower()[index:index+len(search_string)])
            if row[c1].lower() == search_string or search_string in aliasList:
                return row, True
            elif search_string in genAlias: 
                if savedRow == {}:
                    savedRow =  row.copy()
                    suggestions.append(row[c1])
                    matchFound = True
                else:
                    suggestions.append(row[c1])
                    matchFound = False
            else:
                levDist = distance(search_string,row[c1].lower())
                if levDist <= levDistMin:
                    suggestions.append(row[c1])
    if matchFound == True:
        return savedRow, True
    else:
        return suggestions, False

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command(name='ability',brief='Returns faction ability information by name.',help='Searches faction abilities for the specified name or partial match (<arg>).\n\nExample usage:\n?ability assimilate\n?ability entanglement')
async def lookUpAbility(ctx, *, arg):
    cardinfo, match = searchAbility(arg)
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        embed = discord.Embed(title = cardinfo["Name"], description= cardinfo["Faction"] + " Faction Ability", color=botColor)
        embed.add_field(name = "Ability Text", value = separator.join(cardrules), inline = False)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed)

@lookUpAbility.error
async def ability_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('ability')

@bot.command(name='actioncard',brief='Returns action card information by name.',help='Searches action cards for the specified name or partial match (<arg>).\n\nExample usage:\n?actioncard sabotage\n?actioncard rise')
async def lookUpActionCard(ctx, *, arg):
    cardinfo, match = searchAC(arg)
    if match:
        cardlore = cardinfo["Flavour Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = cardinfo["Action Card Name"], description= "**" + cardinfo["Timing"] + ":**\n" + cardinfo["Rules Text"], color=botColor)
        embed.add_field(name = "*Flavor Text*", value = "*" + separator.join(cardlore) + "*", inline = False)
        embed.add_field(name = "Source", value = cardinfo["Source"], inline = True)
        embed.add_field(name = "Quantity", value = cardinfo["Quantity"], inline = True)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed)

@lookUpActionCard.error
async def actioncard_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('actioncard')

@bot.command(pass_context=True,brief='Returns action card information by name.',help='Searches action cards for the specified name or partial match (<arg>).\n\nExample usage:\n?ac sabotage\n?ac rise')
async def ac(ctx):
    await lookUpActionCard.invoke(ctx)

@bot.command(name='agenda',brief='Returns agenda card information by name.',help='Searches agenda cards for the specified name or partial match (<arg>).\n\nExample usage:\n?agenda mutiny\n?agenda ixthian')
async def lookUpAgenda(ctx, *, arg):
    cardinfo, match = searchAgenda(arg)
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = cardinfo["Name"], description= "**" + cardinfo["Agenda Type"] + ":**\n\n" + separator.join(cardrules), color=botColor)
        embed.add_field(name = "Source", value = cardinfo["Source"], inline = True)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed)

@lookUpAgenda.error
async def agenda_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('agenda')

@bot.command(name='exploration',brief='Returns exploration card information by name.',help='Searches exploration cards for the specified name or partial match(<arg>).\n\nExample usage:\n?exploration freelancers\n?exploration fabricators')
async def lookUpExplore(ctx, *, arg):
    cardinfo, match = searchExplore(arg)
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        cardlore = cardinfo["Flavour Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = cardinfo["Name"], description= "*" + cardinfo["Type"] + " Exploration Card*\n\n" + separator.join(cardrules), color=botColor)
        if cardinfo["Flavour Text"] != "":
            embed.add_field(name = "*Flavor Text*", value = "*" + separator.join(cardlore) + "*", inline = False)
        embed.add_field(name = "Quantity", value = cardinfo["Quantity"], inline = True)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed)

@lookUpExplore.error
async def exploration_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('exploration')

@bot.command(pass_context=True,brief='Returns exploration card information by name.',help='Searches exploration cards for the specified name or partial match(<arg>).\n\nExample usage:\n?exp freelancers\n?exp fabricators')
async def exp(ctx):
    await lookUpExplore.invoke(ctx)

@bot.command(name='leader',brief='Returns leader information by name.',help='Searches leaders for the specified name or faction + type(<arg>).\n\nExample usage:\n?leader ta zern\n?leader nekro agent')
async def lookUpLeader(ctx, *, arg):
    cardinfo, match = searchLeader(arg)
    if match:
        cardrules = cardinfo["Text"].split("|")
        cardlore = cardinfo["Flavor Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = "__**" + cardinfo["Name"] + "**__", description= "***" + cardinfo["Subtitle"] + "***\n" + cardinfo["Faction"] + " " + cardinfo["Type"] + "\n" + separator.join(cardrules), color=botColor)
        embed.add_field(name = "*Flavor Text*", value = "*" + separator.join(cardlore) + "*", inline = False)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed)

@lookUpLeader.error
async def leader_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('leader')

@bot.command(name='objective',brief='Returns objective information by name.',help='Searches public and secret objectives for the specified name or partial match (<arg>).\n\nExample usage:\n?objective diversify research\n?objective monument')
async def lookUpObjective(ctx, *, arg):
    cardinfo, match = searchObjective(arg)
    if match:
        embed=discord.Embed(title = cardinfo["Name"], description= "*" + cardinfo["Type"] + " Objective - " + cardinfo["Phase"] + " Phase*\n\n" + cardinfo["Text"], color=botColor)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed)

@lookUpObjective.error
async def objective_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('objective')

@bot.command(pass_context=True,brief='Returns objective information by name.',help='Searches public and secret objectives for the specified name or partial match (<arg>).\n\nExample usage:\n?obj diversify research\n?obj monument')
async def obj(ctx):
    await lookUpObjective.invoke(ctx)

@bot.command(name='planet',brief='Returns planet information by name.',help='Searches planet cards for the specified name or partial match (<arg>).\n\nExample usage:\n?planet bereg\n?planet elysium')
async def lookUpPlanet(ctx, *, arg):
    cardinfo, match = searchPlanet(arg)
    if match:
        techSkip = "\n" + cardinfo["Tech Skip"] + " Technology Specialty" if cardinfo["Tech Skip"] else ""
        embed=discord.Embed(title = cardinfo["Planet Name"], description= cardinfo["Planet Trait"] + " - " + cardinfo["Resources"] + "/" + cardinfo["Influence"] + techSkip, color=botColor)
        embed.add_field(name = "*Flavor Text*", value = "*" + cardinfo["Flavour Text"] + "*", inline = False)
        if cardinfo["Legendary Ability"] != "":
            legend = cardinfo["Legendary Ability"].split("|")
            embed.add_field(name = "Legendary Ability", value = "\n".join(legend), inline = False)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed)

@lookUpPlanet.error
async def planet_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('planet')

@bot.command(name='promissory',brief='Returns promissory note information by name.',help='Searches generic and faction promissory notes for the specified name, partial match, or faction shorthand + "note" (<arg>).\n\nExample usage:\n?promissory alliance\n?promissory argent note')
async def lookUpProm(ctx, *, arg):
    cardinfo, match = searchProm(arg)
    if match:
        separator = "\n"
        rulesText = cardinfo["Rules Text"].split("|")
        embed=discord.Embed(title = cardinfo["Name"], description = "*" + cardinfo["Type"] + " Promissory Note*\n\n" + separator.join(rulesText), color=botColor)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed)

@lookUpProm.error
async def promissory_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('promissory')

@bot.command(pass_context=True,brief='Returns promissory note information by name.',help='Searches generic and faction promissory notes for the specified name, partial match, or faction shorthand + "note" (<arg>).\n\nExample usage:\n?prom alliance\n?prom argent note')
async def prom(ctx):
    await lookUpProm.invoke(ctx)

@bot.command(name='relic',brief='Returns relic information by name.',help='Searches relics for the specified name or partial match (<arg>).\n\nExample usage:\n?relic the obsidian\n?relic emphidia')
async def lookUpRelic(ctx, *, arg):
    cardinfo, match = searchRelic(arg)
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = cardinfo["Name"], description = separator.join(cardrules), color=botColor)
        embed.add_field(name = "*Flavor Text*", value = "*" + cardinfo["Flavor"] + "*", inline = False)
        embed.add_field(name = "Source", value = cardinfo["Source"], inline = True)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed) 

@lookUpRelic.error
async def relic_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('relic')

@bot.command(name='tech',brief='Returns technology information by name.',help='Searches generic and faction technology cards for the specified name or partial match (<arg>).\n\nExample usage:\n?tech dreadnought ii\n?tech dread 2')
async def lookUpTech(ctx, *, arg):
    cardinfo, match = searchTech(arg)
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        prereqs = ", Requires - " + cardinfo["Prerequisites"] if cardinfo["Prerequisites"] else ""
        embed=discord.Embed(title = cardinfo["Technology Name"], description = "*" + cardinfo["Type"] + " Technology" + prereqs + "*\n\n" + separator.join(cardrules), color=botColor)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed) 

@lookUpTech.error
async def tech_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('tech')

@bot.command(name='unit',brief='Returns unit information by name.',help='Searches generic and faction units for the specified name or partial match (<arg>).\n\nExample usage:\n?unit strike wing alpha\n?unit saturn engine')
async def lookUpUnit(ctx, *, arg):
    cardinfo, match = searchUnit(arg)
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        prereqs = "\nUpgrade requires " + cardinfo["Upgrade Requirements"] if cardinfo["Upgrade Requirements"] else ""
        embed=discord.Embed(title = cardinfo["Unit Name"], description = "*" + cardinfo["Type"] + " - " + cardinfo["Classification"] + "*\n\n" + separator.join(cardrules) + prereqs, color=botColor)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searchs: " + ", ".join(cardinfo))
    await ctx.send(embed=embed)

@lookUpUnit.error
async def unit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('unit')

bot.run(token)
random.seed(datetime.now())
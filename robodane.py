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

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='?')
levDistMin = 2

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
        if cardinfo["Notes"] == "":
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n***" + cardinfo["Faction"] + " Faction Ability***\n" + separator.join(cardrules))
        else:
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n***" + cardinfo["Faction"] + " Faction Ability***\n" + separator.join(cardrules) + "\n\n" + "Notes: " + cardinfo["Notes"])
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo))

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
        if cardinfo["Notes"] == "":
            if cardinfo["Quantity"] == "1":
                await ctx.send(">>> There is " + cardinfo["Quantity"] + " copy of " + cardinfo["Action Card Name"] + " printed in " + cardinfo["Source"] + ".\n__**" + cardinfo["Action Card Name"] + "**__\n**" + cardinfo["Timing"] + ":**\n" + cardinfo["Rules Text"] + "\n\n*" + separator.join(cardlore) + "*")
            else:
                await ctx.send(">>> There are " + cardinfo["Quantity"] + " copies of " + cardinfo["Action Card Name"] + " printed in " + cardinfo["Source"] + ".\n__**" + cardinfo["Action Card Name"] + "**__\n**" + cardinfo["Timing"] + ":**\n" + cardinfo["Rules Text"] + "\n\n*" + separator.join(cardlore) + "*")
        else:
            if cardinfo["Quantity"] == "1":
                await ctx.send(">>> There is " + cardinfo["Quantity"] + " copy of " + cardinfo["Action Card Name"] + " printed in " + cardinfo["Source"] + ".\n__**" + cardinfo["Action Card Name"] + "**__\n**" + cardinfo["Timing"] + ":**\n" + cardinfo["Rules Text"] + "\n\n*" + separator.join(cardlore) + "*" + "\nNotes: " + cardinfo["Notes"])
            else:
                await ctx.send(">>> There are " + cardinfo["Quantity"] + " copies of " + cardinfo["Action Card Name"] + " printed in " + cardinfo["Source"] + ".\n__**" + cardinfo["Action Card Name"] + "**__\n**" + cardinfo["Timing"] + ":**\n" + cardinfo["Rules Text"] + "\n\n*" + separator.join(cardlore) + "*" + "\nNotes: " + cardinfo["Notes"])
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo))

@lookUpActionCard.error
async def actioncard_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('actioncard')

@bot.command(name='agenda',brief='Returns agenda card information by name.',help='Searches agenda cards for the specified name or partial match (<arg>).\n\nExample usage:\n?agenda mutiny\n?agenda ixthian')
async def lookUpAgenda(ctx, *, arg):
    cardinfo, match = searchAgenda(arg)
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        if cardinfo["Notes"] == "":
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n***" + cardinfo["Agenda Type"] + "***\n" + separator.join(cardrules) + "\n\n" + "Source: " + cardinfo["Source"])
        else:
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n***" + cardinfo["Agenda Type"] + "***\n" + separator.join(cardrules) + "\n\n" + "Notes: " + cardinfo["Notes"] + "\n\n" + "Source: " + cardinfo["Source"])
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo))

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
        if cardinfo["Flavour Text"] == "":
            if cardinfo["Quantity"] == "1":
                await ctx.send(">>> There is " + cardinfo["Quantity"] + " copy of " + cardinfo["Name"] + ".\n__**" + cardinfo["Name"] + "**__\n***" + cardinfo["Type"] + " Exploration Card***\n" + separator.join(cardrules))
            else:
                await ctx.send(">>> There are " + cardinfo["Quantity"] + " copies of " + cardinfo["Name"] + ".\n__**" + cardinfo["Name"] + "**__\n***" + cardinfo["Type"] + " Exploration Card***\n" + separator.join(cardrules))
        else:
            if cardinfo["Quantity"] == "1":
                await ctx.send(">>> There is " + cardinfo["Quantity"] + " copy of " + cardinfo["Name"] + ".\n__**" + cardinfo["Name"] + "**__\n***" + cardinfo["Type"] + " Exploration Card***\n" + separator.join(cardrules) + "\n\n*" + separator.join(cardlore) + "*")
            else:
                await ctx.send(">>> There are " + cardinfo["Quantity"] + " copies of " + cardinfo["Name"] + ".\n__**" + cardinfo["Name"] + "**__\n***" + cardinfo["Type"] + " Exploration Card***\n" + separator.join(cardrules) + "\n\n*" + separator.join(cardlore) + "*")
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo))

@lookUpExplore.error
async def exploration_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('exploration')

@bot.command(name='leader',brief='Returns leader information by name.',help='Searches leaders for the specified name or faction + type(<arg>).\n\nExample usage:\n?leader ta zern\n?leader nekro agent')
async def lookUpLeader(ctx, *, arg):
    cardinfo, match = searchLeader(arg)
    if match:
        cardrules = cardinfo["Text"].split("|")
        cardlore = cardinfo["Flavor Text"].split("|")
        separator = "\n"
        if cardinfo["Notes"] == "":
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n***" + cardinfo["Subtitle"] + "***\n" + cardinfo["Faction"] + " " + cardinfo["Type"] + "\n" + separator.join(cardrules) + "\n\n*" + separator.join(cardlore) + "*")
        else:
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n***" + cardinfo["Subtitle"] + "***\n" + cardinfo["Faction"] + " " + cardinfo["Type"] + "\n" + separator.join(cardrules) + "\n\n*" + separator.join(cardlore) + "*\n\n" + cardinfo["Notes"])
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo))

@lookUpLeader.error
async def leader_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('leader')

@bot.command(name='objective',brief='Returns objective information by name.',help='Searches public and secret objectives for the specified name or partial match (<arg>).\n\nExample usage:\n?objective diversify research\n?objective monument')
async def lookUpObjective(ctx, *, arg):
    cardinfo, match = searchObjective(arg)
    if match:
        if cardinfo["Notes"] == "":
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n" + "*" + cardinfo["Type"] + " Objective - " + cardinfo["Phase"] + " Phase*\n" + cardinfo["Text"])
        else:
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n" + "*" + cardinfo["Type"] + " Objective - " + cardinfo["Phase"] + " Phase*\n" + cardinfo["Text"] + "\n\n" + "Notes: " + cardinfo["Notes"])
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo))

@lookUpObjective.error
async def objective_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('objective')

@bot.command(name='planet',brief='Returns planet information by name.',help='Searches planet cards for the specified name or partial match (<arg>).\n\nExample usage:\n?planet bereg\n?planet elysium')
async def lookUpPlanet(ctx, *, arg):
    cardinfo, match = searchPlanet(arg)
    if match:
        if cardinfo["Tech Skip"] != "":
            await ctx.send(">>> **" + cardinfo["Planet Name"] + "**\n" + cardinfo["Planet Trait"] + " - " + cardinfo["Resources"] + "/" + cardinfo["Influence"] + "\n" + cardinfo["Tech Skip"] + "\n\n*" + cardinfo["Flavour Text"] + "*")
        elif cardinfo["Legendary Ability"] != "":
            await ctx.send(">>> **" + cardinfo["Planet Name"] + "**\n" + cardinfo["Planet Trait"] + " - " + cardinfo["Resources"] + "/" + cardinfo["Influence"] + "\n\n*" + cardinfo["Flavour Text"] + "*" + "\n\n" + cardinfo["Legendary Ability"].split("|"))
        else:
            await ctx.send(">>> **" + cardinfo["Planet Name"] + "**\n" + cardinfo["Planet Trait"] + " - " + cardinfo["Resources"] + "/" + cardinfo["Influence"] + "\n\n*" + cardinfo["Flavour Text"] + "*")
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo))

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
        if cardinfo["Notes"] == "":
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n*" + cardinfo["Type"] + " Promissory Note*\n" + separator.join(rulesText))
        else:
            await ctx.send(">>> __**" + cardinfo["Name"] + "**__\n*" + cardinfo["Type"] + " Promissory Note*\n" + separator.join(rulesText) + "\n\n*Notes: " + cardinfo["Notes"] + "*")
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo))

@lookUpProm.error
async def promissory_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('promissory')

@bot.command(name='relic',brief='Returns relic information by name.',help='Searches relics for the specified name or partial match (<arg>).\n\nExample usage:\n?relic the obsidian\n?relic emphidia')
async def lookUpRelic(ctx, *, arg):
    cardinfo, match = searchRelic(arg)
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        if cardinfo["Notes"] == "":
            await ctx.send(">>> **" + cardinfo["Name"] + "**\n" + separator.join(cardrules) + "\n\n*" + cardinfo["Flavor"] + "*")
        else:
            await ctx.send(">>> **" + cardinfo["Name"] + "**\n" + separator.join(cardrules) + "\n\n*" + cardinfo["Flavor"] + "*\n\n" +  cardinfo["Notes"])
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo)) 

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
        if cardinfo["Notes"] == "":
            if cardinfo["Prerequisites"] == "":
                await ctx.send(">>> __**" + cardinfo["Technology Name"] + "**__\n" + "*" + cardinfo["Type"] + " Technology*\n" + separator.join(cardrules))
            else:
                await ctx.send(">>> __**" + cardinfo["Technology Name"] + "**__\n" + "*" + cardinfo["Type"] + " Technology, Requires - " + cardinfo["Prerequisites"] + "*\n" + separator.join(cardrules))
        else:
            if cardinfo["Prerequisites"] == "":
                await ctx.send(">>> __**" + cardinfo["Technology Name"] + "**__\n" + "*" + cardinfo["Type"] + " Technology*\n" + separator.join(cardrules) + "\n\n" + "Notes: " + cardinfo["Notes"])
            else:
                await ctx.send(">>> __**" + cardinfo["Technology Name"] + "**__\n" + "*" + cardinfo["Type"] + " Technology, Requires - " + cardinfo["Prerequisites"] + "*\n" + separator.join(cardrules) + "\n\n" + "Notes: " + cardinfo["Notes"])
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo))

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
        if cardinfo["Upgrade Requirements"] == "":
            await ctx.send(">>> **" + cardinfo["Unit Name"] + "**\n*" + cardinfo["Type"] + " - " + cardinfo["Classification"] + "*\n" + separator.join(cardrules))
        else:
            await ctx.send(">>> **" + cardinfo["Unit Name"] + "**\n*" + cardinfo["Type"] + " - " + cardinfo["Classification"] + "*\n" + separator.join(cardrules) + "\nUpgrade requires " + cardinfo["Upgrade Requirements"])
    else:
        if cardinfo == []:
            await ctx.send(">>> No match found for " + arg + ".")
        else:
            await ctx.send(">>> No match found for " + arg + ".\nSuggested searchs: " + ", ".join(cardinfo)) 

@lookUpUnit.error
async def unit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('unit')

bot.run(token)
random.seed(datetime.now())
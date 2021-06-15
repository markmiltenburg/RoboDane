import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import sys, getopt
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

def search(cardname, filename):
    search_string = cardname.lower()
    suggestions = []
    savedRow = {}
    matchFound = False
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12 = reader.fieldnames
        for row in reader:
            aliasList = list(row[c12].split(", "))
            orig_name_lower = row[c1].lower()
            genAlias = [orig_name_lower[i: i+len(search_string)] for i in range(len(orig_name_lower)-len(search_string)+1)]
            if orig_name_lower == search_string or search_string in aliasList:
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
                levDist = distance(search_string,orig_name_lower)
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
    cardinfo, match = search(arg, 'abilities.csv')
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        embed = discord.Embed(title = cardinfo["Name"], description= cardinfo["Type"] + " Faction Ability", color=botColor)
        embed.add_field(name = "Ability Text", value = separator.join(cardrules), inline = False)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpAbility.error
async def ability_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('ability')
        await ctx.message.delete(delay = 60)

@bot.command(name='actioncard',brief='Returns action card information by name.',help='Searches action cards for the specified name or partial match (<arg>).\n\nExample usage:\n?actioncard sabotage\n?actioncard rise')
async def lookUpActionCard(ctx, *, arg):
    cardinfo, match = search(arg,'actioncards.csv')
    if match:
        cardlore = cardinfo["Flavour Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = cardinfo["Name"], description= "**" + cardinfo["Type"] + ":**\n" + cardinfo["Rules Text"], color=botColor)
        embed.add_field(name = "*Flavour Text*", value = "*" + separator.join(cardlore) + "*", inline = False)
        embed.add_field(name = "Source", value = cardinfo["Source"], inline = True)
        embed.add_field(name = "Quantity", value = cardinfo["Quantity"], inline = True)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpActionCard.error
async def actioncard_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('actioncard')
        await ctx.message.delete(delay = 60)

@bot.command(pass_context=True,brief='Returns action card information by name.',help='Searches action cards for the specified name or partial match (<arg>).\n\nExample usage:\n?ac sabotage\n?ac rise')
async def ac(ctx):
    await lookUpActionCard.invoke(ctx)

@bot.command(name='agenda',brief='Returns agenda card information by name.',help='Searches agenda cards for the specified name or partial match (<arg>).\n\nExample usage:\n?agenda mutiny\n?agenda ixthian')
async def lookUpAgenda(ctx, *, arg):
    cardinfo, match = search(arg,'agendas.csv')
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = cardinfo["Name"], description= "**" + cardinfo["Type"] + ":**\n\n" + separator.join(cardrules), color=botColor)
        embed.add_field(name = "Source", value = cardinfo["Source"], inline = True)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpAgenda.error
async def agenda_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('agenda')
        await ctx.message.delete(delay = 60)

@bot.command(name='exploration',brief='Returns exploration card information by name.',help='Searches exploration cards for the specified name or partial match(<arg>).\n\nExample usage:\n?exploration freelancers\n?exploration fabricators')
async def lookUpExplore(ctx, *, arg):
    cardinfo, match = search(arg,'exploration.csv')
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        cardlore = cardinfo["Flavour Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = cardinfo["Name"], description= "*" + cardinfo["Type"] + " Exploration Card*\n\n" + separator.join(cardrules), color=botColor)
        if cardinfo["Flavour Text"] != "":
            embed.add_field(name = "*Flavour Text*", value = "*" + separator.join(cardlore) + "*", inline = False)
        embed.add_field(name = "Quantity", value = cardinfo["Quantity"], inline = True)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpExplore.error
async def exploration_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('exploration')
        await ctx.message.delete(delay = 60)

@bot.command(pass_context=True,brief='Returns exploration card information by name.',help='Searches exploration cards for the specified name or partial match(<arg>).\n\nExample usage:\n?exp freelancers\n?exp fabricators')
async def exp(ctx):
    await lookUpExplore.invoke(ctx)
    await ctx.message.delete(delay = 60)

@bot.command(name='leader',brief='Returns leader information by name.',help='Searches leaders for the specified name or faction + type(<arg>).\n\nExample usage:\n?leader ta zern\n?leader nekro agent')
async def lookUpLeader(ctx, *, arg):
    cardinfo, match = search(arg,'leaders.csv')
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        cardlore = cardinfo["Flavour Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = "__**" + cardinfo["Name"] + "**__", description= "***" + cardinfo["Type"] + "***\n" + cardinfo["Classification"] + " " + cardinfo["Type"] + "\n" + separator.join(cardrules), color=botColor)
        embed.add_field(name = "*Flavour Text*", value = "*" + separator.join(cardlore) + "*", inline = False)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpLeader.error
async def leader_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('leader')
        await ctx.message.delete(delay = 60)

@bot.command(name='objective',brief='Returns objective information by name.',help='Searches public and secret objectives for the specified name or partial match (<arg>).\n\nExample usage:\n?objective diversify research\n?objective monument')
async def lookUpObjective(ctx, *, arg):
    cardinfo, match = search(arg,'objectives.csv')
    if match:
        embed=discord.Embed(title = cardinfo["Name"], description= "*" + cardinfo["Type"] + " Objective - " + cardinfo["Classification"] + " Phase*\n\n" + cardinfo["Rules Text"], color=botColor)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpObjective.error
async def objective_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('objective')
        await ctx.message.delete(delay = 60)

@bot.command(pass_context=True,brief='Returns objective information by name.',help='Searches public and secret objectives for the specified name or partial match (<arg>).\n\nExample usage:\n?obj diversify research\n?obj monument')
async def obj(ctx):
    await lookUpObjective.invoke(ctx)

@bot.command(name='planet',brief='Returns planet information by name.',help='Searches planet cards for the specified name or partial match (<arg>).\n\nExample usage:\n?planet bereg\n?planet elysium')
async def lookUpPlanet(ctx, *, arg):
    cardinfo, match = search(arg,'planets.csv')
    if match:
        techSkip = "\n" + cardinfo["Classification"] + " Technology Specialty" if cardinfo["Classification"] else ""
        embed=discord.Embed(title = cardinfo["Name"], description= cardinfo["Type"] + " - " + cardinfo["Res_Inf"] + techSkip, color=botColor)
        embed.add_field(name = "*Flavour Text*", value = "*" + cardinfo["Flavour Text"] + "*", inline = False)
        if cardinfo["Rules Text"] != "":
            legend = cardinfo["Rules Text"].split("|")
            embed.add_field(name = "Legendary Ability", value = "\n".join(legend), inline = False)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpPlanet.error
async def planet_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('planet')
        await ctx.message.delete(delay = 60)

@bot.command(name='promissory',brief='Returns promissory note information by name.',help='Searches generic and faction promissory notes for the specified name, partial match, or faction shorthand + "note" (<arg>).\n\nExample usage:\n?promissory alliance\n?promissory argent note')
async def lookUpProm(ctx, *, arg):
    cardinfo, match = search(arg,'promissories.csv')
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
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpProm.error
async def promissory_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('promissory')
        await ctx.message.delete(delay = 60)

@bot.command(pass_context=True,brief='Returns promissory note information by name.',help='Searches generic and faction promissory notes for the specified name, partial match, or faction shorthand + "note" (<arg>).\n\nExample usage:\n?prom alliance\n?prom argent note')
async def prom(ctx):
    await lookUpProm.invoke(ctx)

@bot.command(name='relic',brief='Returns relic information by name.',help='Searches relics for the specified name or partial match (<arg>).\n\nExample usage:\n?relic the obsidian\n?relic emphidia')
async def lookUpRelic(ctx, *, arg):
    cardinfo, match = search(arg,'relics.csv')
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        embed=discord.Embed(title = cardinfo["Name"], description = separator.join(cardrules), color=botColor)
        embed.add_field(name = "*Flavour Text*", value = "*" + cardinfo["Flavour Text"] + "*", inline = False)
        embed.add_field(name = "Source", value = cardinfo["Source"], inline = True)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpRelic.error
async def relic_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('relic')
        await ctx.message.delete(delay = 60)

@bot.command(name='tech',brief='Returns technology information by name.',help='Searches generic and faction technology cards for the specified name or partial match (<arg>).\n\nExample usage:\n?tech dreadnought ii\n?tech dread 2')
async def lookUpTech(ctx, *, arg):
    cardinfo, match = search(arg,'techs.csv')
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        prereqs = ", Requires - " + cardinfo["Prerequisites"] if cardinfo["Prerequisites"] else ""
        embed=discord.Embed(title = cardinfo["Name"], description = "*" + cardinfo["Type"] + " Technology" + prereqs + "*\n\n" + separator.join(cardrules), color=botColor)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpTech.error
async def tech_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('tech')
        await ctx.message.delete(delay = 60)

@bot.command(name='unit',brief='Returns unit information by name.',help='Searches generic and faction units for the specified name or partial match (<arg>).\n\nExample usage:\n?unit strike wing alpha\n?unit saturn engine')
async def lookUpUnit(ctx, *, arg):
    cardinfo, match = search(arg,'units.csv')
    if match:
        cardrules = cardinfo["Rules Text"].split("|")
        separator = "\n"
        prereqs = "\nUpgrade requires " + cardinfo["Prerequisites"] if cardinfo["Prerequisites"] else ""
        embed=discord.Embed(title = cardinfo["Name"], description = "*" + cardinfo["Type"] + " - " + cardinfo["Classification"] + "*\n\n" + separator.join(cardrules) + prereqs, color=botColor)
        if cardinfo["Notes"] != "":
            embed.add_field(name = "Notes", value = cardinfo["Notes"], inline = False)
    else:
        if cardinfo == []:
            embed = discord.Embed(title = "No matches found.", description = "No results for \"" + arg + "\" were found. Please try another search.")
        else:
            embed = discord.Embed(title = "No matches found.", description = "Suggested searches: " + ", ".join(cardinfo))
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@lookUpUnit.error
async def unit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help('unit')
        await ctx.message.delete(delay = 60)

@bot.command(name='l1hero',brief='Returns information about using the L1Z1X hero.',help='Returns information about using the L1Z1X hero.\n\nExample usage:\n?l1hero')
async def l1hero(ctx):
    embed=discord.Embed(title = "L1Z1X Hero - Dark Space Navigation", description = "This is a \"teleport\". The move value of your dreads/flagship is irrelevant.\nYou must legally be able to move into the chosen system, so no supernovas, no nebulas, no asteroid fields without Antimass Deflectors.\nYou can move dreads & flagship out of systems containing your command tokens.\nThey can only transport units from their origin system without their command tokens, even if it is the only capacity unit in a system w ground forces in the space area.", color=botColor)
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@bot.command(name='titanstiming',brief='Returns information about the timing windows involved with the titans abilities.',help='Returns information about the timing windows involved with the Titans of Ul\'s abilities Terragenesis and Awaken.\n\nExample usage:\n?titanstiming')
async def titanstiming(ctx):
    embed=discord.Embed(title = "Titans Timing Windows - Terragenesis, Awaken, Ouranos, and Hecatonchires", description = "Activating a system\nis not the same as\nActivating a system that contains X\n\nIf you activate a system that has sleeper tokens on all the planets, no PDS but does have a unit on at least one planet, the first thing you do is use Scanlink Drone Network (SDN).\nAfter exploring you cannot add an additional sleeper token since all sleepers are still present and have not been replaced or moved yet.\nYou can trigger AWAKEN to turn sleeper tokens into PDS, however you cannot use those PDS to DEPLOY their flagship, since you did not \"activate a system that contains 1 or more of your PDS.\"\nLikewise, you cannot activate a system that contains no sleeper tokens, explore using SDN, add a sleeper token and then AWAKEN it since you did not \"activate a system that contains 1 or more of your sleeper tokens.\"\nEven if you had a multi-planet system where one planet has a sleeper token and the explored planet doesn't, AWAKEN specifies \"those tokens\", referring to the tokens present at the time of activation as being able to be replaced.\nIn order to use the mech's Deploy ability, you must have a PDS unit in your reinforcements.", color=botColor)
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

@bot.command(name='sardakkcommander',brief='Returns information about using the Sardakk Commander.',help='Returns information about using the Sardakk N\'orr commander.\n\nExample usage:\n?sardakkcommander')
async def l1hero(ctx):
    embed=discord.Embed(title = "Sardakk Commander - G\'hom Sek\'kus", description = "The Sardakk N\'orr commander/alliance does not care about:\n1) The space area of the active system\n2) The space area of the systems containing planets being committed from\n3) Effects that prevent movement, including being a structure and ground force, Ceasefire and Enforced Travel Ban. Committing is not moving.\n4) Whether the planets being committed to are friendly, enemy, or uncontrolled.\n\nThe Sardakk Norr commander/alliance does care about:\n1) Being the active player\n2) The DMZ(Demilitarized Zone Planet Attachment)\n3) Effects that end your turn, such as Nullification Field or Minister of Peace\n4) Parley. Your ground forces will be removed if you have no capacity in the space area of the active system.\n5) Your command tokens in the systems containing the planets being committed from", color=botColor)
    newMessage = await ctx.send(embed=embed)
    await ctx.message.delete(delay = 60)
    await newMessage.delete(delay = 300)

bot.run(token)
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
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands

levDistMin = 2
botColor = 0x2b006b
time_to_delete_response = 300
prefix = '?'
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild_ids = [696729526830628864, 409096158372167683, 409044671508250625, 692059147201413211]

# Change the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix=prefix, help_command = help_command)
slash = SlashCommand(bot, sync_commands=True)

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


@slash.slash(
    name="ability",
    guild_ids=guild_ids,
    description="Searches faction abilities by name. Example usage: /ability assimilate /ability entanglement",
    options=[manage_commands.create_option(
        name="ability",
        description="Ability Name",
        option_type=3,
        required=True
    )])
async def lookUpAbility(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="actioncard",
    guild_ids=guild_ids,
    description="Searches action cards by name. Example usage: /actioncard sabotage /actioncard rise",
    options=[manage_commands.create_option(
        name="actioncard",
        description="Action Card Name",
        option_type=3,
        required=True
    )])
async def lookUpActionCard(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="ac",
    guild_ids=guild_ids,
    description="Searches action cards by name. Example usage: /ac sabotage /ac rise",
    options=[manage_commands.create_option(
        name="actioncard",
        description="Action Card Name",
        option_type=3,
        required=True
    )])
async def ac(ctx, arg):
    await lookUpActionCard.invoke(ctx, arg)

@slash.slash(
    name="agenda",
    guild_ids=guild_ids,
    description="Searches agenda cards by name. Example usage: /agenda mutiny /agenda ixthian",
    options=[manage_commands.create_option(
        name="agenda",
        description="Agenda Name",
        option_type=3,
        required=True
    )])
async def lookUpAgenda(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="exploration",
    guild_ids=guild_ids,
    description="Searches exploration cards by name. Example usage: /exploration freelancers /exploration fabricators",
    options=[manage_commands.create_option(
        name="explorationcard",
        description="Exploration Card Name",
        option_type=3,
        required=True
    )])
async def lookUpExplore(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="exp",
    guild_ids=guild_ids,
    description="Searches exploration cards by name. Example usage: /exp freelancers /exp fabricators",
    options=[manage_commands.create_option(
        name="explorationcard",
        description="Exploration Card Name",
        option_type=3,
        required=True
    )])
async def exp(ctx, arg):
    await lookUpExplore.invoke(ctx,arg)

@slash.slash(
    name="leader",
    guild_ids=guild_ids,
    description="Searches leaders by name or faction. Example usage: /leader ta zern /leader nekro agent",
    options=[manage_commands.create_option(
        name="leader",
        description="Leader Name/Faction name and leader type",
        option_type=3,
        required=True
    )])
async def lookUpLeader(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="objective",
    guild_ids=guild_ids,
    description="Searches public and secret objectives. Example usage: /objective become a legend /objective monument",
    options=[manage_commands.create_option(
        name="objective",
        description="Objective name",
        option_type=3,
        required=True
    )])
async def lookUpObjective(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="obj",
    guild_ids=guild_ids,
    description="Searches public and secret objectives. Example usage: /obj become a legend /obj monument",
    options=[manage_commands.create_option(
        name="objective",
        description="Objective name",
        option_type=3,
        required=True
    )])
async def obj(ctx, arg):
    await lookUpObjective.invoke(ctx, arg)

@slash.slash(
    name="planet",
    guild_ids=guild_ids,
    description="Searches planet cards. Example usage: /planet bereg /planet elysium",
    options=[manage_commands.create_option(
        name="planet",
        description="Planet name",
        option_type=3,
        required=True
    )])
async def lookUpPlanet(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="promissory",
    guild_ids=guild_ids,
    description="Searches generic and faction promissories. Example usage: /promissory spy net /promissory ceasefire",
    options=[manage_commands.create_option(
        name="promissorynote",
        description="Promissory note",
        option_type=3,
        required=True
    )])
async def lookUpProm(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="prom",
    guild_ids=guild_ids,
    description="Searches generic and faction promissories. Example usage: /prom spy net /prom ceasefire",
    options=[manage_commands.create_option(
        name="promissorynote",
        description="Promissory note",
        option_type=3,
        required=True
    )])
async def prom(ctx, arg):
    await lookUpProm.invoke(ctx, arg)

@slash.slash(
    name="relic",
    guild_ids=guild_ids,
    description="Searches relics for the name or partial match. Example usage: /relic the obsidian /relic emphidia",
    options=[manage_commands.create_option(
        name="relic",
        description="Relic name",
        option_type=3,
        required=True
    )])
async def lookUpRelic(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="tech",
    guild_ids=guild_ids,
    description="Searches generic and faction technologies. Example usage: /tech dreadnought 2 /tech magen",
    options=[manage_commands.create_option(
        name="technology",
        description="Technology name",
        option_type=3,
        required=True
    )])
async def lookUpTech(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="unit",
    guild_ids=guild_ids,
    description="Searches generic and faction units. Example usage: /unit strike wing alpha /unit saturn engine",
    options=[manage_commands.create_option(
        name="unit",
        description="Unit name",
        option_type=3,
        required=True
    )])
async def lookUpUnit(ctx, arg):
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
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="l1hero",
    guild_ids=guild_ids,
    description="Returns information about using the L1Z1X hero. Example usage: /l1hero",
)
async def l1hero(ctx):
    embed=discord.Embed(title = "L1Z1X Hero - Dark Space Navigation", description = "This is a \"teleport\". The move value of your dreads/flagship is irrelevant.\nYou must legally be able to move into the chosen system, so no supernovas, no nebulas, no asteroid fields without Antimass Deflectors.\nYou can move dreads & flagship out of systems containing your command tokens.\nThey can only transport units from their origin system without their command tokens, even if it is the only capacity unit in a system w ground forces in the space area.", color=botColor)
    newMessage = await ctx.send(embed=embed)
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="titanstiming",
    guild_ids=guild_ids,
    description="Returns information about timing windows for the titans abilities. Example usage: /titanstiming",
)
async def titanstiming(ctx):
    embed=discord.Embed(title = "Titans Timing Windows - Terragenesis, Awaken, Ouranos, and Hecatonchires", description = "Activating a system\nis not the same as\nActivating a system that contains X\n\nIf you activate a system that has sleeper tokens on all the planets, no PDS but does have a unit on at least one planet, the first thing you do is use Scanlink Drone Network (SDN).\nAfter exploring you cannot add an additional sleeper token since all sleepers are still present and have not been replaced or moved yet.\nYou can trigger AWAKEN to turn sleeper tokens into PDS, however you cannot use those PDS to DEPLOY their flagship, since you did not \"activate a system that contains 1 or more of your PDS.\"\nLikewise, you cannot activate a system that contains no sleeper tokens, explore using SDN, add a sleeper token and then AWAKEN it since you did not \"activate a system that contains 1 or more of your sleeper tokens.\"\nEven if you had a multi-planet system where one planet has a sleeper token and the explored planet doesn't, AWAKEN specifies \"those tokens\", referring to the tokens present at the time of activation as being able to be replaced.\nIn order to use the mech's Deploy ability, you must have a PDS unit in your reinforcements.", color=botColor)
    newMessage = await ctx.send(embed=embed)
    await newMessage.delete(delay = time_to_delete_response)

@slash.slash(
    name="sardakkcommander",
    guild_ids=guild_ids,
    description="Returns information about using the Sardakk N\'orr commander. Example usage: /sardakkcommander",
)
async def l1hero(ctx):
    embed=discord.Embed(title = "Sardakk Commander - G\'hom Sek\'kus", description = "The Sardakk N\'orr commander/alliance does not care about:\n1) The space area of the active system\n2) The space area of the systems containing planets being committed from\n3) Effects that prevent movement, including being a structure and ground force, Ceasefire and Enforced Travel Ban. Committing is not moving.\n4) Whether the planets being committed to are friendly, enemy, or uncontrolled.\n\nThe Sardakk Norr commander/alliance does care about:\n1) Being the active player\n2) The DMZ(Demilitarized Zone Planet Attachment)\n3) Effects that end your turn, such as Nullification Field or Minister of Peace\n4) Parley. Your ground forces will be removed if you have no capacity in the space area of the active system.\n5) Your command tokens in the systems containing the planets being committed from", color=botColor)
    newMessage = await ctx.send(embed=embed)
    await newMessage.delete(delay = time_to_delete_response)

bot.run(token)
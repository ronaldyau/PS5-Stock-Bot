from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
from bs4 import BeautifulSoup, re
import time
import asyncio
import random

target_status = True
bestbuy_status = True
gamestop_status = True
micromania_status = True

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

prefix = "!PS"

bot = commands.Bot(command_prefix = prefix)

opts = Options()
opts.add_argument('--no-sandbox')
opts.add_argument('--lang=en_US') 
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_argument('--headless')
opts.add_argument('--user-agent=User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"')
opts.add_argument('--disable-dev-shm-usage')

chrome_driver = os.getcwd() +"/linux_chromedriver"

driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

async def update_status(id, in_stock):
    # US
    channel = bot.get_channel(846860248865177630)
    footer_text = "Please consider subscribing to my Patreon"
    if id == 1:
        if in_stock == False:
            embed=discord.Embed(title="Target", url="https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596", description="There are currently no PS5s in stock.", color=0xFF5733)
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        if in_stock == True:
            embed=discord.Embed(title="Target", url="https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596", description="PS5s are in stock!", color=discord.Color.green())
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
    elif id == 2:
        if in_stock == False:
            embed=discord.Embed(title="Best Buy", url="https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149", description="There are currently no PS5s in stock.", color=0xFF5733)
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        if in_stock == True:
            embed=discord.Embed(title="Best Buy", url="https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149", description="PS5s are in stock!", color=discord.Color.green())
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
    elif id == 3:
        if in_stock == False:
            embed=discord.Embed(title="GameStop", url="https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html", description="There are currently no PS5s in stock.", color=0xFF5733)
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        if in_stock == True:
            embed=discord.Embed(title="GameStop", url="https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html", description="PS5s are in stock!", color=discord.Color.green())
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
    #FR
    elif id == 4:
        channel = bot.get_channel(847929825884766239)
        footer_text="Pensez à vous abonner à mon Patreon"
        if in_stock == False:
            embed=discord.Embed(title="MircoMania", url="https://www.micromania.fr/playstation-5-alldigital-106097.html", description="Il n'y a actuellement aucune PS5 en stock.", color=0xFF5733)
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        if in_stock == True:
            embed=discord.Embed(title="MicroMania", url="https://www.micromania.fr/playstation-5-alldigital-106097.html", description="Les PS5 sont en stock!", color=discord.Color.green())
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)

async def scrape_target():
    global target_status
    print("starting target scrape\n\n")

    driver.delete_all_cookies()

    driver.get("https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596")

    await asyncio.sleep(5)

    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'html.parser')

    sold_out = soup.find_all("div", {"data-test": "soldOutBlock"})
    
    if not sold_out:
        print("(Target) IN STOCK!!!!!\n\n")
        if target_status == False:
            await update_status(1, True)
            target_status = True
    else:
        print("(Target) sold out :(\n\n")
        if target_status == True:
            await update_status(1, False)
            target_status = False

async def scrape_best_buy():
    global bestbuy_status
    print("starting best buy scrape\n\n")

    driver.delete_all_cookies()

    driver.get("https://www.bestbuy.com/")

    await asyncio.sleep(5)

    driver.get("https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149")

    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'html.parser')

    sold_out = soup.find_all("button", {"class": "add-to-cart-button"})

    if sold_out[0].text != "Sold Out":
        print("(BestBuy) IN STOCK!!!!!\n\n")
        if bestbuy_status == False:
            await update_status(2, True)
            bestbuy_status = True
    else:
        print("(BestBuy) sold out :(\n\n")
        if bestbuy_status == True:
            await update_status(2, False)
            bestbuy_status = False

async def scrape_gamestop():
    global gamestop_status
    print("starting gamestop scrape\n\n")

    driver.delete_all_cookies()

    driver.get("https://www.gamestop.com/")

    await asyncio.sleep(5)

    driver.get("https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html")

    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'html.parser')

    sold_out = soup.find_all("button", {"data-pid": "11108140"})

    if sold_out[0].text != "Not Available":
        print("(GameStop) IN STOCK!!!!!\n\n")
        if gamestop_status == False:
            await update_status(3, True)
            gamestop_status = True
    else:
        print("(GameStop) sold out :(\n\n")
        if gamestop_status == True:
            await update_status(3, False)
            gamestop_status = False

async def scrape_micromania():
    global micromania_status
    print("starting micromania scrape\n\n")

    driver.delete_all_cookies()

    driver.get("https://www.micromania.fr/playstation-5-alldigital-106097.html")

    await asyncio.sleep(5)

    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'html.parser')

    sold_out = soup.find_all("span", text="Produit disponible en magasin uniquement.")

    print(sold_out)

    if sold_out:
        print("(MicroMania) IN STOCK!!!!!\n\n")
        if micromania_status == False:
            await update_status(4, True)
            micromania_status = True
    else:
        print("(MicroMania) sold out :(\n\n")
        if micromania_status == True:
            await update_status(4, False)
            micromania_status = False

@tasks.loop(seconds=30)
async def scrape():
    await scrape_target()
    await scrape_gamestop()
    await scrape_best_buy()
    await scrape_micromania()
    await bot.get_channel(846905034422878258).send("All Trackers Online")
    await asyncio.sleep(20)

@bot.event
async def on_ready():
    print('[on_ready] start scrape')
    scrape.start()

@bot.command()
async def start(ctx):
    print('[start] start scrape')
    scrape.start()

bot.run(token)
import discord 
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import time 
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import os 
import asyncio
import random
import atexit

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--window-size=1920,1080")
options.add_argument('--no-sandbox')

chrome_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
s = Service(chrome_driver_path)

intents = discord.Intents().all()
intents.members = True
client = commands.Bot(command_prefix=":", intents=intents, case_insensitive=True)
clients = discord.Client(intents=discord.Intents.default())
client.remove_command('help')
token = open("token.txt", "r").read()
url = "https://nonsa.pl/wiki/Mezo"
channelTarget = 1107757434950393946


@client.event
async def on_ready():
    print("Starting...")
    #sending = client.get_channel(channelTarget)
    #guild_id = 1076287644167852042
    #rolename= "VerCard"
    #guild = discord.utils.get(client.guilds, id=guild_id)
    #if guild is not None:
    #    role = discord.utils.get(guild.roles, name=rolename)
    #    if role is not None:
    #        role_mention = role.mention
    #        await sending.send("work " + role_mention)

@client.command()
async def GetFrazes(ctx, *args):
    waitEmbed = discord.Embed(title="" ,description="this may take a few seconds")
    waitEmbed.set_image(url="https://media.tenor.com/w_C4CpUBih4AAAAC/100.gif")
    sendWait =await ctx.send(embed = waitEmbed)
    UseAVA = ctx.author.avatar.url
    driver = webdriver.Chrome(service=s, options=options)
    driver.get('https://nonsa.pl/wiki/Strona_g%C5%82%C3%B3wna')
    wait = WebDriverWait(driver, 5)
    PostDisplay = discord.Embed(title="Random Post from Nonsensopedia" , description=" ",color=0x00b300)
    
    try:       
        losuj_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Załaduj losową stronę [alt-shift-x]"]')))
        losuj_link.click()
        time.sleep(2)
        content = driver.find_element(By.XPATH, '//div[@class="mw-parser-output"]/p[1]')
        websitelink = driver.current_url
        print(content.text)
        PostDisplay.add_field(name="Random Post Scrapped", value=content.text , inline=False)
        PostDisplay.add_field(name="Current website", value=websitelink)
        PostDisplay.set_thumbnail(url=UseAVA)
        await sendWait.delete()
        await ctx.send(embed = PostDisplay)
        
    except NoSuchElementException:
        print("Unable to find element")
        await ctx.send('```Error: Could not find content element.```')
    except IndexError:
        await ctx.send("```list index out of range```")
    finally:
        driver.quit()
@client.command()        
async def GetFraze(ctx):
    waitEmbed = discord.Embed(title="" ,description="this may take a few seconds")
    waitEmbed.set_image(url="https://media.tenor.com/w_C4CpUBih4AAAAC/100.gif")
    sendWait =await ctx.send(embed = waitEmbed)
    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://www.miejski.pl/")
    PostDisplay = discord.Embed(title="Random Post from Słownik Miejski" , description="",color=0x00b300)
    try:
        ul_element = driver.find_element(By.ID ,'full-alpha-nav')
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        random_li = random.choice(li_elements)
        link = random_li.find_element(By.TAG_NAME, 'a')
        link.click()
        time.sleep(2)
        #-------------Get  underwebsite after get letter----------------
        Div = driver.find_element(By.ID, "pagination")
        a_elements = Div.find_elements(By.TAG_NAME, 'a')
        random_a =  random.choice(a_elements)
        driver.execute_script("arguments[0].scrollIntoView();", random_a)
        random_a.click()
        time.sleep(2)
        #-------------???????---------------------------------
        ul_elementV2 = driver.find_element(By.ID ,'simple-link-list')
        li_elementsV2 = ul_elementV2.find_elements(By.TAG_NAME, 'li')
        random_liV2 = random.choice(li_elementsV2)
        linkV2 = random_liV2.find_element(By.TAG_NAME, 'a')
        driver.execute_script("arguments[0].click();", linkV2)
        
        heder = driver.find_element(By.TAG_NAME, 'article')
        exept = heder.find_element(By.TAG_NAME , 'p')
        title = heder.find_element(By.TAG_NAME, 'header')
        quote = heder.find_element(By.TAG_NAME, 'blockquote')
        Date = heder.find_element(By.CLASS_NAME , 'published-date')
        Autor = heder.find_element(By.CLASS_NAME, 'author')
        
        link = driver.current_url
        print(heder.text)
        print("this is exept"+ exept.text)
        PostDisplay.add_field(name=title.text , value="" , inline=False)
        PostDisplay.add_field(name="", value="```"+exept.text+"```", inline=False)
        PostDisplay.add_field(name="", value="*" + quote.text + "*" )
        PostDisplay.add_field(name="Current Website", value=link ,inline=False)
        PostDisplay.set_footer(text=Date.text)
        PostDisplay.set_author(name=Autor.text)
        try:
            Tags = heder.find_element(By.CLASS_NAME, 'tags')
            PostDisplay.add_field(name="", value="```" + Tags.text + "```")
        except NoSuchElementException:
            pass
        finally:
            await sendWait.delete()
            await ctx.send(embed= PostDisplay)      
        time.sleep(2)
    except NoSuchElementException:
        await ctx.send("```Unable to find element or click link```")
    except IndexError:
        await ctx.send("```list index out of range```")
    finally:
        driver.quit()
 #@commands.is_owner() 
#@client.command()
#async def Shut(ctx):
#    await ctx.send("bye")
#    await client.close()
    
client.run(token)
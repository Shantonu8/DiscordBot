import discord
from discord.ext import commands
import os
import requests
import json
from keep_alive import keep_alive



client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def ping(ctx):
  await ctx.send(f'The ping to the server is {round(client.latency * 1000)} ms')

@client.command()
async def doge(ctx):
  response = requests.get('https://dog.ceo/api/breeds/image/random')
  dumped = json.dumps(response.json())
  parsed = json.loads(dumped)
  await ctx.send(parsed["message"])

@client.command()
async def cate(ctx):
  response  = requests.get('https://api.thecatapi.com/v1/images/search')
  dumped = json.dumps(response.json())
  parsed = json.loads(dumped)
  await ctx.send(parsed[0]["url"])
  
  
@client.command()
async def wallpaper(ctx):
  finalString = 'https://api.unsplash.com/photos/random?client_id=' + os.environ['unsplash']
  response  = requests.get(finalString)
  dumped = json.dumps(response.json())
  parsed = json.loads(dumped)
  await ctx.send(parsed["urls"]["raw"])


def getWeatherStatus(weather_status):
  if(weather_status == 'thunderstorm'):
    return 'thunderstorming'
  elif(weather_status == 'drizzle'):
    return 'drizzling'
  elif(weather_status == 'rain'):
    return 'raining'
  elif(weather_status == 'snow'):
    return 'snowing'
  elif(weather_status == 'clear'):
    return 'clear'
  elif(weather_status == 'clouds'):
    return 'cloudy'
  else:
    return 'misty'


@client.command()
async def weather(ctx, *, message):
  api_key  = os.environ['weather']

  try:
    if (message):
      response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message}&appid={api_key}")
      dumped = json.dumps(response.json())
      parsed = json.loads(dumped) 
      messageNew = message.capitalize()
      weather_status = parsed["weather"][0]["main"].lower()
      temp = round(parsed["main"]["temp"] - 271,2)
      humidity = parsed["main"]["humidity"]
      icon_id = parsed["weather"][0]["icon"]
      weather_status = getWeatherStatus(weather_status)
      await ctx.send(f'It is {weather_status} in {messageNew}. The temperature in {messageNew} is {temp} celcius. The humidity in {messageNew} is {humidity}.')
      await ctx.send(f'https://openweathermap.org/img/wn/{icon_id}@2x.png')
    else:
      ctx.send('Please enter the name of the city along with the command')
  except:
    ctx.send('Please enter a valid city name')    

@client.command()
async def purge(ctx):
  await ctx.channel.purge()




keep_alive()
client.run(os.getenv('TOKEN'))

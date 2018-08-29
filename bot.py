import discord
import asyncio
import json
import urllib3
urllib3.disable_warnings()
http = urllib3.PoolManager()
suffix = ['.jpg','.png','.gif','.bmp']
counter = 1
urlpartone = "https://reddit.com/r/"
urlpartthree = "/random.json"
checkerurl = ".json"
usertoken = input('What is your token? (NO QUOTES AT START OR END) ')
client = discord.Client()
@client.event
async def on_ready():
    print('We up, ready and logged in as...')
    print(client.user.name,' ',client.user.id)
    await client.change_presence(game=discord.Game(name='r!help | rb.daf.lol'))
@client.event
async def on_message(message):
    if message.content.startswith('r!help'):
        await client.send_message(message.channel, '`r!get subreddit`: Fetches image from any subreddit of your choice.')
    if message.content.startswith('r!get'):
        if " " in message.content[5]:
            if " " in message.content[6:]:
                await client.send_message(message.channel, 'You can\'t use a space in a subreddit!')
                return
            else:
                print('Passed space checks')
                print(message.content[6:])
                while True:
                    urlparttwo = message.content[6:]
                    tocheck = urlpartone + urlparttwo + checkerurl
                    response = http.request('GET',tocheck)
                    checkdata = response.data
                    parsecheck = json.loads(	checkdata)
                    if parsecheck['data']['dist'] == 0:
                        await client.send_message(message.channel, 'Invalid sub!')
                        return
                    else:
                        finalurl = urlpartone + urlparttwo + urlpartthree
                        while True:
                            response = http.request('GET',finalurl)
                            thedata = response.data
                            parsedjson = json.loads(thedata).decode()
                            img = parsedjson[0]['data']['children'][0]['data']['url']
                            if img.endswith('.png') or img.endswith('.jpg') or img.endswith('.gif'):
                                await client.send_message(message.channel, img)
                                return
                            else:
                                print('Not an image')
                                global counter
                                counter += 1
                            if counter == 11:
                                    await client.send_message(message.channel, 'Failed to get image after 10 tries. If you\'re sure there are images, try again. Bad luck!')
                                    return

                
        else:
            await client.send_message(message.channel, 'Incorrect syntax. use `r!get subreddit`')
            return
        
client.run(usertoken)

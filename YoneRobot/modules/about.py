import random 
import asynci
from telethon import event 

@client.on(events.NewMessage(pattern="^/about"))

async def_(event):
  if event.fwd_from:
     return
  h=(random.randrange(1))
  if h==1:
     await event.edit(f"hi there")

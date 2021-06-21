from YoneRobot.events import register
from YoneRobot import OWNER_ID
from YoneRobot import telethn as tbot
import os 
from PIL import Image, ImageDraw, ImageFont

        fonts = [
          "./YoneRobot/resources/Night Machine.otf"
          "./YoneRobot/resources/lethal-injector hollow2.otf"
          "./YoneRobot/resources/Deadly Advance.otf"
          "./YoneRobot/resources/Vampire Wars.otf"
          "./YoneRobot/resources/Chopsic.otf"
        ]
        chosen_font = random.choice(fonts)

@register(pattern="^/logo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('ρяσνι∂є ѕσмє тєχт тσ ∂яαω!')
       return
    else:
       pass
 await event.reply('cяєαтιηg уσυя ℓσgσ...ωαιт!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./YoneRobot/resources/20210621_141943.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "blue"
    font = ImageFont.truetype("./YoneRobot/resources/chosen_font", 330)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=30, stroke_fill="blue")
    fname2 = "LogoByYone.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="**мα∂є ву 𝐓𝐈𝐓𝐀𝐍 𝟐.𝟎**")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Report @TITANX_CHAT, {e}')



   
@register(pattern="^/ptxt ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('ρяσνι∂є ѕσмє тєχт тσ ρяιηт!')
       return
    else:
       pass
 await event.reply('ρяιηтιηg уσυя тєχт...ωαιт!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./YoneRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "blue"
    font = ImageFont.truetype("./YoneRobot/resources/Maghrib.ttf", 500)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=0, stroke_fill="white")
    fname2 = "LogoByYone.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="**мα∂є ву 𝐓𝐈𝐓𝐀𝐍 𝟐.𝟎**")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Report @TITANX_CHAT, {e}')

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")


__help__ = """
 ✮ /logo `<text>` **:**  TITAN BOT will Create your logo with your name given.

 ✮ /ptxt `<text>` **:** TITAN BOT prints your name as pic.
 """
__mod_name__ = "Lᴏɢᴏ🖼️"

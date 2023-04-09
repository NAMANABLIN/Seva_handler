from dotenv import load_dotenv
from os import getcwd, getenv, listdir, path, remove
from discord import Intents
import json
load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")
VK_TOKEN = getenv("VK_GRISHA")

intents = Intents.default()
intents.message_content = True

jsons = {}
pth = getcwd()
a = pth + '/jsons'
for x in listdir(a):
    jsons[x[:-5]] = json.load(open(a + "/" + x, 'rb'))

hearts='❤💙💚💜🧡💛🖤'
frm =['Twitter', 'Discord', 'Twitter/Discord']
# for x in jsons.items():
#     print(x)
# print(" ".join([jsons["hashs"][x] for x in ['РјРґ']]))
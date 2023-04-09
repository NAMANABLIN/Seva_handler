import json

import discord
from discord import app_commands
import vk_api
from config import DISCORD_TOKEN, VK_TOKEN, intents, jsons, frm, pth, path, remove
from random import choice, randint
from asyncio import sleep
import requests

from datetime import time

vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk_session)


# TODO улучшить проверку роли
# TODO добавить класс для улчшения
# TODO добавить кнопку для перехода на пост
# TODO добавить фото для показа в дискорде
# TODO добавить рандомизацию мастей карт

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=1049025410362515587))
        self.synced = True
        print("AAAAAAAA")


servers = [discord.Object(id=1049025410362515587)]
bot = abot()
tree = app_commands.CommandTree(bot)


@tree.command(name='add_post', description='Создаёт пост', guilds=servers)
async def add_post(interation: discord.Interaction, pub: str, artist: str, desc: str, hashtags: str, date: str,
                   photos: str):
    a = False
    for x in interation.user.roles:
        if x.name == '.':
            a = True
            break
    if a:
        try:
            if artist == '-':
                artist = ''
            else:
                rndm = jsons[pub]['random']
                artist = f'• Создатель - {artist}| {choice(frm)} ' \
                         f'{choice(rndm[0]) + choice(rndm[1]) if type(rndm) == list else choice(rndm)}\n\n'
            if desc == '-':
                desc = ''
            else:
                desc = f'•{desc}\n\n'
            if hashtags == '-':
                hashtags = ''
            else:
                hashtags = f'{" ".join([jsons[pub][x] for x in hashtags.split()])} {jsons[pub]["base"]}'
            if photos == "-":
                attachments = ''
            else:
                uphotos = []
                for x in photos.split():
                    r = requests.get(x)
                    if r.status_code == 200:
                        with open(f'photos/{x[x.rfind("/"):x.rfind(".")]}.png', 'wb') as f:
                            f.write(r.content)
                            uphotos.append(f'photos/{x[x.rfind("/"):x.rfind(".")]}.png')
                attachments = []
                for x in uphotos:
                    photo = upload.photo_wall(photos=x)[0]
                    remove(x)
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
            mes = artist + desc + hashtags
            if date == '-':
                vk.wall.post(owner_id=jsons[pub]["id"], message=mes, attachments=','.join(attachments))
                await interation.response.send_message('Post created!')
            else:
                a = await interation.response.send_message(mes + f'Пост будет выложен через {date}:00')
                hour = int(date) - 1
                for i in range(hour, -1, -1):
                    for j in range(1, 13):
                        await sleep(5 * 60)
                        # await a.edit(
                        #     content=mes + f'Пост будет выложен через {i}:{"0" if minute < 10 else ""}{minute}')
                vk.wall.post(owner_id=jsons[pub]["id"], message=mes, attachments=','.join(attachments))
                await interation.edit_original_response(content=mes + '\n\nPost created!')
        except Exception as e:
            if date == '-':
                await interation.response.send_message(f"Что то пошло не так\n{e}")
            else:
                await interation.edit_original_response(content=f"Что то пошло не так\n{e}")

            print(e)
    else:
        await interation.response.send_message(
            'https://images-ext-1.discordapp.net/external/Zu0SzHFM-foGbPu5G0lVzmeE7dKGwtMTHCgAcZ9BDIg/https/media.tenor.com/E6yGtiwZ4jkAAAPo/ultrakill-%25D1%2581%25D1%258A%25D0%25B5%25D0%25B1%25D0%25B0%25D0%25BB%25D0%25BE%25D1%2581%25D1%258C%25D1%2587%25D1%2583%25D0%25B4%25D0%25B8%25D1%2589%25D0%25B5.mp4')
        print('Лошня')


@tree.command(name='change', description='Изменить/добавить хэштеги для словаря', guilds=servers)
async def change(interation: discord.Interaction, pub: str, short: str, hashtags: str):
    a = False
    for x in interation.user.roles:
        if x.name == '.':
            a = True
            break
    if a:
        try:
            jsons[pub][short] = hashtags
            json.dump(jsons[pub], open(f'{pth}/jsons/{pub}.json', 'w'), indent=2, ensure_ascii=True)
            await interation.response.send_message("Новый/ие хэштег/и: " + jsons[pub][short])
        except KeyError:
            await interation.response.send_message("Такого паблика не существует, попробуй /all")
    else:
        await interation.response.send_message(
            'https://images-ext-1.discordapp.net/external/Zu0SzHFM-foGbPu5G0lVzmeE7dKGwtMTHCgAcZ9BDIg/https/media.tenor.com/E6yGtiwZ4jkAAAPo/ultrakill-%25D1%2581%25D1%258A%25D0%25B5%25D0%25B1%25D0%25B0%25D0%25BB%25D0%25BE%25D1%2581%25D1%258C%25D1%2587%25D1%2583%25D0%25B4%25D0%25B8%25D1%2589%25D0%25B5.mp4')
        print('Лошня')


@tree.command(name='all', description='Вывести все словари для хэштегов', guilds=servers)
async def all(interation: discord.Interaction):
    a = False
    for x in interation.user.roles:
        if x.name == '.':
            a = True
            break
    if a:
        await interation.response.send_message(', '.join([x for x in jsons.keys()]))
    else:
        await interation.response.send_message(
            'https://images-ext-1.discordapp.net/external/Zu0SzHFM-foGbPu5G0lVzmeE7dKGwtMTHCgAcZ9BDIg/https/media.tenor.com/E6yGtiwZ4jkAAAPo/ultrakill-%25D1%2581%25D1%258A%25D0%25B5%25D0%25B1%25D0%25B0%25D0%25BB%25D0%25BE%25D1%2581%25D1%258C%25D1%2587%25D1%2583%25D0%25B4%25D0%25B8%25D1%2589%25D0%25B5.mp4')
        print('Лошня')


@tree.command(name='give', description='Вывести содержимое словаря для хэштегов', guilds=servers)
async def give(interation: discord.Interaction, pub: str):
    a = False
    for x in interation.user.roles:
        if x.name == '.':
            a = True
            break
    if a:
        try:
            pub = jsons[pub]
            ans = []
            for x in pub.keys():
                ans.append(f'{x}: {pub[x]}')
            await interation.response.send_message('\n'.join(ans))
        except KeyError:
            await interation.response.send_message("Такого паблика не существует, попробуй /all")
    else:
        await interation.response.send_message(
            'https://images-ext-1.discordapp.net/external/Zu0SzHFM-foGbPu5G0lVzmeE7dKGwtMTHCgAcZ9BDIg/https/media.tenor.com/E6yGtiwZ4jkAAAPo/ultrakill-%25D1%2581%25D1%258A%25D0%25B5%25D0%25B1%25D0%25B0%25D0%25BB%25D0%25BE%25D1%2581%25D1%258C%25D1%2587%25D1%2583%25D0%25B4%25D0%25B8%25D1%2589%25D0%25B5.mp4')
        print('Лошня')


@tree.command(name='create', description='Создать новый словарь для хэштегов', guilds=servers)
async def create(interation: discord.Interaction, pub: str):
    a = False
    for x in interation.user.roles:
        if x.name == '.':
            a = True
            break
    if a:
        a = f'{pth}\\jsons\\{pub}.json'
        if path.exists(a):
            await interation.response.send_message("Такой словарь уже есть")
        else:
            jsons[pub] = {}
            json.dump(jsons[pub], open(pth + '/jsons/' + pub + '.json', 'w'), indent=2, ensure_ascii=True)
            await interation.response.send_message("Создан новый словарь для хэштегов")
    else:
        await interation.response.send_message(
            'https://images-ext-1.discordapp.net/external/Zu0SzHFM-foGbPu5G0lVzmeE7dKGwtMTHCgAcZ9BDIg/https/media.tenor.com/E6yGtiwZ4jkAAAPo/ultrakill-%25D1%2581%25D1%258A%25D0%25B5%25D0%25B1%25D0%25B0%25D0%25BB%25D0%25BE%25D1%2581%25D1%258C%25D1%2587%25D1%2583%25D0%25B4%25D0%25B8%25D1%2589%25D0%25B5.mp4')
        print('Лошня')


# @tree.command(name='delete', description='FEWFW', guilds=servers)
# async def create(interation: discord.Interaction, pub: str, short:str):
#     a = False
#     for x in interation.user.roles:
#         if x.name == '.':
#             a = True
#             break
#     if a:
#         try:
#             del jsons[pub][short]
#             json.dump(jsons[pub], open(f'{pth}/jsons/{pub}.json', 'w'), indent=2, ensure_ascii=True)
#             await interation.response.send_message("Новый/ие хэштег/и: " + jsons[pub])
#         except KeyError:
#             await interation.response.send_message("Такого паблика не существует, попробуй /all")
#     else:
#         await interation.response.send_message('https://images-ext-1.discordapp.net/external/Zu0SzHFM-foGbPu5G0lVzmeE7dKGwtMTHCgAcZ9BDIg/https/media.tenor.com/E6yGtiwZ4jkAAAPo/ultrakill-%25D1%2581%25D1%258A%25D0%25B5%25D0%25B1%25D0%25B0%25D0%25BB%25D0%25BE%25D1%2581%25D1%258C%25D1%2587%25D1%2583%25D0%25B4%25D0%25B8%25D1%2589%25D0%25B5.mp4')
#         print('Лошня')

@tree.command(name='help', description='Изменить/добавить хэштеги для словаря', guilds=servers)
async def change(interation: discord.Interaction):
    a = False
    for x in interation.user.roles:
        if x.name == '.':
            a = True
            break
    if a:
        await interation.response.send_message(
            'У каждой команды есть своё описание, дублировать сюда я его не буду.\n\n'
            'pub - название паблика\n'
            'short - сокращение хэштегов\n'
            'hashtags - сокращения через пробел\n'
            'artist - автор изображения\n'
            'desc - описание\n'
            'date - через сколько часов выйдет пост\n'
            'photos - вводятся ссылки на фото через пробел\n\n'
            'Если не нужно вводить параметр, то просто впиши -, единственное, нужно '
            'обязательно чтобы что-то одно было(desc, artisti, photos)')
    else:
        await interation.response.send_message(
            'https://images-ext-1.discordapp.net/external/Zu0SzHFM-foGbPu5G0lVzmeE7dKGwtMTHCgAcZ9BDIg/https/media.tenor.com/E6yGtiwZ4jkAAAPo/ultrakill-%25D1%2581%25D1%258A%25D0%25B5%25D0%25B1%25D0%25B0%25D0%25BB%25D0%25BE%25D1%2581%25D1%258C%25D1%2587%25D1%2583%25D0%25B4%25D0%25B8%25D1%2589%25D0%25B5.mp4')
        print('Лошня')


bot.run(DISCORD_TOKEN)

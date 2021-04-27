import discord
import os
import json
from threading import Thread
import PIL.Image as Image
import requests
import random
from bs4 import BeautifulSoup
from io import BytesIO
import googletrans

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "cookie": "fst=1; yuidss=9597109791603910568; yandexuid=9597109791603910568; ymex=1919270568.yrts.1603910568#1919270568.yrtsi.1603910568; _ym_uid=1603919398924476944; mda=0; gdpr=0; my=YwA=; font_loaded=YSv1; L=AQlXaAZEWAN3bA54VglvWEUDUAN9Q3h5EiMjAi0nSS4FJSA0.1604078494.14404.320154.f9555eb4c296b42410f446a19031d667; yandex_login=kkkkck.vanya; yandex_gid=213; is_gdpr=0; is_gdpr_b=CLuMORC4DygC; instruction=1; computer=1; HOhdORSx=1; FxuGQqNNo=1; kNAcVGYFWhx=1; jsOmqPGh=1; _ym_d=1607776178; zm=m-white_bender_zen-ssr.gen.webp.css-https%3As3home-static_x5pZlL7gT5De5cCi1ZUS6I6b154%3Al; NBgfDVFir=1; i=7MRuY3US6wnHeg5zANgXQnHQaltvDM91bhQb4n5WpLBHIl9tf7NxnJlkPDl+pmyiYQOehgjK1lfDx3AwzaWtjy7PNvw=; yabs-frequency=/5/0000000000000000/q_ToS9G0001uFa4Y841jXW0007W-8OkHSd2K0000U3uX9HL1ROO0001mFYUa1NDmb00007W-869ui72L0000U3uWQcwmS9K0001uFc29Rx1mbG0003i-_F___m1ki72L0000U3vW-rImS9K0001uFc3rRh1mbG0007W-GEnKi72L0000U3wW/; Session_id=3:1608233851.5.0.1604078494220:LI3jFw:cd.1|231794600.0.2|227433.356085.-sVXqI6p7X3D7l_00Upsfm612bk; sessionid2=3:1608233851.5.0.1604078494220:LI3jFw:cd.1|231794600.0.2|227433.307479.1VmXCnGzhdvzF5O7lPM5O1jQbfc; _ym_isad=1; bltsr=1; _ym_visorc_26812653=b; yp=1924464026.sp.aflt%3A1608240026#1608326388.nps.8639673365%3Aclose#1638251285.ygu.1#1919438494.udn.cDpra2trY2sudmFueWE%3D#1610368637.los.1#1639312634.p_sw.1607776633#1623544181.szm.1:1920x1080:1480x880#1610368637.losc.0"}

NOTFOUNDIMAGE=json.loads(list(BeautifulSoup(requests.get("https://yandex.ru/images/search?text=not%20found", headers=headers).content, 'html.parser').find_all("div", class_="serp-item"))[0].get("data-bem"))['serp-item']['preview'][0]['url']


def save_img(img, i):
    
    try:
      response = requests.get(img)
      image = Image.open(BytesIO(response.content))
      filename = str(i) + '.png'
      image.save('images\\'+filename)
    except Exception:
        pass

save_img(NOTFOUNDIMAGE,'not_found')

def get_true_link(text,c):
    lnk = "https://yandex.ru/images/search?text=" + text
    try:
        page = requests.get(lnk, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        imgs = soup.find_all("div", class_="serp-item")
        img_lst=list(imgs)
        save_img(json.loads(img_lst[random.randrange(0,len(img_lst))].get("data-bem"))['serp-item']['preview'][0]['url'], c)
    except(Exception):
        save_img(NOTFOUNDIMAGE, c)

def get_all_images_async(file):
    threads = []
    words = file.split()
    for i in range(len(words)):
        process = Thread(target=get_true_link, args=[words[i], i])
        threads.append(process)
        process.start()

    for prc in threads:
        prc.join()
    threads.clear()

def get_all_images_async_lim(file,lim):
    threads = []
    words = file.split()
    for i in range(len(words)):
        process = Thread(target=get_true_link, args=[words[i], i])
        threads.append(process)
        process.start()
        if len(threads) >= lim:
            for prc in threads:
                prc.join()
            threads.clear()
    for prc in threads:
        prc.join()
    threads.clear()


def tti(file):
    lines = file.strip('\n').split('\n')
    max = 0
    for line in lines:
        l = len(line.split(' '))
        if l > max:
            max = l
    id = 0

    s = 10

    result = Image.new('RGBA', (max * 128 * s, len(lines) * 96 * s))

    for i in range(len(lines)):
        words = lines[i].split()
        for j in range(len(words)):
            try:
                im = Image.open("images\\" + str(id) + ".png")
            except(Exception):
                im = Image.open("images\\not_found.png")
            # im.thumbnail((128*s,96*s))
            im = im.resize((128 * s, 96 * s))
            result.paste(im, (j * 128 * s, i * 96 * s))
            id += 1
    result.save("result\\result.png")

def thumbnail_result(factor):
    thumb = Image.open("result\\result.png")
    thumb = thumb.resize((thumb.size[0]//factor,thumb.size[1]//factor))
    thumb.save("result\\resultThumb"+str(factor)+".png")





client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/help '):
        text = message.content.strip('/help ')
        await message.channel.send(text)
        sentenses = text.split("\n")
        
        t = googletrans.Translator()
       
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en,ru;q=0.9,hu;q=0.8,ru-RU;q=0.7,en-US;q=0.6",
            'cache-control': "max-age=0",
            'content-length': "1492",
            'content-type': "application/x-www-form-urlencoded",
            'origin': "https://englishforbusy.ru",
            'referer': "https://englishforbusy.ru/transliterator/",
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': "?0",
            'sec-fetch-dest': "document",
            'sec-fetch-mode': "navigate",
            'sec-fetch-site': "same-origin",
            'sec-fetch-user': "?1",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

        }

        data = {
            'action': 'bukvoed_form',
            'redirect': 'https://englishforbusy.ru/transliterator/',
            'message':'1. A force applied to a body causes it to move in a straight line.'
        }





        x1=[]
        x2=[]
        x3=[]
        for s in sentenses:
            s=s.strip("\n")
            x1.append(s)
            translated = t.translate(s, src='en', dest='ru')
            x2.append(translated.text)
            data['message']=s
            r = requests.post('https://englishforbusy.ru/transliterator/', headers=headers, data=data)
            x3.append(r.content.decode('UTF-8').split('name="result"')[1].split("<")[0].split(">")[1])

        ans=""
        for i in range(len(x1)):
            ans+=x1[i]+"\n"+x3[i].replace(" Ди "," Зэ ").replace(" ди "," зэ ").replace("тф","ф").replace("Тф","Ф").replace(" Тын "," Финг ").replace(" тын "," финг ")+"\n"+x2[i]+"\n"+"\n"
        await message.channel.send(ans)



    if message.content.startswith('/tti '):
        text = message.content.strip('/tti ')
        await message.channel.send('Searching Photos')
        get_all_images_async_lim(text,128)
        await message.channel.send('Combining into one image')
        tti(text)
        await message.channel.send('Creating attachment')
        try:
            await message.channel.send(file=discord.File("result\\result.png"))
        except(Exception):
            await message.channel.send(
                'Your message is too big for discord,but I will scale it down, if you want full resolution, then you need to contact my creator at kkkkck.vanya@yandex.ru')
            try:
                thumbnail_result(2)
                await message.channel.send(file=discord.File("result\\resultThumb2.png"))
            except(Exception):
                await message.channel.send(
                    'Still to big for discord, scaling down more...')
                try:
                    thumbnail_result(4)
                    await message.channel.send(file=discord.File("result\\resultThumb4.png"))
                except(Exception):
                    await message.channel.send(
                        'You know, that is quite a big image, scaling down even more...')
                    try:
                        thumbnail_result(8)
                        await message.channel.send(file=discord.File("result\\resultThumb8.png"))
                    except(Exception):
                        await message.channel.send(
                            'OMG that image is SO BIG, doing SUPER DOWN SCALE!!!')
                        try:
                            thumbnail_result(32)
                            await message.channel.send(file=discord.File("result\\resultThum32.png"))
                        except(Exception):
                            await message.channel.send(
                                'WTF? I cant send images of THAT sizes (if you REALLY need one contact my creator)')

client.run(os.getenv('BOT2_TOKEN'))

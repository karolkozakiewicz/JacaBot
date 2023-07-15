
# -*- coding: utf-8 -*-
import discord
import asyncio
from StreamChecker import StreamChecker
import datetime

# Tworzenie klienta bota
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

# Token Twojego bota Discord
TOKEN = 'TU TOKEN'

# ID kanału, na którym chcesz wysyłać powiadomienia
channel_id = 840540315010072596

# Tworzenie obiektu StreamChecker
checker = StreamChecker()
checker.start_checking_stream()

first_run = True

# Funkcja sprawdzająca, czy stream jest włączony


def check_stream():
    if checker.status:
        return True
    else:
        return False


async def send_notification():
    channel = client.get_channel(channel_id)

    embed = discord.Embed(title="Stream ON", url="https://raszei.com",
                          description="https://raszei.com", color=0xff0000)
    embed.set_author(name="Chłopaki z Raszei", url="https://raszei.com",
                     icon_url="https://raszei.com/assets/img/Site-favicon.webp")
    embed.set_thumbnail(url="https://raszei.com/assets/img/Bez%20nazwy-1.png")
    embed.add_field(name="Zapraszamy", value="", inline=True)
    _time = datetime.datetime.now()
    _time = _time.strftime("%Y-%m-%d %H:%M:%S")
    embed.set_footer(text=_time)
    last_status = False
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)

    while not client.is_closed():
        status = check_stream()  # Wywołanie funkcji sprawdzającej status streamu
        if (last_status == False and status == True):
            await channel.send(embed=embed)
            last_status = True

        if (last_status == True and status == False):
            last_status = False

        await asyncio.sleep(5)
        # print(f"{last_status} - {status}")

# Event ready, wywoływany, gdy bot jest gotowy do użycia


@client.event
async def on_ready():
    print(f'Zalogowano jako {client.user.name}')
    asyncio.create_task(send_notification())

# Uruchomienie bota
client.run(TOKEN)

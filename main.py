import discord
from discord.ext import commands
import random, string
import requests
from urllib.request import Request, urlopen
from discord import Permissions
from colorama import Fore, Style
import asyncio, os, sys, socket, datetime
from discord.ext.commands import MemberConverter
from discord.ext.commands import CommandNotFound
import shutil
from screenshotone import Client, TakeOptions
import socket
import time
import threading, re, json
from discord import SyncWebhook

from queue import Queue

ADMIN = 123 # Your User ID
logchannel = 123 # Channel ID To Send Logs To
screenshot = Client("Api Key", "Access Key") # Get Them From Screenshotone.com
zenrowkey = "Api Key" # Get It From Zenrows.com
WEBHOOK = "Your Webhook URL" # Put Your Webhook URL Here
log_channel = False # Do Not Touch
fcid = 0 # Do Not Touch
tcid = 0 # Do Not Touch
LOGWEB = "" # Do Not Touch
SNIPEUSER = 1, 2, 3 # User IDs For Snipe Commands

prefix = "." # You Can Change The Prefix But Do Not Touch These Things Below
uptime = None
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(
    command_prefix=prefix,
    help_command=None,
    intents=intents,
    chunk_guilds_at_startup=False,
)
snipe_message_author = {}
snipe_message_content = {}
snipe_image_content = {}
snipe_image_author = {}
snipe_image_message = {}
client.launch_time = datetime.datetime.utcnow()

languages = {
    "hu": "Hungarian, Hungary",
    "nl": "Dutch, Netherlands",
    "no": "Norwegian, Norway",
    "pl": "Polish, Poland",
    "pt-BR": "Portuguese, Brazilian, Brazil",
    "ro": "Romanian, Romania",
    "fi": "Finnish, Finland",
    "sv-SE": "Swedish, Sweden",
    "vi": "Vietnamese, Vietnam",
    "tr": "Turkish, Turkey",
    "cs": "Czech, Czechia, Czech Republic",
    "el": "Greek, Greece",
    "bg": "Bulgarian, Bulgaria",
    "ru": "Russian, Russia",
    "uk": "Ukranian, Ukraine",
    "th": "Thai, Thailand",
    "zh-CN": "Chinese, China",
    "ja": "Japanese",
    "zh-TW": "Chinese, Taiwan",
    "ko": "Korean, Korea",
}

locales = [
    "da",
    "de",
    "en-GB",
    "en-US",
    "es-ES",
    "fr",
    "hr",
    "it",
    "lt",
    "hu",
    "nl",
    "no",
    "pl",
    "pt-BR",
    "ro",
    "fi",
    "sv-SE",
    "vi",
    "tr",
    "cs",
    "el",
    "bg",
    "ru",
    "uk",
    "th",
    "zh-CN",
    "ja",
    "zh-TW",
    "ko",
]


@client.event
async def on_message_delete(message):
    snipe_message_author.setdefault(message.channel.id, []).append(message.author)
    snipe_message_content.setdefault(message.channel.id, []).append(message.content)

    if message.attachments:
        for attachment in message.attachments:
            urls = attachment.url
            snipe_image_content.setdefault(message.channel.id, []).append(urls)
            snipe_image_author.setdefault(message.channel.id, []).append(message.author)
            snipe_image_message.setdefault(message.channel.id, []).append(
                message.content
            )
    await asyncio.sleep(60)


@client.event
async def on_bulk_message_delete(messages):
    for msg in list(messages):
        message = msg.content
        channelid = msg.channel.id
        author = msg.author
        attachment = msg.attachments
        snipe_message_content.setdefault(channelid, []).append(message)
        snipe_message_author.setdefault(channelid, []).append(author)

        if attachment:
            for img in attachment:
                urls = img.url
                snipe_image_content.setdefault(channelid, []).append(urls)
                snipe_image_author.setdefault(channelid, []).append(author)
                snipe_image_message.setdefault(channelid, []).append(message)
    await asyncio.sleep(60)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title=f"**Command Not Found!**",
            description=f"Type {prefix}help For Command List.",
            color=discord.Color.red(),
            timestamp=ctx.message.created_at,
        )
        await ctx.send(embed=embed)


@client.event
async def on_ready():
    os.system("clear")
    print("[ + ] " + Fore.GREEN + f"{client.user} Is Ready!" + Fore.RESET)
    print("\n[ + ] " + Fore.GREEN + f"Bot Prefix Is {prefix}" + Fore.RESET)
    print(
        "\n[ + ] "
        + Fore.GREEN
        + f"Bot Is Online In {len(client.guilds)} Servers"
        + Fore.RESET
    )
    for guilds in client.guilds:
        print(
            "\n[ + ] "
            + Fore.MAGENTA
            + "Server Name : "
            + guilds.name
            + Fore.RESET
            + "\n~~~~> "
            + Fore.MAGENTA
            + "Server ID : "
            + str(guilds.id)
            + Fore.RESET
        )
    activity = discord.Game(
        name=f"Discord Multi-Purpose Bot | {client.user} | {prefix}HELP"
    )
    await client.change_presence(status=discord.Status.idle, activity=activity)


@client.command()
async def get(ctx, link):
    await ctx.reply("Please Wait A Few Seconds", delete_after=0.5)

    if "https://" not in link and "http://" not in link:
        link = "https://" + link

    session = requests.Session()
    response = session.get(
        link,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0"
        },
    )

    with open("data.txt", "w") as file:
        file.write(response.text)
        file.close()
    await ctx.send("Print Output (p) or Send File (s)")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msgs = await client.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("You Didn't Reply In Time.")

    if msgs.content == "p":
        with open("data.txt", "r") as file:
            msg = file.read(2000).strip()
            while len(msg) > 0:
                embed = discord.Embed(
                    title=link.lower(),
                    description=f"{msg}",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow(),
                )
                user = ctx.author
                await user.send(embed=embed)
                msg = file.read(2000).strip()
    else:
        user = ctx.author
        await user.send(file=discord.File("data.txt"))


@client.command()
async def render(ctx, wrld):
    urls = f"https://s3.amazonaws.com/world.growtopiagame.com/{wrld}.png"
    req = requests.get(urls)
    if req.status_code == 200:
        await ctx.send("Please Wait A Few Seconds", delete_after=1)
        embed = discord.Embed(
            title=f"Render Of {wrld.upper()}", color=discord.Color.green()
        )
        embed.set_image(url=urls)
        await ctx.reply(embed=embed)
    else:
        await ctx.send("Please Wait A Few Seconds", delete_after=1)
        embeds = discord.Embed(
            title=f"World : {wrld.upper()}",
            description="Not Found 404",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embeds)


@client.command()
async def server(ctx):
    if ctx.author.id == ADMIN:
        for guild in client.guilds:
            stats = discord.Embed(title="Server List", color=discord.Colour.random())
            stats.add_field(
                name=f"**Server Name** : {guild.name}",
                value=f"**Server ID** : {str(guild.id)}",
                inline=True,
            )
            await ctx.send(embed=stats)
    else:
        await ctx.send("You Don't Have Permission For This Command")


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.message.delete()
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=limit)
    purge_embed = discord.Embed(
        title=f"Purge [{prefix}purge]",
        description=f"Successfully purged {limit} messages. \nCommand executed by {ctx.author}.",
        color=discord.Colour.random(),
    )
    purge_embed.set_footer(text=str(datetime.datetime.now()))
    await ctx.channel.send(embed=purge_embed, delete_after=True)


class MyView(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=180)
        self.author = author

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        embed = discord.Embed(
            title="Timeout",
            description="You Did Not Respond Within 3 Minutes",
            color=discord.Color.magenta(),
        )
        embed.set_thumbnail(url=client.user.avatar.url)
        embed.set_footer(text=f"Type {prefix}help To View Help Menu Again")
        await self.message.edit(embed=embed, view=self)

    async def on_timeout(self) -> None:
        await self.disable_all_items()

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.success)
    async def first_help_callback(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        delta_uptime = datetime.datetime.utcnow() - client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(
            title=f"Hello, I am {client.user}",
            description="Click On One Of The Buttons Below To View The Help Menu.",
            color=discord.Color.random(),
        )
        embed.add_field(
            name="Bot Info",
            value=f"Online Time: **{days}d, {hours}h, {minutes}m, {seconds}s** | Ping: **{round(client.latency*1000)} Ms**",
            inline=False,
        )
        embed.set_thumbnail(url=client.user.avatar.url)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="User", style=discord.ButtonStyle.primary)
    async def second_help_callback(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        embed = discord.Embed(title="Help Menu", color=discord.Color.blue())
        embed.add_field(
            name=f"{prefix}render", value="<name of gt world>", inline=False
        )
        embed.add_field(name=f"{prefix}purge", value="<amount of msgs>", inline=False)
        embed.add_field(
            name=f"{prefix}snipe",
            value="<number of msg>, Returns Most Current Deleted Msgs If Argument Is Left Blank",
            inline=False,
        )
        embed.add_field(
            name=f"{prefix}snipeimg",
            value="<number of attachment>, Returns Most Current Deleted Attachments If Argument Is Left Blank",
            inline=False,
        )
        embed.add_field(name=f"{prefix}get", value="<website url>", inline=False)
        embed.add_field(
            name=f"{prefix}tdox/tokeninfo",
            value="Provide The Token In Bot's Dm",
            inline=False,
        )
        embed.add_field(
            name=f"{prefix}porthelp", value="Help Menu Of Port Scanner", inline=False
        )
        embed.add_field(
            name=f"{prefix}ttb",
            value="<text> INFO : Convert Texts To Binary",
            inline=False,
        )
        embed.add_field(
            name=f"{prefix}btt",
            value="<binary code> INFO : Convert Binary To Texts",
            inline=False,
        )
        embed.add_field(name=f"{prefix}ss", value="<website url>", inline=False)
        embed.add_field(
            name=f"{prefix}gtport",
            value="Fetch IP & Ports From Growtopia Server",
            inline=False,
        )
        embed.add_field(name=f"{prefix}check", value="<ip/website url>", inline=False)
        embed.add_field(name=f"{prefix}ping", value="Shows Bot Latency", inline=False)
        embed.set_thumbnail(url=client.user.avatar.url)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Owner", style=discord.ButtonStyle.primary)
    async def third_help_callback(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        owner = discord.Embed(title="Help Menu (Owner Only)", color=discord.Color.red())
        owner.add_field(
            name=f"{prefix}server",
            value="Get a List Of Servers The Bot Joined",
            inline=False,
        )
        owner.add_field(name=f"{prefix}invite", value="<server id>", inline=False)
        owner.add_field(
            name=f"{prefix}start",
            value="<channel id> INFO : Logs Messages From a Channel",
            inline=False,
        )
        owner.add_field(name=f"{prefix}stop", value="Stops Logging Message")
        owner.set_thumbnail(url=client.user.avatar.url)
        await interaction.response.edit_message(embed=owner)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return interaction.user.id == self.author.id
        else:
            await interaction.response.send_message(
                "You Cannot Interact With This Message", ephemeral=True
            )


@client.command(aliases=["HELP"])
async def help(ctx):
    delta_uptime = datetime.datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(
        title=f"Hello, I am {client.user}",
        description="Click On One Of The Buttons Below To View The Help Menu.",
        color=discord.Color.random(),
    )
    embed.add_field(
        name="Bot Info",
        value=f"Online Time: **{days}d, {hours}h, {minutes}m, {seconds}s** | Ping: **{round(client.latency*1000)} Ms**",
        inline=False,
    )
    embed.set_thumbnail(url=client.user.avatar.url)
    view = MyView(ctx.author)
    message = await ctx.send(embed=embed, view=view)
    view.message = message


@client.command()
async def snipe(ctx, arg: int = None):
    channel = ctx.channel
    if ctx.author.id in SNIPEUSER:
        try:
            args = len(list(snipe_message_content[ctx.channel.id]))
            pass
        except:
            await ctx.send(f"There are no deleted messages in #{channel.name}")
            return

        if arg is None:
            arg = args - 1
            argz = arg + 1
            pass
        else:
            arg = arg - 1
            argz = arg + 1
            pass

        snipeEmbed = discord.Embed(
            title=f"Currently viewing {argz}/{args} of deleted messages in #{channel.name}",
            description=list(snipe_message_content[ctx.channel.id])[arg],
            color=discord.Color.red(),
        )
        snipeEmbed.set_footer(
            text=f"Deleted by {list(snipe_message_author[ctx.channel.id])[arg]}"
        )
        await ctx.send(embed=snipeEmbed)
    else:
        await ctx.reply("No Permission")


@client.command()
async def snipeimg(ctx, arg: int = None):
    channel = ctx.channel
    if ctx.author.id in SNIPEUSER:
        try:
            args = len(list(snipe_image_content[ctx.channel.id]))
            pass
        except:
            await ctx.send(f"There are no deleted attachments in #{channel.name}")
            return

        if arg is None:
            arg = args - 1
            argz = arg + 1
            pass
        else:
            arg = arg - 1
            argz = arg + 1
            pass

        snipeImage = discord.Embed(
            title=f"Currently viewing {argz}/{args} of deleted attachments in #{channel.name}",
            description=f"{list(snipe_image_message[ctx.channel.id])[arg]}",
            color=discord.Color.red(),
        )
        snipeImage.add_field(
            name="Attachment Link",
            value=f"[Click Here To View Link]({list(snipe_image_content[ctx.channel.id])[arg]})",
        )
        snipeImage.set_footer(
            text=f"Deleted By {list(snipe_image_author[ctx.channel.id])[arg]}"
        )
        snipeImage.set_image(url=f"{list(snipe_image_content[ctx.channel.id])[arg]}")
        await ctx.send(embed=snipeImage)
    else:
        await ctx.reply("No Permission")


@client.command()
async def check(ctx, ip: str = None):
    if ip is None:
        await ctx.send("Please sepcify an IP address")
        return
    else:
        try:
            with requests.session() as ses:
                resp = ses.get(f"https://ipinfo.io/{ip}/json")
                if "Wrong ip" in resp.text:
                    await ctx.send("Invalid IP address")
                    return
                else:
                    try:
                        j = resp.json()
                        embed = discord.Embed(
                            color=discord.Colour.red(),
                            title=f"INFO",
                            timestamp=datetime.datetime.utcnow(),
                        )
                        embed.add_field(name=f"IP", value=f"{ip}", inline=True)
                        embed.add_field(name=f"City", value=f'{j["city"]}', inline=True)
                        embed.add_field(
                            name=f"Region", value=f'{j["region"]}', inline=True
                        )
                        embed.add_field(
                            name=f"Country", value=f'{j["country"]}', inline=True
                        )
                        embed.add_field(
                            name=f"Coordinates", value=f'{j["loc"]}', inline=True
                        )
                        embed.add_field(
                            name=f"Postal", value=f'{j["postal"]}', inline=True
                        )
                        embed.add_field(
                            name=f"Timezone", value=f'{j["timezone"]}', inline=True
                        )
                        embed.add_field(
                            name=f"Organization", value=f'{j["org"]}', inline=True
                        )
                        embed.set_footer(
                            text="これを使用していただきありがとうございます"
                        )
                        await ctx.send(embed=embed)
                    except discord.HTTPException:
                        await ctx.send(
                            f'**{ip} Info**\n\nCity: {j["city"]}\nRegion: {j["region"]}\nCountry: {j["country"]}\nCoordinates: {j["loc"]}\nPostal: {j["postal"]}\nTimezone: {j["timezone"]}\nOrganization: {j["org"]}'
                        )
        except Exception as e:
            await ctx.send(f"Error: {e}")


@client.command(aliases=["tokinfo", "tdox"])
async def tokeninfo(ctx):
    await ctx.message.delete()
    user = ctx.author
    await ctx.send("Please Check Your Dm")
    await user.send("Input Discord Token Here")

    def check(m):
        return m.author == ctx.author and str(m.channel.type) == "private"

    try:
        msg = await client.wait_for("message", check=check, timeout=120)
        _token = msg.content
    except asyncio.TimeoutError:
        await user.send("Timeout.You Didn't Send Discord Token within 2 Minutes")
    headers = {"Authorization": _token, "Content-Type": "application/json"}
    try:
        res = requests.get(
            "https://canary.discordapp.com/api/v6/users/@me", headers=headers
        )
        res = res.json()
        user_id = res["id"]
        locale = res["locale"]
        avatar_id = res["avatar"]
        language = languages.get(locale)
        creation_date = datetime.datetime.utcfromtimestamp(
            ((int(user_id) >> 22) + 1420070400000) / 1000
        ).strftime("%d-%m-%Y %H:%M:%S UTC")
    except KeyError:
        headers = {"Authorization": "Bot " + _token, "Content-Type": "application/json"}
        try:
            res = requests.get(
                "https://canary.discordapp.com/api/v6/users/@me", headers=headers
            )
            res = res.json()
            user_id = res["id"]
            locale = res["locale"]
            avatar_id = res["avatar"]
            language = languages.get(locale)
            creation_date = datetime.datetime.utcfromtimestamp(
                ((int(user_id) >> 22) + 1420070400000) / 1000
            ).strftime("%d-%m-%Y %H:%M:%S UTC")
            em = discord.Embed(
                description=f"Name: `{res['username']}#{res['discriminator']} ` **BOT**\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`"
            )
            fields = [
                {"name": "Flags", "value": res["flags"]},
                {"name": "Local language", "value": res["locale"] + f"{language}"},
                {"name": "Verified", "value": res["verified"]},
            ]
            for field in fields:
                if field["value"]:
                    em.add_field(name=field["name"], value=field["value"], inline=False)
                    em.set_thumbnail(
                        url=f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}"
                    )
            return await user.send(embed=em)
        except KeyError:
            await user.send("Invalid token")
    em = discord.Embed(
        description=f"Name: `{res['username']}#{res['discriminator']}`\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`"
    )
    nitro_type = "None"
    if "premium_type" in res:
        if res["premium_type"] == 2:
            nitro_type = "Nitro Premium"
        elif res["premium_type"] == 1:
            nitro_type = "Nitro Classic"
    fields = [
        {"name": "Phone", "value": res["phone"]},
        {"name": "Flags", "value": res["flags"]},
        {"name": "Local language", "value": res["locale"] + f"{language}"},
        {"name": "MFA", "value": res["mfa_enabled"]},
        {"name": "Verified", "value": res["verified"]},
        {"name": "Nitro", "value": nitro_type},
    ]
    for field in fields:
        if field["value"]:
            em.add_field(name=field["name"], value=field["value"], inline=False)
            em.set_thumbnail(
                url=f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}"
            )
    return await user.send(embed=em)


@client.command()
async def porthelp(ctx):
    embed = discord.Embed(
        title=f"""Usage Of {prefix}scan <ip/url> Scan For Open Ports""",
        description=f"""{prefix}scan 127.0.0.1\n\n\n\n\n**Port Scanner Tools By : https://github.com/inforkgodara/python-port-scanner**""",
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=ctx.author.avatar.url)
    await ctx.send(embed=embed)


@client.command()
async def scan(ctx, ipa):
    socket.setdefaulttimeout(0.25)
    lock = threading.Lock()
    host = socket.gethostbyname(ipa)
    await ctx.send("Scanning on IP Address: " + host)
    fi = open("ports.txt", "r+")
    fi.truncate(0)
    fil = open("ports.txt", "w")
    fil.close()

    def scan(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = sock.connect((host, port))
            with lock:
                print(str(port), "is open")
                f = open("ports.txt", "a")
                f.write(str(port) + " is open\n")
                f.close()
                con.close()
        except:
            pass

    def execute():
        while True:
            worker = queue.get()
            scan(worker)
            queue.task_done()

    queue = Queue()
    start_time = time.time()
    for x in range(100):
        thread = threading.Thread(target=execute)
        thread.daemon = True
        thread.start()
    for worker in range(1, 1024):
        queue.put(worker)
    queue.join()
    fol = open("ports.txt", "r")
    mug = fol.readlines()
    new_sentences = [re.sub(r"\n+", "", s) for s in mug]
    await ctx.send(new_sentences)
    await ctx.send("Time taken:" + str(time.time() - start_time))


@client.command()
async def btt(ctx, *, bit):
    revert = "".join([chr(int(s, 2)) for s in bit.split()])
    embed = discord.Embed(
        title="Binary To Text",
        description=f"Binary : {bit}"
        + "\n\nConverted To"
        + f"\n\nText : {revert}"
        + "\n\n[Source](https://stackoverflow.com/a/48219616)",
        color=discord.Color.red(),
    )
    await ctx.send(embed=embed)


@client.command()
async def ttb(ctx, *, ans):
    out = " ".join(format(ord(x), "b") for x in ans)
    embed = discord.Embed(
        title="Text To Binary",
        description=f"Text : {ans}"
        + "\n\nConverted To"
        + f"\n\nBinary : {out}"
        + "\n\n[Source](https://stackoverflow.com/a/48219616)",
        color=discord.Color.red(),
    )
    await ctx.send(embed=embed)


@client.command()
async def gtport(ctx):
    wait = discord.Embed(
        title="Please wait for a few seconds as the bot is fetching the url",
        color=discord.Colour.random(),
    )
    await ctx.send(embed=wait, delete_after=True)
    url = "https://www.growtopiagame.com/growtopia/server_data.php"
    apikey = zenrowkey
    params = {
        "url": url,
        "apikey": apikey,
        "js_render": "true",
    }
    response = requests.get("https://api.zenrows.com/v1/", params=params)
    if "209.59.191.76" in response.text:
        port = response.text[51:56]
        ip = "209.59.191.76"
    else:
        port = response.text[53:59]
        ip = response.text[32:47]
    rst = discord.Embed(title="Growtopia Server", color=discord.Colour.random())
    rst.add_field(
        name="Server IP & Port", value=f"IP : {ip}\nPort : {port}", inline=False
    )
    rst.add_field(name="Full Information", value=f"{response.text}", inline=False)
    await ctx.send(embed=rst)


@client.command()
async def ss(ctx, urlx):
    wait = discord.Embed(
        title="Please wait for a few seconds", color=discord.Colour.random()
    )
    await ctx.send(embed=wait, delete_after=True)
    if "https://" not in urlx and "http://" not in urlx:
        urlx = "https://" + urlx
    try:
        options = (
            TakeOptions.url(urlx)
            .format("png")
            .viewport_width(1024)
            .viewport_height(768)
            .block_cookie_banners(True)
            .block_chats(True)
        )
        image = screenshot.take(options)
        with open("result.png", "wb") as result_file:
            shutil.copyfileobj(image, result_file)
        file = discord.File("result.png")
        embed = discord.Embed(
            description=f"Screenshot Of {urlx.lower()}", color=discord.Colour.random()
        )
        embed.set_image(url="attachment://result.png")
        await ctx.send(embed=embed, file=file)
    except:
        error = discord.Embed(
            title="Request Failed",
            description="Invalid Url",
            color=discord.Colour.random(),
        )
        await ctx.send(embed=error)


@client.event
async def on_command(ctx):
    user = ctx.author
    avatar = ctx.author.avatar.url
    command = ctx.command
    server = ctx.guild.name
    channel = client.get_channel(logchannel)
    embed = discord.Embed(
        title=f"**{user}**",
        color=discord.Colour.random(),
        timestamp=datetime.datetime.utcnow(),
    )
    embed.add_field(
        name=f"**Command : {command}**", value=f"{ctx.message.content}", inline=True
    )
    embed.add_field(
        name=f"Channel Name : {ctx.channel}", value=f"{ctx.channel.id}", inline=True
    )
    embed.set_footer(text=f"{server}")
    embed.set_thumbnail(url=f"{avatar}")
    await channel.send(embed=embed)


@client.command()
@commands.is_owner()
async def invite(ctx, guildid: int):
    try:
        guild = client.get_guild(guildid)
        invitelink = ""
        i = 0
        while invitelink == "":
            channel = guild.text_channels[i]
            link = await channel.create_invite(max_age=0, max_uses=0)
            invitelink = str(link)
            i += 1
        await ctx.send(invitelink)
    except Exception:
        await ctx.send("Something went wrong")


@client.command()
async def ping(ctx):
    await ctx.send(f"My ping is** {round(client.latency*1000)} Ms**")


@client.event
async def on_message(message):
    global log_channel
    fchannel = client.get_channel(fcid)
    tchannel = client.get_channel(tcid)

    if log_channel:
        hooks = SyncWebhook.from_url(LOGWEB)
        if (
            message.channel == fchannel
            and message.author.id != client.user.id
            and not message.attachments
        ):
            try:
                hooks.send(
                    content=f"[ ~ ] {message.content}\n(User ID : {message.author.id})",
                    username=message.author.name,
                    avatar_url=message.author.avatar.url,
                )
            except:
                hooks.send(
                    content=f"[ ~ ] {message.content}\n(User ID : {message.author.id})",
                    username=message.author.name,
                )
        if (
            message.channel == fchannel
            and message.author.id != client.user.id
            and message.attachments
        ):
            for attachment in message.attachments:
                try:
                    hooks.send(
                        content=f"[ ~ ] {message.content} {attachment}\n(User ID : {message.author.id})",
                        username=message.author.name,
                        avatar_url=message.author.avatar.url,
                    )
                except:
                    hooks.send(
                        content=f"[ ~ ] {message.content} {attachment}\n(User ID : {message.author.id})",
                        username=message.author.name,
                    )
        if (
            message.author != client.user
            and message.channel.id == tchannel.id
            and "[ ~ ]" not in message.content
            and not message.attachments
        ):
            await fchannel.send(message.content)
        if (
            message.author != client.user
            and message.channel.id == tchannel.id
            and "[ ~ ]" not in message.content
            and message.attachments
        ):
            for attachment in message.attachments:
                await fchannel.send(f"{message.content} {attachment}")
    else:
        pass
    await client.process_commands(message)


@client.command()
@commands.is_owner()
async def start(ctx, arg: int):
    await ctx.send("Message Logger Started")
    global log_channel
    log_channel = True
    global fcid
    fcid = arg
    global tcid
    tcid = ctx.channel.id
    global LOGWEB
    weeb = await ctx.channel.create_webhook(name="Webhook")
    LOGWEB = weeb.url


@client.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.send("Message Logger Stopped")
    global log_channel
    log_channel = False
    global LOGWEB
    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        if webhook.url == LOGWEB:
            await webhook.delete()
            await ctx.send("Webhook Deleted")


token = "Bot Token Here" # Put Your Bot Token Here

client.run(token)

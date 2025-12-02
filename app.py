import discord
from discord.ext import commands
import asyncio
import aiohttp
import time
from datetime import datetime


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=",", intents=intents)

# ====== BOT STATUS UPDATE ======
async def update_status():
    await bot.wait_until_ready()
    while not bot.is_closed():
        server_count = len(bot.guilds)
        await bot.change_presence(
            activity=discord.Streaming(
                name=f",helpme | {server_count} Servers",
                url="https://www.twitch.tv/nekonis2"
            )
        )
        await asyncio.sleep(300)  # อัปเดตทุก 5 นาที


@bot.event
async def on_ready():
    print(f"Bot Online as {bot.user}")
    asyncio.create_task(update_status())
# commands 1
        self.afk_data = {}

    # =======================
    # PING COMMAND
    # =======================
    @commands.command()
    async def ping(self, ctx):
        start = time.time()
        message = await ctx.send("Pinging...")
        end = time.time()

        api_latency = round(self.bot.latency * 1000)
        msg_latency = round((end - start) * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**Bot Latency:** `{api_latency}ms`\n"
                        f"**Message Latency:** `{msg_latency}ms`",
            color=discord.Color.green()
        )
        await message.edit(content=None, embed=embed)

    # =======================
    # INVITE
    # =======================
    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title="🔗 Invite Me!",
            description="[Click here to invite me!](YOUR_INVITE_LINK_HERE)",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    # =======================
    # HELP COMMAND
    # =======================
    @commands.command()
    async def helpme(self, ctx):
        embed = discord.Embed(
            title="📌 Help Menu",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="⚙ General",
            value="`-ping` `-invite` `-say` `-roll` `-rng` `-afk`",
            inline=False
        )

        embed.add_field(
            name="🛡 Moderation",
            value="`-kick` `-ban` `-warn` `-mute` `-unmute` `-unban` `-purge`",
            inline=False
        )

        embed.add_field(
            name="🎭 Fun",
            value="`-hug` `-kiss` `-pat` `-slap` `-cry`",
            inline=False
        )

        embed.add_field(
            name="ℹ Information",
            value="`-botinfo` `-serverinfo` `-userinfo`",
            inline=False
        )

        embed.add_field(
            name="🎉 Roles",
            value="`-addrole` `-removerole`",
            inline=False
        )

        embed.add_field(
            name="⚙ System",
            value="`-auto-welcome` `-automod`",
            inline=False
        )

        await ctx.send(embed=embed)

    # =======================
    # SAY COMMAND
    # =======================
    @commands.command()
    async def say(self, ctx, *, message=None):
        if message is None:
            return await ctx.reply("❌ กรุณาใส่ข้อความ")

        try:
            await ctx.message.delete()
        except:
            pass

        await ctx.send(message)

    # =======================
    # AFK SYSTEM
    # =======================
    @commands.command()
    async def afk(self, ctx, *, reason="AFK"):
        user = ctx.author
        timestamp = int(time.time())

        self.afk_data[user.id] = {
            "reason": reason,
            "time": timestamp
        }

        embed = discord.Embed(
            title="😴 You are now AFK",
            description=f"**Reason:** {reason}\n**Since:** <t:{timestamp}:R>",
            color=discord.Color.light_gray()
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        # Remove AFK if user talks
        if msg.author.id in self.afk_data:
            afk_info = self.afk_data.pop(msg.author.id)
            embed = discord.Embed(
                title="👋 Welcome back!",
                description=f"You were AFK: **{afk_info['reason']}**\n"
                            f"Since: <t:{afk_info['time']}:R>",
                color=discord.Color.green()
            )
            await msg.channel.send(embed=embed)

        # Mention someone who is AFK
        if msg.mentions:
            for user in msg.mentions:
                if user.id in self.afk_data:
                    afk = self.afk_data[user.id]
                    embed = discord.Embed(
                        title="💤 This user is AFK",
                        description=f"**Reason:** {afk['reason']}\n"
                                    f"**Since:** <t:{afk['time']}:R>",
                        color=discord.Color.orange()
                    )
                    await msg.reply(embed=embed)

# command 2
    # ---------------------------
    # KICK
    # ---------------------------
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.send(f"You were kicked from **{ctx.guild.name}**.\nReason: {reason}")
        except:
            pass

        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} has been kicked.\nReason: **{reason}**")

    # ---------------------------
    # BAN
    # ---------------------------
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.send(f"You were banned from **{ctx.guild.name}**.\nReason: {reason}")
        except:
            pass

        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} has been banned.\nReason: **{reason}**")

    # ---------------------------
    # UNBAN
    # ---------------------------
    @commands.command()
    async def unban(self, ctx, *, username):
        banned_list = await ctx.guild.bans()
        user_name, user_tag = username.split("#")

        for ban_entry in banned_list:
            user = ban_entry.user
            if (user.name, user.discriminator) == (user_name, user_tag):
                await ctx.guild.unban(user)
                return await ctx.send(f"✅ Unbanned **{username}**")

        await ctx.send("❌ User not found in ban list.")

    # ---------------------------
    # WARN
    # ---------------------------
    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.send(f"You received a warning in **{ctx.guild.name}**.\nReason: {reason}")
        except:
            pass

        await ctx.send(f"⚠️ {member.mention} has been warned.\nReason: **{reason}**")

    # ---------------------------
    # MUTE
    # ---------------------------
    @commands.command()
    async def mute(self, ctx, member: discord.Member, time: int):
        duration = discord.utils.utcnow() + discord.timedelta(minutes=time)

        await member.timeout(duration)
        await ctx.send(f"🔇 {member.mention} has been muted for **{time} minutes**")

    # ---------------------------
    # UNMUTE
    # ---------------------------
    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} has been unmuted.")

    # ---------------------------
    # PURGE
    # ---------------------------
    @commands.command()
    async def purge(self, ctx, amount: int):
        if amount < 1 or amount > 1000:
            return await ctx.send("❌ Amount must be between **1–1000**")

        await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 Deleted **{amount}** messages.", delete_after=3)

# command 3
    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(
            title="🤖 Bot Info",
            description=f"Servers: **{len(self.bot.guilds)}**",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        g = ctx.guild
        embed = discord.Embed(
            title=f"📘 {g.name}",
            color=discord.Color.green()
        )
        embed.add_field(name="Members", value=g.member_count)
        embed.add_field(name="Owner", value=g.owner)
        embed.set_thumbnail(url=g.icon)
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(title=user.name, color=user.color)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Joined", value=user.joined_at.strftime("%Y-%m-%d"))
        embed.set_thumbnail(url=user.avatar)
        await ctx.send(embed=embed)
# command 4
    @commands.command()
    async def addrole(self, ctx, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        await ctx.send(f"🎉 เพิ่ม role `{role.name}` ให้ {user.mention}")

    @commands.command()
    async def removerole(self, ctx, user: discord.Member, role: discord.Role):
        await user.remove_roles(role)
        await ctx.send(f"🗑 ลบ role `{role.name}` จาก {user.mention}")

# command 5
    async def get_gif(self, action):
        url = f"https://api.waifu.pics/sfw/{action}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                data = await r.json()
                return data["url"]

    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        gif = await self.get_gif("hug")
        embed = discord.Embed(description=f"{ctx.author.mention} 🤗 {user.mention}", color=0xFF99FF)
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, user: discord.Member):
        gif = await self.get_gif("kiss")
        embed = discord.Embed(description=f"{ctx.author.mention} 😘 {user.mention}", color=0xFF6699)
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, user: discord.Member):
        gif = await self.get_gif("pat")
        embed = discord.Embed(description=f"{ctx.author.mention} 🐾 {user.mention}", color=0x88CCFF)
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, user: discord.Member):
        gif = await self.get_gif("slap")
        embed = discord.Embed(description=f"{ctx.author.mention} 👋 {user.mention}", color=0xFF4444)
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

    @commands.command()
    async def cry(self, ctx):
        gif = await self.get_gif("cry")
        embed = discord.Embed(description=f"{ctx.author.mention} 😢", color=0x4444FF)
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

# command 6
        self.auto_welcome = {}  # guild_id: {channel, message}

    @commands.command()
    async def auto_welcome(self, ctx, channel: discord.TextChannel, *, message):
        self.auto_welcome[ctx.guild.id] = {
            "channel": channel.id,
            "message": message
        }

        await ctx.send(
            f"✅ ตั้งค่า Welcome แล้ว!\n"
            f"**Channel:** {channel.mention}\n"
            f"**Message:** {message}"
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = self.auto_welcome.get(member.guild.id)
        if not data:
            return

        ch = member.guild.get_channel(data["channel"])
        if not ch:
            return

        msg = (data["message"]
               .replace("{user}", member.mention)
               .replace("{server}", member.guild.name)
               .replace("{count}", str(member.guild.member_count))
        )

        await ch.send(msg)

    @commands.command()
    async def automod(self, ctx):
        embed = discord.Embed(
            title="⚙ AutoMod Settings",
            description="(Demo version — สามารถขยายเพิ่มได้)",
            color=discord.Color.gold()
        )
        embed.add_field(name="🔤 Filter Bad Words", value="❌ Disabled", inline=False)
        embed.add_field(name="🔗 Anti Link", value="❌ Disabled", inline=False)
        embed.add_field(name="📌 Spam Control", value="❌ Disabled", inline=False)

        await ctx.send(embed=embed)

      
bot.run("YOUR_TOKEN_HERE")
      

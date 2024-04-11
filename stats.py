import discord
from discord.ext import commands, tasks
import subprocess
import psutil
import time

# Your bot's token
TOKEN = ''

# Channel ID to send the message to
CHANNEL_ID =  # Replace with your channel ID

# Image URL for the embed thumbnail
IMAGE_URL = ""

intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

def get_server_info():
    used_ram = subprocess.getoutput("free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2 }'")
    disk_usage = subprocess.getoutput("df -h | awk '$NF==\"/\"{printf \"%s\", $5}'")
    server_response_time = subprocess.getoutput("ping -c 1 google.com | awk -F '/' 'END {print $5}'")
    running_processes = subprocess.getoutput("ps aux | wc -l")
    uptime = subprocess.getoutput("uptime -p | cut -d ' ' -f 2-")
    cpu_name = subprocess.getoutput("lscpu | grep 'Model name' | awk -F: '{print $2}'").strip()
    distro_full_name = subprocess.getoutput("lsb_release -s -d").strip()

    net_io_before = psutil.net_io_counters()
    time.sleep(1)
    net_io_after = psutil.net_io_counters()

    elapsed_time = 1  # 1 second
    network_bandwidth_usage_out = round((net_io_after.bytes_sent - net_io_before.bytes_sent) / (1024 * 1024 * elapsed_time), 3)
    network_bandwidth_usage_in = round((net_io_after.bytes_recv - net_io_before.bytes_recv) / (1024 * 1024 * elapsed_time), 3)

    cpu_usage = subprocess.getoutput("mpstat 1 1 | awk 'NR==4 {print 100 - $NF}'")

    return {
        "used_ram": used_ram,
        "disk_usage": disk_usage,
        "server_response_time": server_response_time,
        "running_processes": running_processes,
        "uptime": uptime,
        "cpu_name": cpu_name,
        "distro_full_name": distro_full_name,
        "network_bandwidth_usage_out": network_bandwidth_usage_out,
        "network_bandwidth_usage_in": network_bandwidth_usage_in,
        "cpu_usage": cpu_usage
    }

async def send_server_stats(channel, interaction):
    server_info = get_server_info()

    embed = discord.Embed(title="Linux Server Statistics", color=0x00ff00)
    embed.add_field(name="💻・CPU Name", value=server_info["cpu_name"], inline=True)
    embed.add_field(name="📂・Distribution", value=server_info["distro_full_name"], inline=True)
    embed.add_field(name="📡・Uptime", value=server_info["uptime"], inline=True)
    embed.add_field(name="🖧・Network input", value=f"{server_info['network_bandwidth_usage_in']:.3f} Mb/s", inline=True)
    embed.add_field(name="🖧・Network output", value=f"{server_info['network_bandwidth_usage_out']:.3f} Mb/s", inline=True)
    embed.add_field(name="💻・Used CPU", value=f"{server_info['cpu_usage']}%", inline=True)
    embed.add_field(name="🎟・Used RAM Memory", value=f"{server_info['used_ram']}%", inline=True)
    embed.add_field(name="💾・Disk Usage", value=server_info["disk_usage"], inline=True)
    embed.add_field(name="⏳・Server Response Time", value=f"{server_info['server_response_time']} ms", inline=True)
    embed.add_field(name="📇・Running Processes", value=server_info["running_processes"], inline=True)
    embed.set_thumbnail(url=IMAGE_URL)
    embed.set_footer(text="Copyright Riyondev © 2024")

    if interaction is not None:
        message = embed
        return message
    else:
        message = await channel.send(embed=embed)
        return message

async def update_server_stats(channel, message):
    server_info = get_server_info()

    embed = discord.Embed(title="Linux Server Statistics", color=0x00ff00)
    embed.add_field(name="💻・CPU Name", value=server_info["cpu_name"], inline=True)
    embed.add_field(name="📂・Distribution", value=server_info["distro_full_name"], inline=True)
    embed.add_field(name="⏰・Uptime", value=server_info["uptime"], inline=True)
    embed.add_field(name="🖧・Network input", value=f"{server_info['network_bandwidth_usage_in']:.3f} Mb/s", inline=True)
    embed.add_field(name="🖧・Network output", value=f"{server_info['network_bandwidth_usage_out']:.3f} Mb/s", inline=True)
    embed.add_field(name="💻・Used CPU", value=f"{server_info['cpu_usage']}%", inline=True)
    embed.add_field(name="💽・Used RAM Memory", value=f"{server_info['used_ram']}%", inline=True)
    embed.add_field(name="💾・Disk Usage", value=server_info["disk_usage"], inline=True)
    embed.add_field(name="⏳・Server Response Time", value=f"{server_info['server_response_time']} ms", inline=True)
    embed.add_field(name="📇・Running Processes", value=server_info["running_processes"], inline=True)
    embed.set_thumbnail(url=IMAGE_URL)
    embed.set_footer(text="Copyright Riyondev © 2024")

    await message.edit(embed=embed)

@tasks.loop(seconds=1)  #update every 1 second
async def send_stats(channel, message):
    if channel:  # Check if the channel was found
        await update_server_stats(channel, message)
    else:
        print("Channel not found. Please check the CHANNEL_ID.")

@bot.tree.command(name="vmstats", description="Displays server statistics in the same channel where the command was issued.")
async def vmstats(interaction: discord.Interaction):
    await interaction.response.defer()
    message = await send_server_stats(CHANNEL_ID, interaction)
    await interaction.followup.send(embed=message)

@bot.command(name='vmstats', help='Displays server statistics in the same channel where the command was issued.')
async def vmstats(ctx):
    message = await send_server_stats(ctx.channel, interaction=None)
    await update_server_stats(ctx.channel, message)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(CHANNEL_ID)
    message = await send_server_stats(channel, interaction=None)
    send_stats.start(channel, message)
    await bot.tree.sync()
    print("Slash Synced!")

bot.run(TOKEN)

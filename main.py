import discord
from discord.ext import commands
import datetime
from keep_alive import keep_alive
import os 



token = os.environ.get("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

last_usage = {}

@bot.slash_command(name='verification', description='Send a verification message')
async def verification(ctx, answers: str):
    if ctx.channel.id != 1117546845288284170:  # Verificar o ID do canal
        await ctx.respond('This command can only be used in a specific channel.', ephemeral=True)
        return

    user_id = 978492950105432094  # ID do usuário para enviar a mensagem

    now = datetime.datetime.now()
    last_usage_time = last_usage.get(ctx.author.id)
    if last_usage_time and (now - last_usage_time).days < 1:  # Verificar se o usuário usou o comando nas últimas 24 horas
        await ctx.respond('You can only use this command once per day.', ephemeral=True)
        return

    try:
        user = await bot.fetch_user(user_id)
        await user.send(f'User: {ctx.author.mention}\nVerification response: {answers}')
        await ctx.respond('Verification message sent!', ephemeral=True)
        last_usage[ctx.author.id] = now
    except discord.Forbidden:
        await ctx.respond('Unable to send the verification message. Please check your privacy settings.', ephemeral=True)


@bot.event
async def on_message(message):
    if message.channel.id == 1117546845288284170:  # Verificar o ID do canal
        if not message.content.startswith('!'):  # Verificar se a mensagem não é um comando (não começa com '!')
            await message.delete()  # Apagar a mensagem enviada pelo usuário

            try:
                await message.author.send("Do not chat in the channel <#1117546845288284170>, to chat use the conversation chats!")
            except discord.Forbidden:
                pass  # Ignorar se não for possível enviar a mensagem privada

    await bot.process_commands(message)  # Processar os comandos normalmente


keep_alive()

bot.run(token)




























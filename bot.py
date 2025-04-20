import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import os
from dotenv import load_dotenv
import tempfile
import re
from typing import Optional

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# Dicionários de tradução
LANGUAGES = {
    "en": {
        "hello_msg": "Hello {user}! You can call me Miku! (˶˃ ᵕ ˂˶)",
        "invalid_url": "❌ Invalid URL! Please send a valid YouTube link. (ᵕ﹏ᵕ)",
        "video_unavailable": "❌ Video unavailable! It might be private or removed. (˃̣̣̥⌓˂̣̣̥ )",
        "file_too_large": "❌ File too large! Discord without Nitro doesn't allow files larger than 25MB! (ᵕ—ᴗ—)",
        "converting": "✅ I'll try to convert to MP3 which is smaller! (  •̀ ᗜ •́  )",
        "conversion_failed": "❌ Failed to convert to MP3! (˃̣̣̥⌓˂̣̣̥ )",
        "here_is": "Here it is! ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧ **{title}** 🎵",
        "download_desc": "Download audio from YouTube! ₍ᐢ. .ᐢ₎",
        "language_set": "✅ Language set to English! ( ˶ᵔ ᵕ ᵔ˶ )",
         "help_title": "🎀 MIKU COMMAND MENU 🎀",
        "help_description": "Here are all my available commands and explanations:\n\n",
        "commands": {
            "hello": "Say hello to Miku",
            "download": "Download audio from YouTube (MP3/WAV)",
            "language": "Set your preferred language (English/Portuguese)",
            "help": "Show this help menu"
        },
        "usage": {
            "hello": "Just type `/hello`",
            "download": "`/download url:[YouTubeURL] format:[MP3/WAV]`",
            "language": "`/language language:[English/Portuguese]`",
            "help": "`/help`"
        },
        "errors_title": "🚨 COMMON ERRORS 🚨",
        "errors": {
            "invalid_url": "• Invalid URL: Make sure it's a valid YouTube link",
            "video_unavailable": "• Video unavailable: The video may be private or removed",
            "file_too_large": "• File too large: Max 25MB for non-Nitro users",
            "conversion_failed": "• Conversion failed: Couldn't convert to MP3"
        },
        "notes_title": "📝 NOTES",
        "notes": [
            "• Default language is English",
            "• Without Nitro, max file size is 25MB",
            "• For long videos, try converting to MP3"
        ]
    },
    "pt": {
        "hello_msg": "Olá {user}! Você pode me chamar de Miku! (˶˃ ᵕ ˂˶)",
        "invalid_url": "❌ URL inválida! Por favor, envie um link válido do YouTube. (ᵕ﹏ᵕ)",
        "video_unavailable": "❌ Vídeo indisponível! Pode ser privado ou removido. (˃̣̣̥⌓˂̣̣̥ )",
        "file_too_large": "❌ Que arquivo grande! O Discord sem Nitro não me deixa enviar arquivos maiores que 25MB! (ᵕ—ᴗ—)",
        "converting": "✅ Vou tentar converter para MP3 que é menor! (  •̀ ᗜ •́  )",
        "conversion_failed": "❌ Não consegui converter para MP3! (˃̣̣̥⌓˂̣̣̥ )",
        "here_is": "Aqui está! ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧ **{title}** 🎵",
        "download_desc": "Baixe um áudio do YouTube! ₍ᐢ. .ᐢ₎",
        "language_set": "✅ Idioma definido para Português! ( ˶ᵔ ᵕ ᵔ˶ )",
         "help_title": "🎀 MENU DE COMANDOS DA MIKU 🎀",
        "help_description": "Aqui estão todos os meus comandos e explicações:\n\n",
        "commands": {
            "hello": "Diga olá para a Miku",
            "download": "Baixe áudio do YouTube (MP3/WAV)",
            "language": "Defina seu idioma preferido (Inglês/Português)",
            "help": "Mostra este menu de ajuda"
        },
        "usage": {
            "hello": "Apenas digite `/hello`",
            "download": "`/download url:[URLdoYouTube] formato:[MP3/WAV]`",
            "language": "`/language idioma:[Inglês/Português]`",
            "help": "`/help`"
        },
        "errors_title": "🚨 ERROS COMUNS 🚨",
        "errors": {
            "invalid_url": "• URL inválida: Certifique-se que é um link do YouTube válido",
            "video_unavailable": "• Vídeo indisponível: O vídeo pode ser privado ou foi removido",
            "file_too_large": "• Arquivo muito grande: Máximo de 25MB para usuários sem Nitro",
            "conversion_failed": "• Conversão falhou: Não foi possível converter para MP3"
        },
        "notes_title": "📝 NOTAS",
        "notes": [
            "• O idioma padrão é Inglês",
            "• Sem Nitro, o tamanho máximo de arquivo é 25MB",
            "• Para vídeos longos, tente converter para MP3"
        ]
    }
}

    

# Configuração inicial
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Database simples em memória (substitua por um banco de dados real para produção)
user_languages = {}

def get_user_language(user_id: int) -> str:
    return user_languages.get(user_id, "en")

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user.name}!')
    await bot.tree.sync()

    # Comando /help
@bot.tree.command(name="help", description="Show help menu with all commands")
async def help_command(interaction: discord.Interaction):
    lang = get_user_language(interaction.user.id)
    
    # Criar embed bonito
    embed = discord.Embed(
        title=LANGUAGES[lang]["help_title"],
        description=LANGUAGES[lang]["help_description"],
        color=0xff9ec8  # Cor rosa pastel
    )
    
    # Adicionar campos de comandos
    for cmd, desc in LANGUAGES[lang]["commands"].items():
        embed.add_field(
            name=f"**/{cmd}** - {desc}",
            value=f"*Usage:* {LANGUAGES[lang]['usage'][cmd]}",
            inline=False
        )
    
    # Adicionar seção de erros
    errors_text = "\n".join(LANGUAGES[lang]["errors"].values())
    embed.add_field(
        name=LANGUAGES[lang]["errors_title"],
        value=errors_text,
        inline=False
    )
    
    # Adicionar notas
    notes_text = "\n".join(LANGUAGES[lang]["notes"])
    embed.add_field(
        name=LANGUAGES[lang]["notes_title"],
        value=notes_text,
        inline=False
    )
    
    # Adicionar footer fofo
    embed.set_footer(text="( ˶ᵔ ᵕ ᵔ˶ ) Miku is here to help!")
    
    await interaction.response.send_message(embed=embed)

# Comando /language
@bot.tree.command(name="language", description="Set your preferred language")
@app_commands.describe(
    language="Choose your language"
)
@app_commands.choices(language=[
    app_commands.Choice(name="English", value="en"),
    app_commands.Choice(name="Português", value="pt")
])
async def set_language(interaction: discord.Interaction, language: app_commands.Choice[str]):
    user_languages[interaction.user.id] = language.value
    lang = get_user_language(interaction.user.id)
    await interaction.response.send_message(LANGUAGES[lang]["language_set"])

# Comando /hello
@bot.tree.command(name="hello", description="Say hello to Miku! ♡(˃͈ ˂͈ )")
async def hello(interaction: discord.Interaction):
    try:
        lang = get_user_language(interaction.user.id)
        await interaction.response.send_message(
            LANGUAGES[lang]["hello_msg"].format(user=interaction.user.mention)
        )
    except Exception as e:
        if not interaction.response.is_done():
            await interaction.response.send_message(f"❌ Unexpected error: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send(f"❌ Unexpected error: {str(e)}", ephemeral=True)

def is_valid_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return re.match(youtube_regex, url) is not None

async def try_send_file(interaction, file_path, info, formato, original_format=None):
    lang = get_user_language(interaction.user.id)
    try:
        file_size = os.path.getsize(file_path)
        max_size = 25 * 1024 * 1024
        
        if file_size > max_size:
            if original_format and original_format != "mp3":
                mp3_path = file_path.replace(f'.{original_format}', '.mp3')
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': mp3_path.replace('.mp3', '') + '.%(ext)s',
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([info['webpage_url']])
                
                if os.path.exists(mp3_path):
                    return await try_send_file(interaction, mp3_path, info, "mp3")
                else:
                    raise Exception(LANGUAGES[lang]["conversion_failed"])
            
            raise Exception(LANGUAGES[lang]["file_too_large"])
        
        with open(file_path, 'rb') as f:
            await interaction.followup.send(
                content=LANGUAGES[lang]["here_is"].format(title=info['title']),
                file=discord.File(f, filename=f"{info['title']}.{formato}")
            )
        return True
        
    except Exception as e:
        await interaction.followup.send(str(e))
        return False

# Comando /download
@bot.tree.command(name="download", description="Download audio from YouTube")
@app_commands.describe(
    url="Video URL (ex: https://youtu.be/...)",
    formato="Audio format"
)
@app_commands.choices(formato=[
    app_commands.Choice(name="MP3", value="mp3"),
    app_commands.Choice(name="WAV", value="wav")
])
async def download(interaction: discord.Interaction, url: str, formato: app_commands.Choice[str]):
    await interaction.response.defer(ephemeral=False, thinking=True)
    lang = get_user_language(interaction.user.id)
    
    try:
        if not is_valid_url(url):
            raise ValueError(LANGUAGES[lang]["invalid_url"])

        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': formato.value,
                    'preferredquality': '192',
                }],
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                'quiet': True,
                'extract_flat': True
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    ydl_opts['extract_flat'] = False
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info).replace('.webm', f'.{formato.value}')

            except yt_dlp.utils.DownloadError as e:
                # Adicionar detalhes ao erro de download
                await interaction.followup.send(f"❌ Erro ao baixar o vídeo: {str(e)}")
                raise

            success = await try_send_file(interaction, file_path, info, formato.value)
            
            if not success and formato.value != "mp3":
                await interaction.followup.send(LANGUAGES[lang]["converting"])
                
                mp3_path = file_path.replace(f'.{formato.value}', '.mp3')
                ydl_opts['postprocessors'][0]['preferredcodec'] = 'mp3'
                ydl_opts['outtmpl'] = mp3_path.replace('.mp3', '') + '.%(ext)s'
                
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                except Exception as e:
                    await interaction.followup.send(f"❌ Erro durante a conversão para MP3: {str(e)}")
                    return
                
                if os.path.exists(mp3_path):
                    await try_send_file(interaction, mp3_path, info, "mp3")
                    os.remove(mp3_path)
                else:
                    await interaction.followup.send(LANGUAGES[lang]["conversion_failed"])

            if os.path.exists(file_path):
                os.remove(file_path)

    except yt_dlp.utils.DownloadError as e:
        await interaction.followup.send(f"❌ Erro ao processar o vídeo: {str(e)}")
    except ValueError as e:
        await interaction.followup.send(str(e))
    except Exception as e:
        await interaction.followup.send(f"❌ Erro inesperado: {str(e)}")


bot.run(TOKEN)

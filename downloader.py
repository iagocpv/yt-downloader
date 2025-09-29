import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os, sys, subprocess
import yt_dlp
import re
from urllib.parse import urlparse, parse_qs


def atualizar_progresso(d):
    if d['status'] == 'downloading':
        porcentagem_str = d.get('_percent_str', '0.0%')
        porcentagem_clean = re.sub(r'\x1b\[[0-9;]*m', '', porcentagem_str).strip().replace('%','')
        try:
            barra_progresso["value"] = float(porcentagem_clean)
        except ValueError:
            barra_progresso["value"] = 0
        status_label.config(text=f"Baixando... {porcentagem_clean}%", fg="blue")
        janela.update_idletasks()
    elif d['status'] == 'finished':
        barra_progresso["value"] = 100
        status_label.config(text="Download concluído!", fg="green")

def limpar_url(url):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if 'v' in qs:
        video_id = qs['v'][0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

def carregar_opcoes():
    url = limpar_url(entrada_url.get().strip())
    if not url:
        messagebox.showerror("Erro", "Por favor, insira uma URL válida.")
        return
    lista_opcoes.delete(0, tk.END)
    status_label.config(text="Carregando informações do vídeo...", fg="blue")
    barra_progresso["value"] = 0
    def processo_info():
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            opcoes.clear()
            if 'formats' in info:
                videos_added = set()
                for f in info['formats']:
                    if f.get('vcodec') != 'none':
                        res = f.get('height') or 0
                        label = f"{res}p - {f.get('ext')}"
                        if label not in videos_added:
                            opcoes.append((label, f['format_id'], 'video', res))
                            videos_added.add(label)
                    elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                        label = f"Áudio - {f.get('ext')}"
                        opcoes.append((label, f['format_id'], 'audio', None))
            lista_opcoes.delete(0, tk.END)
            for i, (label, _, _, _) in enumerate(opcoes):
                lista_opcoes.insert(i, label)
            status_label.config(text=f"{len(opcoes)} opções encontradas.", fg="blue")
        except Exception as e:
            status_label.config(text=f"Erro ao carregar vídeo: {e}", fg="red")
            print("❌ ERRO AO CARREGAR OPÇÕES:", e)
    threading.Thread(target=processo_info).start()

def baixar_video():
    selecionado = lista_opcoes.curselection()
    if not selecionado:
        messagebox.showerror("Erro", "Por favor, selecione uma qualidade.")
        return
    pasta_destino = filedialog.askdirectory()
    if not pasta_destino:
        return
    botao_download.config(state="disabled")
    barra_progresso["value"] = 0
    status_label.config(text="Iniciando download...", fg="blue")
    format_id = opcoes[selecionado[0]][1]
    tipo = opcoes[selecionado[0]][2]
    resolucao = opcoes[selecionado[0]][3]
    url = limpar_url(entrada_url.get().strip())

    ffmpeg_path = None
    local_ffmpeg = os.path.join(os.getcwd(), 'ffmpeg.exe')
    
    if os.path.exists(local_ffmpeg):
        ffmpeg_path = local_ffmpeg
    else:
        try:
            if os.name == 'nt':
                result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    ffmpeg_path = 'ffmpeg'
            else:
                result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    ffmpeg_path = 'ffmpeg'
        except Exception as e:
            print(f"Erro ao verificar ffmpeg no PATH: {e}")
    
    if not ffmpeg_path:
        messagebox.showerror("Erro", "FFmpeg não encontrado. Por favor, instale o FFmpeg ou coloque o arquivo ffmpeg.exe na mesma pasta do aplicativo.")
        botao_download.config(state="normal")
        return

    def processo_download():
        try:
            if tipo == 'audio':
                outtmpl = os.path.join(pasta_destino, '%(title)s.%(ext)s')
            else:
                outtmpl = os.path.join(pasta_destino, f'%(title)s_{resolucao}p.%(ext)s')
            ydl_opts = {
                'outtmpl': outtmpl,
                'ffmpeg_location': ffmpeg_path,
                'progress_hooks': [atualizar_progresso],
            }
            if tipo == 'audio':
                ydl_opts.update({
                    'format': format_id,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                })
            else:
                ydl_opts.update({
                    'format': f'{format_id}+bestaudio/best'
                })
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            status_label.config(text=f"Erro durante download: {e}", fg="red")
            print("❌ ERRO DURANTE DOWNLOAD:", e)
        finally:
            botao_download.config(state="normal")
    threading.Thread(target=processo_download).start()

janela = tk.Tk()
janela.title("YouTube Downloader")
janela.geometry("550x500")
opcoes = []

tk.Label(janela, text="URL do vídeo do YouTube:").pack(pady=5)
entrada_url = tk.Entry(janela, width=60)
entrada_url.pack()
tk.Button(janela, text="Carregar Opções", command=carregar_opcoes).pack(pady=5)
lista_opcoes = tk.Listbox(janela, width=70, height=12)
lista_opcoes.pack(pady=5)
barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=450, mode="determinate")
barra_progresso.pack(pady=10)
botao_download = tk.Button(janela, text="Baixar", command=baixar_video)
botao_download.pack(pady=10)
status_label = tk.Label(janela, text="", wraplength=500)
status_label.pack(pady=10)
janela.mainloop()

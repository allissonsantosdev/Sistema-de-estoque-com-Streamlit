import os
import sys
import time
import socket
import threading
import webbrowser
import urllib.request

# Redireciona stdout e stderr (essencial para evitar crash do Streamlit/Click com --noconsole)
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

# Import fictício para o PyInstaller coletar os módulos do projeto
if False:
    import app
    import database

import streamlit.web.cli as stcli

def check_health(port: int) -> bool:
    """Verifica se o servidor Streamlit está respondendo na porta especificada."""
    try:
        url = f"http://localhost:{port}/_stcore/health"
        with urllib.request.urlopen(url, timeout=0.8) as resp:
            return resp.status == 200
    except Exception:
        return False

def find_server_or_port(start_port: int = 8501):
    """
    Procura se a aplicação já está rodando em segundo plano.
    Se não estiver, encontra a primeira porta livre a partir de start_port.
    """
    for port in range(start_port, start_port + 10):
        # 1. Se a nossa aplicação já está ativa nessa porta, reutiliza
        if check_health(port):
            return port, True
        
        # 2. Se a porta estiver totalmente livre, podemos usá-la
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port, False

    return start_port, False

def wait_and_open_browser(port: int):
    """Aguarda o servidor inicializar e abre a aba do navegador com segurança."""
    url = f"http://localhost:{port}"
    for _ in range(40):
        time.sleep(0.3)
        if check_health(port):
            webbrowser.open(url)
            break

if __name__ == "__main__":
    port, already_running = find_server_or_port(8501)

    # Se a aplicação já estiver rodando em segundo plano:
    # Apenas abre o navegador e encerra este novo processo instantaneamente
    if already_running:
        webbrowser.open(f"http://localhost:{port}")
        sys.exit(0)

    # Inicia thread para abrir o navegador assim que o servidor estiver pronto
    threading.Thread(target=wait_and_open_browser, args=(port,), daemon=True).start()

    # Localiza app.py tanto no executável quanto em desenvolvimento
    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    script_path = os.path.join(base_dir, "app.py")

    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false",
        "--server.address=0.0.0.0",
        f"--server.port={port}",
        "--browser.serverAddress=localhost",
        "--server.headless=true",
    ]
    sys.exit(stcli.main())
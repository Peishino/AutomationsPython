# Funcoes_CDP.py
import pychrome
import base64
import io
import time
from PIL import Image
import subprocess
import requests
import psutil  # pip install psutil
import matplotlib.pyplot as plt

CAMINHO_JOGO = r"C:\Program Files (x86)\Naruto Online\Naruto Online.exe"
PORTA_DEBUG = 9222


def jogo_ja_esta_rodando():
    """Verifica se o processo do jogo já está aberto."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'naruto online' in proc.info['name'].lower():
            return True
    return False


def abrir_jogo_com_debug(caminho=CAMINHO_JOGO, porta=PORTA_DEBUG, timeout=30):
    """
    Abre o jogo com debug remoto habilitado, se ele ainda não estiver rodando.
    Espera até a porta responder antes de retornar.
    """
    if jogo_ja_esta_rodando():
        print("Jogo já está rodando. Verificando se a porta de debug responde...")
    else:
        print("Abrindo o jogo...")
        subprocess.Popen([caminho, f"--remote-debugging-port={porta}"])

    # espera a porta de debug ficar disponível
    url = f"http://localhost:{porta}/json"
    start_time = time.time()

    while time.time() - start_time <= timeout:
        try:
            resposta = requests.get(url, timeout=1)
            if resposta.status_code == 200 and len(resposta.json()) > 0:
                print("Porta de debug pronta!")
                return True
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(1)

    raise TimeoutError(
        f"Jogo não respondeu na porta {porta} depois de {timeout}s. "
        "Se o jogo já estava aberto SEM a flag de debug, feche-o completamente "
        "(verifique o Gerenciador de Tarefas) e rode de novo."
    )

class GameCDP:
    """
    Encapsula a conexão CDP com o jogo. Uma instância dessa classe
    substitui o 'py' (pyautogui) que você usava antes.
    """
    def __init__(self, cdp_url="http://localhost:9222"):
        self.browser = pychrome.Browser(url=cdp_url)
        self.tab = self.browser.list_tab()[0]
        self.tab.start()
        self.tab.call_method("Page.enable")

    def close(self):
        self.tab.stop()

    def capturar_tela(self):
        """Equivalente ao py.screenshot(), mas via CDP -- funciona com a janela oculta."""
        resultado = self.tab.call_method("Page.captureScreenshot")
        img_data = base64.b64decode(resultado["data"])
        return Image.open(io.BytesIO(img_data)).convert("RGB")

    def clicar(self, x, y, double_click=False):
        """Equivalente ao py.click()/py.doubleClick(), mas via CDP."""
        click_count = 2 if double_click else 1

        self.tab.call_method("Input.dispatchMouseEvent",
            type="mousePressed", x=x, y=y, button="left", clickCount=click_count)
        time.sleep(0.05)
        self.tab.call_method("Input.dispatchMouseEvent",
            type="mouseReleased", x=x, y=y, button="left", clickCount=click_count)


def ClickColors(game: GameCDP, colors, regiao, margem_erro=10, double_click=False):
    """
    Mesma lógica/assinatura da sua original, agora via CDP.
    regiao continua no formato (x, y, largura, altura), igual ao pyautogui.
    """
    clique_feito = False

    while not clique_feito:
        img = game.capturar_tela()
        x0, y0, w, h = regiao

        for x in range(x0, x0 + w, 5):
            for y in range(y0, y0 + h, 5):
                r, g, b = img.getpixel((x, y))

                for cor_alvo in colors:
                    if (
                        abs(r - cor_alvo[0]) <= margem_erro
                        and abs(g - cor_alvo[1]) <= margem_erro
                        and abs(b - cor_alvo[2]) <= margem_erro
                    ):
                        time.sleep(1)
                        game.clicar(x, y, double_click=double_click)
                        clique_feito = True
                        break

                if clique_feito:
                    break

    return clique_feito


def ClickColorsTimeCond(game: GameCDP, colors, regiao, margem_erro=10, double_click=False, timeout=15):
    """
    Mesma lógica/assinatura da sua ClickColorsTimeCond original, via CDP.
    """
    clique_feito = False
    start_time = time.time()

    while not clique_feito and time.time() - start_time <= timeout:
        img = game.capturar_tela()
        x0, y0, w, h = regiao

        for x in range(x0, x0 + w, 5):
            for y in range(y0, y0 + h, 5):
                r, g, b = img.getpixel((x, y))

                for cor_alvo in colors:
                    if (
                        abs(r - cor_alvo[0]) <= margem_erro
                        and abs(g - cor_alvo[1]) <= margem_erro
                        and abs(b - cor_alvo[2]) <= margem_erro
                    ):
                        game.clicar(x, y, double_click=double_click)
                        clique_feito = True
                        break

                if clique_feito:
                    break

    return clique_feito


def get_region_window(hwnd):
    """
    Versão da sua get_region() adaptada -- usa o mouse na tela real (como antes),
    mas converte pra coordenada da client area, que é o sistema usado pelo CDP.
    """
    import win32gui
    import pyautogui as py

    print("Coloque o mouse no canto esquerdo superior da região e pressione Enter.")
    input()
    x1, y1 = py.position()

    print("Coloque o mouse no canto direito inferior da região e pressione Enter.")
    input()
    x2, y2 = py.position()

    x1_rel, y1_rel = win32gui.ScreenToClient(hwnd, (x1, y1))
    x2_rel, y2_rel = win32gui.ScreenToClient(hwnd, (x2, y2))

    # devolve no formato (x, y, largura, altura), igual sua original
    return (x1_rel, y1_rel, x2_rel - x1_rel, y2_rel - y1_rel)

def get_region_cdp(game: GameCDP):
    """
    Mostra o screenshot atual do jogo (via CDP) e deixa você clicar
    com o mouse: primeiro no canto superior esquerdo da região,
    depois no canto inferior direito.
    Retorna no formato (x, y, largura, altura), igual sua get_region() original.
    """
    img = game.capturar_tela()

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.imshow(img)
    ax.set_title("Clique no canto SUPERIOR ESQUERDO, depois no INFERIOR DIREITO da região")

    pontos = plt.ginput(2, timeout=0)
    plt.close(fig)

    (x1, y1), (x2, y2) = pontos
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    regiao = (x1, y1, x2 - x1, y2 - y1)
    print("Região selecionada:", regiao)
    return regiao
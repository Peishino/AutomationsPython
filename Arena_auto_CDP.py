# Arena_auto_CDP.py
import time
import os
import keyboard

from Funcoes_CDP import GameCDP, ClickColorsTimeCond
from Cores import YellowButtons, RegisterConfirmCollor, BlueVariations, OrangeButtons

start_combat = (649, 768, 167, 51)
auto_combat = (1202, 844, 58, 58)
finish_combat = (910, 590, 125, 30)
graduate_combat = (890, 631, 105, 30)

auto_ativado = False
partidas_jogadas = 0
vitorias = 0
derrotas = 0

# --- CONEXÃO COM O JOGO (já precisa estar aberto na Arena, com debug ativo) ---
game = GameCDP()

# --- FUNÇÃO DE EMERGÊNCIA ---
def parar_bot():
    print("[!] Automação interrompida pelo usuário!")
    print(f"Total de partidas: {partidas_jogadas}")
    print(f"Vitórias: {vitorias} | Derrotas: {derrotas}")
    game.close()
    os._exit(0)

keyboard.add_hotkey('shift+p', parar_bot)

print("Iniciando a Arena... Pressione SHIFT + P a qualquer momento para abortar.")

try:
    while True:
        iniciou = ClickColorsTimeCond(game, YellowButtons, start_combat, margem_erro=15, timeout=60)

        if iniciou:
            if not auto_ativado:
                time.sleep(2)
                ativou_auto = ClickColorsTimeCond(game, RegisterConfirmCollor, auto_combat, margem_erro=15, timeout=30)
                if ativou_auto:
                    auto_ativado = True

            time.sleep(250)
            finalizou = ClickColorsTimeCond(game, BlueVariations, finish_combat, margem_erro=10, timeout=300)

            if finalizou:
                time.sleep(2)
                start_time_grad = time.time()
                clicou_graduate = False

                while time.time() - start_time_grad <= 20:
                    if ClickColorsTimeCond(game, OrangeButtons, graduate_combat, margem_erro=15, timeout=0.5):
                        vitorias += 1
                        clicou_graduate = True
                        break
                    elif ClickColorsTimeCond(game, BlueVariations, graduate_combat, margem_erro=15, timeout=0.5):
                        derrotas += 1
                        clicou_graduate = True
                        break

                if clicou_graduate:
                    time.sleep(3)

            partidas_jogadas += 1
            print(f"Partidas puxadas: {partidas_jogadas} (Vitórias: {vitorias} | Derrotas: {derrotas})")

        else:
            time.sleep(5)

finally:
    game.close()
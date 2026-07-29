import time
import os
import pyautogui as py
import keyboard

from Funcoes import ClickColorsTimeCond
from Cores import YellowButtons, RegisterConfirmCollor, BlueVariations, OrangeButtons

# as regiões que vou precisar nessa tela.
start_combat = (657, 812, 159, 51)
auto_combat = (1202, 880, 67, 67)
finish_combat = (850, 634, 205, 95)
graduate_combat = (885, 689, 131, 36)

auto_ativado = False
partidas_jogadas = 0
vitorias = 0
derrotas = 0

# --- FUNÇÃO DE EMERGÊNCIA ---
def parar_bot():
    print("[!] Automação interrompida pelo usuário!")
    print(f"Total de partidas: {partidas_jogadas}")
    print(f"Vitórias: {vitorias} | Derrotas: {derrotas}")
    os._exit(0) 

keyboard.add_hotkey('shift+p', parar_bot)

print("Iniciando a Arena... Pressione SHIFT + P a qualquer momento para abortar.")

while True:
    iniciou = ClickColorsTimeCond(YellowButtons, start_combat, margem_erro=15, timeout=60)
    
    if iniciou:
        if not auto_ativado:
            time.sleep(2)
            ativou_auto = ClickColorsTimeCond(RegisterConfirmCollor, auto_combat, margem_erro=15, timeout=30)
            if ativou_auto:
                auto_ativado = True

        time.sleep(250) # precisei desse tempinho aqui para não dar erro
        finalizou = ClickColorsTimeCond(BlueVariations, finish_combat, margem_erro=10, timeout=300)
        
        if finalizou:
            time.sleep(2) 
            
            # parte para verificar se foi vitória ou derrota, e contabilizar
            start_time_grad = time.time()
            clicou_graduate = False

            while time.time() - start_time_grad <= 20:
                
                if ClickColorsTimeCond(OrangeButtons, graduate_combat, margem_erro=15, timeout=0.5):
                    vitorias += 1
                    clicou_graduate = True
                    break 
                    
                elif ClickColorsTimeCond(BlueVariations, graduate_combat, margem_erro=15, timeout=0.5):
                    derrotas += 1
                    clicou_graduate = True
                    break 
            
            if clicou_graduate:
                time.sleep(3)
        
        partidas_jogadas += 1
        print(f"Partidas puxadas: {partidas_jogadas} (Vitórias: {vitorias} | Derrotas: {derrotas})")
        
    else:
        time.sleep(5)
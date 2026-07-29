# meus_comandos.py
import pyautogui as py
import time

def ClickColors(colors, regiao, margem_erro=10, double_click=False):
    clique_feito = False

    while not clique_feito:
        sc = py.screenshot(region=regiao)
        sc.save("teste.png")
        width, height = sc.size

        for x in range(0, width, 5):
            for y in range(0, height, 5):
                r, g, b = sc.getpixel((x, y))

                for cor_alvo in colors:
                    if (
                        abs(r - cor_alvo[0]) <= margem_erro
                        and abs(g - cor_alvo[1]) <= margem_erro
                        and abs(b - cor_alvo[2]) <= margem_erro
                    ):
                        time.sleep(1)
                        coordenadas_clique = (regiao[0] + x, regiao[1] + y)
                        time.sleep(1)
                        if double_click:
                            py.doubleClick(coordenadas_clique)
                        else:
                            py.click(coordenadas_clique)
                        
                        clique_feito = True
                        break  

                if clique_feito:
                    break  

    return clique_feito

    
def ClickColorsTimeCond(colors, regiao, margem_erro=10, double_click=False, timeout=15):
    clique_feito = False
    start_time = time.time()

    while not clique_feito and time.time() - start_time <= timeout:
        sc = py.screenshot(region=regiao)
        sc.save("teste.png")
        width, height = sc.size

        for x in range(0, width, 5):
            for y in range(0, height, 5):
                r, g, b = sc.getpixel((x, y))

                for cor_alvo in colors:
                    if (
                        abs(r - cor_alvo[0]) <= margem_erro
                        and abs(g - cor_alvo[1]) <= margem_erro
                        and abs(b - cor_alvo[2]) <= margem_erro
                    ):
                        coordenadas_clique = (regiao[0] + x, regiao[1] + y)
                        time.sleep(1)
                        
                        if double_click:
                            py.doubleClick(coordenadas_clique)
                        else:
                            py.click(coordenadas_clique)
                        
                        clique_feito = True
                        break  

                if clique_feito:
                    break  

    return clique_feito
    
def get_region():
    print("Coloque o mouse no canto esquerdo superior da região e pressione Enter.")
    input()  # Aguarda até que o Enter seja pressionado
    ponto_superior_esquerdo = py.position()
    
    print("Coloque o mouse no canto direito inferior da região e pressione Enter.")
    input()
    ponto_inferior_direito = py.position()

    # Calcula a região com base nas coordenadas
    x1, y1 = ponto_superior_esquerdo
    x2, y2 = ponto_inferior_direito
    regiao = (x1, y1, x2 - x1, y2 - y1)  # (x, y, largura, altura)

    return regiao

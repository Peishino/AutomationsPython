from Funcoes_CDP import abrir_jogo_com_debug, GameCDP, get_region_cdp

abrir_jogo_com_debug()
game = GameCDP()

regiao_start_combat = get_region_cdp(game)
print("Copia isso pro seu Arena_auto:", regiao_start_combat)

game.close()
import sys
import os
import random
import time
import select
import tty
import termios

if len(sys.argv) > 1:
    SEED = sys.argv[1]
    random.seed(SEED)
else:
    SEED = 42
    random.seed(SEED)

print(f'Seed de geração: {SEED}')

# REGRAS DO JOGO DA VIDA DE CONWAY
# 1. SOBREVIVÊNCIA: Uma célula viva com 2 ou 3 vizinhos vivos sobrevive.
# 2. MORTE (SOLIDÃO): Uma célula viva com menos de 2 vizinhos vivos morre.
# 3. MORTE (SUPERPOPULAÇÃO): Uma célula viva com mais de 3 vizinhos vivos morre.
# 4. NASCIMENTO: Uma célula morta com exatamente 3 vizinhos vivos torna-se viva.

# Caracteres para representar as células (ANSI)
COR_VIVA = "\033[42m \033[0m" # fundo colorido
COR_MORTA = " "


def inicializar_grid(largura, altura):
    print("Gerando mundo aleatório...")
    return [[1 if random.randint(0, 3) == 0 else 0 for _ in range(largura)] for _ in range(altura)]

def desenhar_grid(grid):
    buffer = ["\033[H"]
    for linha in grid:
        str_linha = "".join([COR_VIVA if celula == 1 else COR_MORTA for celula in linha])
        buffer.append(str_linha)
    
    sys.stdout.write("\n".join(buffer))
    sys.stdout.flush()

def calcular_proxima_geracao(grid):
    altura = len(grid)
    largura = len(grid[0])
    next_grid = [[0 for _ in range(largura)] for _ in range(altura)]

    for y in range(altura):
        for x in range(largura):
            vizinhos_vivos = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue  # Não conta a própria célula
                    
                    nx = (x + dx) % largura
                    ny = (y + dy) % altura

                    if grid[ny][nx] == 1:
                        vizinhos_vivos += 1
            
            estado_atual = grid[y][x]
            
            if estado_atual == 1 and vizinhos_vivos in [2, 3]:
                next_grid[y][x] = 1  # Sobrevivência
            elif estado_atual == 0 and vizinhos_vivos == 3:
                next_grid[y][x] = 1  # Nascimento
            else:
                next_grid[y][x] = 0  # Morte (solidão ou superpopulação)

    return next_grid

def get_key():
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1)
    return None

def main():
    try:
        largura, altura = os.get_terminal_size()
        # Subtrai 1 da altura para evitar que o prompt de comando pule ao final
        altura -= 1
    except OSError:
        largura, altura = 80, 24  # Valores padrão se não for um terminal

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        sys.stdout.write("\033[?25l")  # Esconde o cursor
        tty.setcbreak(fd)

        grid = inicializar_grid(largura, altura)
        time.sleep(1) # Pausa para ver a mensagem "Gerando mundo..."

        while True:
            desenhar_grid(grid)
            grid = calcular_proxima_geracao(grid)

            key = get_key()
            if key == 'q':
                print("Saindo...")
                break
            elif key == 'r':
                grid = inicializar_grid(largura, altura)
                time.sleep(1)

            time.sleep(0.05) # Controla a velocidade da simulação

    finally:
        # Restaura o estado original do terminal ao sair
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\033[?25h\n") # Restaura o cursor e pula uma linha

if __name__ == "__main__":
    main()

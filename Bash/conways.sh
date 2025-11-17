#!/bin/bash

# REGRAS

# SOBREVIVENCIA
# MORTE POR UNDERPOPULATION
# MORTE POR SUPERPOPULACAO
# NASCIMENTO
 
# vizinhos são outras celulas ou espaços diretamente conectados
# qualquer celula com menos de dois vizinhos morre (underpopulation)
# qualquer celula com dois ou três vive para a proxima geração 
# qualquer celula com mais de três vizinhos morre (overpopulation)
# três celulas formam uma celula nova (reprodução)

# Configurações iniciais
trap "tput cnorm; clear; exit" SIGINT SIGTERM # Restaura o cursor ao sair (Ctrl+C)
tput civis # Esconde o cursor para ficar mais bonito

COR_VIVA="\e[42m \e[0m" # Fundo verde (espaço)
COR_MORTA=" "

# Dimensões 
largura=$(tput cols)
altura=$(tput lines)

# Arrays para o estado atual e o próximo
declare -a grid
declare -a next_grid
size=$((largura * altura))


# Inicializa o grid com valores aleatórios (0 ou 1)
inicializar() {
    echo "Gerando mundo aleatório..."
    for ((i=0; i<size; i++)); do
        if (( RANDOM % 4 == 0 )); then
    grid[$i]=1
        else
            grid[$i]=0
        fi
    done
}

# Desenha o grid na tela
desenhar() {
    tput cup 0 0 
    
    local buffer=""
    
    for ((y=0; y<altura; y++)); do
        for ((x=0; x<largura; x++)); do
            idx=$((y * largura + x))
            if (( grid[idx] == 1 )); then
                buffer+="${COR_VIVA}"
            else
                buffer+="${COR_MORTA}"
            fi
        done
        buffer+=$'\n' 
    done
    printf "%b" "$buffer"
}

# Conta vizinhos e aplica as regras
calcular_proxima_geracao() {
    for ((y=0; y<altura; y++)); do
        for ((x=0; x<largura; x++)); do
            idx=$((y * largura + x))
            vizinhos=0

            # Verifica os 8 vizinhos (com wrap-around/mundo toroidal)
            for dy in -1 0 1; do
                for dx in -1 0 1; do
                    if (( dx == 0 && dy == 0 )); then continue; fi
                    
                    # Lógica toroidal (se sair pela direita, volta na esquerda)
                    nx=$(( (x + dx + largura) % largura ))
                    ny=$(( (y + dy + altura) % altura ))
                    nidx=$((ny * largura + nx))

                    if (( grid[nidx] == 1 )); then
                        ((vizinhos++))
                    fi
                done
            done

            estado=${grid[$idx]}
            
            # APLICAÇÃO DAS REGRAS DO JOGO DA VIDA
            if (( estado == 1 )); then
                if (( vizinhos < 2 || vizinhos > 3 )); then
                    next_grid[$idx]=0 # Morre
                else
                    next_grid[$idx]=1 # Vive
                fi
            else
                if (( vizinhos == 3 )); then
                    next_grid[$idx]=1 # Nasce
                else
                    next_grid[$idx]=0 # Continua morto
                fi
            fi
        done
    done

    # Atualiza o grid principal
    for ((i=0; i<size; i++)); do
        grid[$i]=${next_grid[$i]}
    done
}


inicializar

while true; do
    desenhar
    calcular_proxima_geracao
    
    # Verifica input do usuário (non-blocking)
    # -t 0.01 define a velocidade (tempo de espera)
    read -t 0.01 -n 1 key
    
    if [[ $key == "q" ]]; then
        echo "Saindo..."
        break
    elif [[ $key == "r" ]]; then
        inicializar
    fi
done

tput cnorm # Restaura cursor

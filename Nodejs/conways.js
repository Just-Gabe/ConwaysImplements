// REGRAS DO JOGO DA VIDA DE CONWAY
// 1. SOBREVIVÊNCIA: Uma célula viva com 2 ou 3 vizinhos vivos sobrevive.
// 2. MORTE (SOLIDÃO): Uma célula viva com menos de 2 vizinhos vivos morre.
// 3. MORTE (SUPERPOPULAÇÃO): Uma célula viva com mais de 3 vizinhos vivos morre.
// 4. NASCIMENTO: Uma célula morta com exatamente 3 vizinhos vivos torna-se viva.

const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

const vivo = 'O';
const morto = '';

const altura = 500
const largura = 400

function inicializarGrid() {
    console.log("Gerando novo mundo aleatório no servidor...");
    return Array.from({ length: ALTURA }, () =>
        Array.from({ length: LARGURA }, () => (Math.random() < 0.25 ? 1 : 0))
    );
}

function calculoProxGeracao(grid){
  const altura = grid.length;
  const largura = grid[0].length;
  const proxGrid = Array.from({ length: altura }, () => Array(largura).fill(0)); 
  
  for (let y=0; y < altura; y++){
    for(let x=0; x < largura; x++){
      
      let vizinhosVivos = 0;
      
      for (let vizinhosY = -1; dy <=1; dy++){
        for (let vizinhosX = -1)
      }

    }
  }

}


app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});

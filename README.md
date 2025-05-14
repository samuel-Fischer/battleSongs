# 🎵 Song Battles


**Song Battles** é um sistema criado para ranquear músicas com base em batalhas entre duas faixas, decididas por meio de votações dos usuários. O projeto nasceu como uma forma de entretenimento para um servidor no Discord de uma fanbase.

A ideia central do projeto se inspira na metodologia de organização *Merge Sort*, onde as músicas são gradualmente organizadas em uma hierarquia de acordo com os resultados das batalhas — sejam diretas (quando duas músicas são comparadas entre si) ou indiretas (quando o histórico de batalhas já permite inferir a posição relativa de músicas que ainda não se enfrentaram diretamente).

### 🔍 Exemplo prático:

Imagine que a música **A** venceu a música **B**, e a música **B** venceu a música **C**. Mesmo sem uma batalha direta entre **A** e **C**, o sistema consegue inferir que **A** está acima de **C** no ranking atual.

---

Agora, vamos considerar um exemplo com cinco músicas reais: **Chlorine**, **Stressed Out**, **Heathens**, **Ride** e **Car Radio**.

As batalhas ocorreram na seguinte ordem:

1. **Chlorine** venceu **Stressed Out**
2. **Stressed Out** venceu **Heathens**
3. **Ride** venceu **Heathens**
4. **Car Radio** venceu **Ride** (_Aqui já conseguimos saber que Heathens fica na última posição, porque perdeu para todas as músicas, direta ou indiretamente._)
5. **Chlorine** venceu **Car Radio** (_Neste ponto, já é possível afirmar que Chlorine ocupa o topo do ranking, e Car Radio a segunda posição._)
6. **Stressed Out** venceu **Ride** (_Neste ponto, todas as posições do ranking já estão definidas, mesmo sem comparações diretas entre todas as músicas._)

Mesmo sem todas as batalhas diretas (por exemplo, **Chlorine** nunca enfrentou **Heathens**), o sistema utiliza os dados anteriores para inferir a seguinte hierarquia:

➡️ `Chlorine > Car Radio > Ride > Stressed Out > Heathens`

---

Esse modelo de ranqueamento reduz a necessidade de comparações diretas entre todas as músicas. À medida que mais batalhas são registradas, o sistema se torna mais eficiente, construindo um ranking coerente de forma progressiva.

---

## ✅ TODO

### 🚨 Melhorias urgentes
- [ ] **Otimizar o processo para adicionar novas batalhas.** (pelo grande número de músicas competindo, o programa está demorando mais do que deveria para realizar as comparações) - `(2)`

### 🛠️ Lógica e funcionalidades
- [ ] Ao adicionar uma batalha, incluir o número da batalha na mensagem. ex: "✅ XXXº batalha inserida com sucesso!" - `(2)`
- [ ] Permitir abreviações para álbuns e, possivelmente, músicas. - `(2)`
- [ ] Corrigir falha ao buscar músicas que ainda não batalharam. (de forma indireta) - `(5)`
- [ ] Incluir número da batalha no histórico de batalhas. - `(4)`
- [ ] Corrigir visualização de derrotas da música. (ex do que acontece com 'Heavydirtysoul') - `(4)`
- [ ] Verificar contagem incorreta de vitórias/derrotas. (ex: 'Addict With a Pen') `(4)`
- [ ] Adicionar ranking atual da música e o melhor resultado possível. `(4)`

<small>*- Os números entre parênteses __()__ referem-se à função que ela exerce no __menu__.*</small>

---

## 📁 Estrutura do Projeto

```
/battleSongs
├── battles.csv
├── songs.csv
└── songBattles.py
```

---

## 🚀 Como executar

  1. Clone o repositório.
  2. Abra o terminal na pasta do projeto.
  3. Execute o script principal com o comando: ```python songBattles.py``` (Certifique-se de ter o Python instalado em seu sistema)
  4. Siga as instruções no terminal para iniciar as batalhas.

---

## 📌 Observações

- Projeto para passar o tempo.
- Contribuições e feedbacks são bem-vindos!

---

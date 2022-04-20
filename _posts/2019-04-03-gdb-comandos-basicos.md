---
layout: post
title: GDB - Comandos básicos
date: 2019-04-03 22:08
author: obrerodrigues
categories: [Hacking]
---

Estava eu, compilando uns links para auxiliar uns chegados no aprendizado da arte obscura da engenharia reversa, quando, ao iniciar as pesquisas sobre algo relacionado ao gdb, me frustrei por não encontrar porra nenhuma em pt-br. E claro que isso não é admissível.

Então me meti a escrever algo simples para colaborar com a galera e evitar que se sintam perdidos e sozinhos no terminal quando abrirem o gdb.

São os comandos básicos que utilizo e exemplos de como usar. Se algumda dúvida persistir, o [manual](https://sourceware.org/gdb/current/onlinedocs/gdb/) deverá ser consultado.

** A formatação desse texto ficou uma bosta, se te incomoda, lê direto no [git](https://github.com/brerodrigues/brerodrigues.github.io/blob/master/_posts/2019-04-03-gdb-comandos-basicos.md): 

- *gdb binario*: executando e passando o binário que será debugado.

```
$ gdb binario
GNU gdb (Ubuntu 8.1-0ubuntu3) 8.1.0.20180409-git
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from binario...(no debugging symbols found)...done.
(gdb) 
```

Ao se passar *-q*, não é impresso esse banner gigante.

```
$ gdb binario -q
Reading symbols from binario...(no debugging symbols found)...done.
(gdb)
```

- *info functions*: vai listar as funções.

```
(gdb) info functions
All defined functions:

Non-debugging symbols:
0x0000000000000558  _init
0x0000000000000580  puts@plt
0x0000000000000590  printf@plt
0x00000000000005a0  atoi@plt
0x00000000000005b0  __cxa_finalize@plt
0x00000000000005c0  _start
0x00000000000005f0  deregister_tm_clones
0x0000000000000630  register_tm_clones
0x0000000000000680  __do_global_dtors_aux
0x00000000000006c0  frame_dummy
0x00000000000006ca  main
0x0000000000000750  __libc_csu_init
0x00000000000007c0  __libc_csu_fini
0x00000000000007c4  _fini
(gdb) 
```

- *disas nome_funcao*: vai trazer o assembly da função.

```
(gdb) disas main
Dump of assembler code for function main:
   0x00000000000006ca <+0>:	push   %rbp
   0x00000000000006cb <+1>:	mov    %rsp,%rbp
   0x00000000000006ce <+4>:	sub    $0x20,%rsp
   0x00000000000006d2 <+8>:	mov    %edi,-0x14(%rbp)
   0x00000000000006d5 <+11>:	mov    %rsi,-0x20(%rbp)
   0x00000000000006d9 <+15>:	movl   $0x3e7,-0x8(%rbp)
   0x00000000000006e0 <+22>:	cmpl   $0x1,-0x14(%rbp)
   0x00000000000006e4 <+26>:	jg     0x708 <main+62>
   0x00000000000006e6 <+28>:	mov    -0x20(%rbp),%rax
   0x00000000000006ea <+32>:	mov    (%rax),%rax
   0x00000000000006ed <+35>:	mov    %rax,%rsi
   0x00000000000006f0 <+38>:	lea    0xdd(%rip),%rdi        # 0x7d4
   0x00000000000006f7 <+45>:	mov    $0x0,%eax
   0x00000000000006fc <+50>:	callq  0x590 <printf@plt>
   0x0000000000000701 <+55>:	mov    $0x1,%eax
   0x0000000000000706 <+60>:	jmp    0x745 <main+123>
   0x0000000000000708 <+62>:	mov    -0x20(%rbp),%rax
   0x000000000000070c <+66>:	add    $0x8,%rax
   0x0000000000000710 <+70>:	mov    (%rax),%rax
   0x0000000000000713 <+73>:	mov    %rax,%rdi
   0x0000000000000716 <+76>:	callq  0x5a0 <atoi@plt>
   0x000000000000071b <+81>:	mov    %eax,-0x4(%rbp)
   0x000000000000071e <+84>:	mov    -0x8(%rbp),%eax
   0x0000000000000721 <+87>:	cmp    -0x4(%rbp),%eax
   0x0000000000000724 <+90>:	jne    0x734 <main+106>
   0x0000000000000726 <+92>:	lea    0xb8(%rip),%rdi        # 0x7e5
   0x000000000000072d <+99>:	callq  0x580 <puts@plt>
   0x0000000000000732 <+104>:	jmp    0x740 <main+118>
   0x0000000000000734 <+106>:	lea    0xb9(%rip),%rdi        # 0x7f4
   0x000000000000073b <+113>:	callq  0x580 <puts@plt>
   0x0000000000000740 <+118>:	mov    $0x0,%eax
   0x0000000000000745 <+123>:	leaveq 
   0x0000000000000746 <+124>:	retq   
End of assembler dump.
(gdb)
```

- *set disassembly flavor*: para mudar a forma de representação do assembly entre Intel e AT&T. A maioria da galera acha a Intel mais fácil de ler. Se quiser saber a diferença entre as duas dá uma olhada [aqui](https://pt.wikibooks.org/wiki/Assembly_no_Linux/Sintaxes_e_ferramentas

```
(gdb) set disassembly-flavor intel
```

E agora observe a diferença para o *disasm main* anterior:

```
(gdb) disas main
Dump of assembler code for function main:
   0x00000000000006ca <+0>:	push   rbp
   0x00000000000006cb <+1>:	mov    rbp,rsp
   0x00000000000006ce <+4>:	sub    rsp,0x20
   0x00000000000006d2 <+8>:	mov    DWORD PTR [rbp-0x14],edi
   0x00000000000006d5 <+11>:	mov    QWORD PTR [rbp-0x20],rsi
   0x00000000000006d9 <+15>:	mov    DWORD PTR [rbp-0x8],0x3e7
   0x00000000000006e0 <+22>:	cmp    DWORD PTR [rbp-0x14],0x1
   0x00000000000006e4 <+26>:	jg     0x708 <main+62>
   0x00000000000006e6 <+28>:	mov    rax,QWORD PTR [rbp-0x20]
   0x00000000000006ea <+32>:	mov    rax,QWORD PTR [rax]
   0x00000000000006ed <+35>:	mov    rsi,rax
   0x00000000000006f0 <+38>:	lea    rdi,[rip+0xdd]        # 0x7d4
   0x00000000000006f7 <+45>:	mov    eax,0x0
   0x00000000000006fc <+50>:	call   0x590 <printf@plt>
   0x0000000000000701 <+55>:	mov    eax,0x1
   0x0000000000000706 <+60>:	jmp    0x745 <main+123>
   0x0000000000000708 <+62>:	mov    rax,QWORD PTR [rbp-0x20]
   0x000000000000070c <+66>:	add    rax,0x8
   0x0000000000000710 <+70>:	mov    rax,QWORD PTR [rax]
   0x0000000000000713 <+73>:	mov    rdi,rax
   0x0000000000000716 <+76>:	call   0x5a0 <atoi@plt>
   0x000000000000071b <+81>:	mov    DWORD PTR [rbp-0x4],eax
   0x000000000000071e <+84>:	mov    eax,DWORD PTR [rbp-0x8]
   0x0000000000000721 <+87>:	cmp    eax,DWORD PTR [rbp-0x4]
   0x0000000000000724 <+90>:	jne    0x734 <main+106>
   0x0000000000000726 <+92>:	lea    rdi,[rip+0xb8]        # 0x7e5
   0x000000000000072d <+99>:	call   0x580 <puts@plt>
   0x0000000000000732 <+104>:	jmp    0x740 <main+118>
   0x0000000000000734 <+106>:	lea    rdi,[rip+0xb9]        # 0x7f4
   0x000000000000073b <+113>:	call   0x580 <puts@plt>
   0x0000000000000740 <+118>:	mov    eax,0x0
   0x0000000000000745 <+123>:	leave  
   0x0000000000000746 <+124>:	ret    
End of assembler dump.
```

- *break* ou *b*: seta um [breakpoint](https://pt.wikipedia.org/wiki/Ponto_de_parada). Você pode usar o nome da função como referência ou passar um endereço direto.

```
(gdb) b *main
Breakpoint 1 at 0x6ce
```

E até usar *b *main+26*

```
(gdb) b *main+26
Breakpoint 2 at 0x6e4
```

- *info break* ou *info b*: lista breakpoints.

```
(gdb) info b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x00000000000006ca <main>
2       breakpoint     keep y   0x00000000000006e4 <main+26>
```

- *del 1*: remove breakpoint por número.

```
(gdb) del 2
(gdb) info b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x00000000000006ca <main>
```

- *run*: roda o programa

```
(gdb) run
Starting program: /home/b/gdb_post/binario 
Uso: /home/b/gdb_post/binario [senha]
[Inferior 1 (process 12083) exited with code 01]
(gdb) 
```

- *continue* ou *c*: resume execução do binário apos bater em breakpoint.

```
(gdb) b *main
Breakpoint 1 at 0x5555555546ca
(gdb) run
Starting program: /home/b/gdb_post/binario 

Breakpoint 1, 0x00005555555546ca in main ()
(gdb) c
Continuing.
Uso: /home/b/gdb_post/binario [senha]
[Inferior 1 (process 12087) exited with code 01]
```

- *r*: reinicia execução do binário

```
(gdb) r
Starting program: /home/b/gdb_post/binario 
```

Antes de continuar, deixe-me introduzir o [PEDA](https://github.com/longld/peda). É um não tão simples script python para trazer úteis funcionalidades ao debugger. Tente usar sem e depois com e tire suas conclusões. Antes de conhece-lo, passei muito tempo analisando stack, endereços, etc, na mão. Era foda. Pensei em mostrar como era feito antes de conhecer o PEDA, mas não achei necessário essa perda de tempo. Então, antes de executar os exemplos seguintes, configure seu GDB:

```
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
echo "DONE! debug your program with gdb and enjoy"
```

E não esqueça de dar uma olhada nos novos comandos que estarão disponíveis, serão úteis um dia: [https://github.com/longld/peda](https://github.com/longld/peda). As próximas saídas do GDB serão cortadas para não exibir a caralhada de informações que o PEDA imprime a cada breakpoint.
 
- *next*: executa proxima linha do binário (sem entrar em chamadas de função).

```
gdb-peda$ b *main
Breakpoint 1 at 0x6ca
gdb-peda$ run
Starting program: /home/b/gdb_post/binario 

[----------------------------------registers-----------------------------------]
RAX: 0x5555555546ca (<main>:	push   rbp)
[...]
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x5555555546c1 <frame_dummy+1>:	mov    rbp,rsp
   0x5555555546c4 <frame_dummy+4>:	pop    rbp
   0x5555555546c5 <frame_dummy+5>:	jmp    0x555555554630 <register_tm_clones>
*=> 0x5555555546ca <main>:	push   rbp*
   0x5555555546cb <main+1>:	mov    rbp,rsp
   0x5555555546ce <main+4>:	sub    rsp,0x20
   0x5555555546d2 <main+8>:	mov    DWORD PTR [rbp-0x14],edi
   0x5555555546d5 <main+11>:	mov    QWORD PTR [rbp-0x20],rsi
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe578 --> 0x7ffff7a05b97 (<__libc_start_main+231>:	mov    edi,eax)
[...]
0056| 0x7fffffffe5b0 --> 0x5555555545c0 (<_start>:	xor    ebp,ebp)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x00005555555546ca in main ()
```

E, após bater num breakpoint, usa-se *n* para ir a próxima instrução:

```
gdb-peda$ n

[----------------------------------registers-----------------------------------]
RAX: 0x5555555546ca (<main>:	push   rbp)
[...]
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x5555555546c4 <frame_dummy+4>:	pop    rbp
   0x5555555546c5 <frame_dummy+5>:	jmp    0x555555554630 <register_tm_clones>
   0x5555555546ca <main>:	push   rbp
*=> 0x5555555546cb <main+1>:	mov    rbp,rsp*
   0x5555555546ce <main+4>:	sub    rsp,0x20
   0x5555555546d2 <main+8>:	mov    DWORD PTR [rbp-0x14],edi
   0x5555555546d5 <main+11>:	mov    QWORD PTR [rbp-0x20],rsi
   0x5555555546d9 <main+15>:	mov    DWORD PTR [rbp-0x8],0x3e7
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe570 --> 0x555555554750 (<__libc_csu_init>:	push   r15)
[...]
0056| 0x7fffffffe5a8 --> 0xe169e4e8e633c51c 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x00005555555546cb in main ()
```
 
- *step*: executa proxima linha do binário (entrando em chamadas de função)

Ao chegar com o breakpoint em uma instrução tipo *0x5555555546fc <main+50>:	call   0x555555554590 <printf@plt>* e usar o *next*, printf vai ser executada e seguiremos a próxima instrução de main. Ao se usar *step*, se entra na função, no caso printf.

```
gdb-peda$ 

[----------------------------------registers-----------------------------------]
RAX: 0x0 
[...]
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x5555555546ed <main+35>:	mov    rsi,rax
   0x5555555546f0 <main+38>:	lea    rdi,[rip+0xdd]        # 0x5555555547d4
   0x5555555546f7 <main+45>:	mov    eax,0x0
*=> 0x5555555546fc <main+50>:	call   0x555555554590 <printf@plt>*
   0x555555554701 <main+55>:	mov    eax,0x1
   0x555555554706 <main+60>:	jmp    0x555555554745 <main+123>
   0x555555554708 <main+62>:	mov    rax,QWORD PTR [rbp-0x20]
   0x55555555470c <main+66>:	add    rax,0x8
Guessed arguments:
arg[0]: 0x5555555547d4 ("Uso: %s [senha]\n")
arg[1]: 0x7fffffffe9a7 ("/home/b/gdb_post/binario")
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe550 --> 0x7fffffffe658 --> 0x7fffffffe9a7 ("/home/b/gdb_post/binario")
[...]
0056| 0x7fffffffe588 --> 0x7fffffffe658 --> 0x7fffffffe9a7 ("/home/b/gdb_post/binario")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x00005555555546fc in main ()
gdb-peda$ s

[----------------------------------registers-----------------------------------]
RAX: 0x0 
[...]
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x7ffff7a48e6c <__fprintf+172>:	call   0x7ffff7b18c80 <__stack_chk_fail>
   0x7ffff7a48e71:	nop    WORD PTR cs:[rax+rax*1+0x0]
   0x7ffff7a48e7b:	nop    DWORD PTR [rax+rax*1+0x0]
*=> 0x7ffff7a48e80 <__printf>:	sub    rsp,0xd8*
   0x7ffff7a48e87 <__printf+7>:	test   al,al
   0x7ffff7a48e89 <__printf+9>:	mov    QWORD PTR [rsp+0x28],rsi
   0x7ffff7a48e8e <__printf+14>:	mov    QWORD PTR [rsp+0x30],rdx
   0x7ffff7a48e93 <__printf+19>:	mov    QWORD PTR [rsp+0x38],rcx
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe548 --> 0x555555554701 (<main+55>:	mov    eax,0x1)
[...]
0056| 0x7fffffffe580 --> 0x1 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
__printf (format=0x5555555547d4 "Uso: %s [senha]\n") at printf.c:28
28	printf.c: No such file or directory.
gdb-peda$ 
```

- *jump*: pula a execução do binário para algum endereço arbitrário.

```
gdb-peda$ b *main+124
Breakpoint 2 at 0x555555554746
gdb-peda$ j *main+124
Continuing at 0x555555554746.

[----------------------------------registers-----------------------------------]
RAX: 0x5555555546ca (<main>:	push   rbp)
[...]
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x55555555473b <main+113>:	call   0x555555554580 <puts@plt>
   0x555555554740 <main+118>:	mov    eax,0x0
   0x555555554745 <main+123>:	leave  
*=> 0x555555554746 <main+124>:	ret    *
   0x555555554747:	nop    WORD PTR [rax+rax*1+0x0]
   0x555555554750 <__libc_csu_init>:	push   r15
   0x555555554752 <__libc_csu_init+2>:	push   r14
   0x555555554754 <__libc_csu_init+4>:	mov    r15,rdx
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe578 --> 0x7ffff7a05b97 (<__libc_start_main+231>:	mov    edi,eax)
[...]
0056| 0x7fffffffe5b0 --> 0x5555555545c0 (<_start>:	xor    ebp,ebp)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 2, 0x0000555555554746 in main ()
```

- *x*: para examinar a memória. É um pouco mais complexo que os comandos anteriores porque é preciso que você saiba o que está procurando.
Por exemplo: x/4xw $sp tratá 4 words do $sp, que é o stack pointer.

```
gdb-peda$ x/4xw $sp
0x7fffffffe578:	0xf7a05b97	0x00007fff	0x00000001	0x00000000
```

[Dúvidas?](https://sourceware.org/gdb/current/onlinedocs/gdb/)

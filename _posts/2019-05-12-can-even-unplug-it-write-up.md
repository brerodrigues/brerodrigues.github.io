---
layout: post
title: Cant_even_unplug_it - [DEF CON CTF Qualifier 2019]
date: 2019-05-12 22:00
author: obrerodrigues
comments: true
categories: [CTFs]
---
No fim de semana (11/05/2019), participei, com meu time, do [DEF CON CTF Qualifier](https://ctftime.org/event/762). 

Como era esperado de um evento qualificatorio para a [Defcon](https://www.defcon.org/), a maior parte dos desafios estavam bem acima do meu nível, então fiquei feliz quando consegui resolver um da categoria *FIRST CONTACT*, que tinha desafios mais simples do que das outras categorias.

O desafio em questão foi o *cant_even_unplug_it*. E a descrição era a seguinte:

> You know, we had this up and everything. Prepped nice HTML5, started deploying on a military-grade-secrets.dev subdomain, got the certificate, the whole shabang. Boss-man got moody and wanted another name, we set up the new names and all. Finally he got scared and unplugged the server. Can you believe it? Unplugged. Like that can keep it secret…

E anexado ao desafio havia um arquivo txt com o nome *Hint* e o conteúdo:

> Hint: these are HTTPS sites. Who is publicly and transparently logging the info you need?
Just in case: all info is freely accessible, no subscriptions are necessary. The names cannot really be guessed. 

Certo, a descrição me diz que eles trabalharam num site, arrumaram o subdominio military-grade-secrets.dev, hospedaram o site, arrumaram um certificado HTTPS e etc. Então o chefe resolveu trocar o nome do domínio e logo depois mandou desligar o servidor. Finaliza com os dizeres: "Acredita nisso? Desligar o servidor... Como se isso fosse manter os dados em segredo...".

O arquivo txt Hint  dá a idéia que eles são sites https e pergunta "Quem está transparentemente logando as informações que você precisa?". E completa que as informações necessárias podem ser obtidas de graça e que não seriam muito "adivinháveis".

Com isso, fui atrás de quem estava "logando as informações que eu precisava" e joguei no google "publicly and transparency logging certificates" e aprendi como [*Certificate Transparency*](https://en.wikipedia.org/wiki/Certificate_Transparency) é usado para logar e auditar *certificados digitais*. Então imaginei que o novo domínio teria seu endereço logado em algum lugar, afinal, precisaria do certificado.

Pesquisando pela internet por "*transparency certificate logging search*" e cheguei em [https://transparencyreport.google.com/https/certificates](https://transparencyreport.google.com/https/certificates). Nesse site há a opção de buscar os certificados pelo nome do host e, buscando por military-grade-secrets.dev (sem esquecer de incluir os subdomínios na pesquisa), encontrei os dominios: *now.under.even-more-militarygrade.pw.military-grade-secrets.dev* e o *secret-storage.military-grade-secrets.dev*. 

O *now.under.even-more*, por ter sido registrado mais recente, foi a primeira pista que segui. Tentei acessa-lo no navegador mas não tive sucesso, então usei o *curl* pela linha de comando e obtive a resposta:

<script src="https://gist.github.com/brerodrigues/0d807a7deb61a6104343ee75c89f5b29.js"></script>

Aparentemente o servidor http responde com um 302 e nos redireciona para *https://forget-me-not.even-more-militarygrade.pw/* que, na minha noobice, achei que seria o endereço da flag, mas infelizmente o servidor não me respondia.

Fiquei um tempo pensando e, por confiar que num CTF do nível de qualificatórias para a Def con não haveria algo guessing randômico, voltei a reler com atenção a descrição e tive uma epifania graças à última parte que dizia: *Finally he got scared and unplugged the server. Can you believe it? Unplugged. Like that can keep it secret…*

Ou seja, claro que nada viria daquele endereço, o servidor foi desconectado da internet. Haveria uma forma de obter as informações que um dia estavam online e outra não? Claro que sim. Pela [Wayback Machine](https://web.archive.org/).

E após pesquisar pelo domínio forgetme-not, encontrei [isso](https://web.archive.org/web/20190427160922/https://forget-me-not.even-more-militarygrade.pw/) com a flag bem vísivel: 

THE FLAG IS: OOO{DAMNATIO_MEMORIAE}

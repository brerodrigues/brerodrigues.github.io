---
layout: post
title: Fiz o exame da OSCP e veja no que deu (ou um não-guia para a OSCP)
date: 2023-07-01 20:15
author: obrerodrigues
comments: true
categories: [Hacking, Favorites]
tags: [OSCP, Offsec, certificação]
---
Eu iria fazer um único texto sobre a certificação mas percebi que o mesmo começou a ficar longo. Então separei em dois. Nessa versão conto minha experiência em primeira pessoa desde a compra do curso até o exame. Na próxima versão (atualizo esse post assim que publicar, enquanto isso recomendo [esse link aqui](https://johnjhacking.com/blog/oscp-reborn-2023/)) compartilharei uns conselhos mais práticos e úteis, seja para noobs da área de segurança ou para alguém mais experiente.

Bora lá.

Dizem por aí que quem consegue essa certificação e não posta sobre o assunto nunca mais consegue acesso root em um servidor. Então aqui vai minha história.

Posso dizer que tenho algum background e experiência hackeando umas coisas. O leitor atento pode observar que tenho textos horríveis e sem revisão de 2009, época em que eu era uma criança fazendo o que não deve e que só mantenho online como registro histórico. Um exemplo é a pérola [em que ensino a fazer como fazer ligações em telefones trancados](https://brerodrigues.github.io/hacking/favorites/2009/10/12/fazendo-ligacoes-em-telefones-trancados.html). Aliás, a pausa que descrevi ser de 7 segundos entre pulsos parece excessivamente longa, 2 ou 3 segundos são suficientes. Tendo em vista esses fatos, posso me definir como alguém que não é um iniciante no hacking.

Comprei o curso em outubro de 2022, mas só comecei a fazê-lo em dezembro (após a compra é possível decidir qual a data de inicio). Em 2023 saiu uma versão atualizada, mas essa postagem não entra o suficiente nas especificidades do curso, então ainda o vejo como útil. Utilizei um tempo pré-curso para afiar minhas habilidades fazendo algumas máquinas Windows do HTB e alguns cursos relacionados ao Active Directory.

Decidi planejar os 90 dias de curso assim: 30 dias estudando o material e fazendo todos os exercícios e os 60 restantes hackeando o máximo de máquinas possíveis nos labs.

Minha ideia era passar por cima do material de forma superficial porque eu dominava quase todo o conteúdo. As exceções eram os módulos de escalação de privilégios no Windows e a parte do AD. Os exercícios precisavam ser feitos por que, além de ser necessário no mínimo 80% de completude nos mesmos (e 30 máquinas hackeadas nos labs) para obter 10 pontos extras para o exame, saber que acertei os exercícios me daria a confiança de que eu realmente dominava o conteúdo.

Nos 30 dias iniciais finalizei os exercícios com relativa facilidade. Estudei algumas horinhas todos os dias e nos fins de semana dava um gás a mais. É mais fácil investir seu tempo livre quando você curte o negócio e sonhava com essa merda desde a época que descobriu o [BackTrack](https://en.wikipedia.org/wiki/BackTrack) em 2008. O material não é profundo e tem aquela filosofia de te ensinar o básico e depois te cobrar um pouco mais nos exercícios. Aquela vibe de ensinar a pescar e não te dar o peixe. Um novato teria que se matar e pôr muito mais horas que eu para consumir o curso e ainda ter tempo para os labs. Apanhei na parte de AD e foi lá que deixei para trás um dos únicos exercícios que não completei. Claro que isso deu um baque na minha confiança. Que tipo de hacker era eu que não conseguia um Domain Admin nos exercícios? Minha mente me dizia que era óbvio que eu ia me foder no exame se continuasse assim.

Ah, um segredo: desde as primeiras seções do curso eu fui fazendo anotações utilizando o Obsidian. Nada verboso. Anotava o que sentia que iria precisar um dia, sabe? A ideia era fazer notas práticas e não um resumo do material.

Fui para os labs. Comecei a escanear e hackear furiosamente tudo que podia. Priorizei as máquinas Windows e fui em busca dos Active Directories por saber que eram meus pontos fracos. Tentava não passar muito tempo em algum alvo que eu estivesse completamente sem rumo porque era possível que ele tivesse alguma dependência (nos labs há máquinas que não são vulneráveis inicialmente e só podem ser comprometidas ao se acessar uma outra máquina). Nesse processo, minhas anotações eram testadas e eu as enriquecia a cada novo comando que eu aprendia. Em determinado momento comecei a montar um checklist de passos e os respectivos comando ou ferramentas utilizadas para ownar uma máquina porque percebi que um dos meus erros mais comuns era esquecer de fazer algo bobo, como por exemplo não tentar logar em um serviço com credenciais default. Percebi minha tendência a pensar demais, ir para as soluções complexas ao invés de enxergar as simples. Seria um erro fatal levar esse defeito para um exame em que o tempo era meu maior rival.

Foi assim que encarei os labs e onde achei seu maior valor: encontrar o que iria fazer com que eu falhasse no exame e corrigir antes do dia da prova.

Algumas vezes usei o Discord da Offsec, na área privada dos alunos, para procurar hints de máquinas que me deixavam encucado. Em algum dos conselhos ([nem sempre tão úteis](https://www.youtube.com/watch?v=6Aw0yOMBbiY)) que li dos monitores, recebi um que acredito ter sido o segredo da minha aprovação: "**TUDO QUE VOCÊ PRECISA PARA HACKEAR OS LABS E PASSAR NO EXAME ESTÁ NO MATERIAL DO CURSO**". Eu usei essa recomendação para cortar pela raiz meu mal de overthinking.

No final, consegui acesso completo a 34 máquinas dos labs e uma análise/acesso inicial em outras 19, o que dá um total de 53 máquinas fuçadas (também peguei acesso a duas redes internas além da pública). Depois que eu passei das 30 mínimas para obter os 10 pontos extras, tirei o pé do acelerador porque me vi repetindo meus processos e hackeando máquinas com vulnerabilidades parecidas, algo que não estava adicionando munição para o exame. Então foquei, encontrei, explorei, entendi bem e fiz boas notas sobre os 2 Active Directories que estavam rodando nos labs e fiquei brincando com umas máquinas Windows para treinar outros conceitos, como o buffer overflow, ataques client side e escalação de privilégios.

Quando chegou o meu último dia de lab era óbvio que eu me sentia um completo despreparado. O que, convenhamos, era exagero, mas esse exame pode afetar sua confiança tranquilamente não apenas pela dificuldade inerente, mas pelo peso que carrega. Era quase como se minha carteirinha de hacker fosse cancelada se eu não fosse aprovado nessa porra.

Sem mais acesso ao lab e com alguns emails da Offsec me lembrando que precisava marcar o dia do exame, tomei a decisão que qualquer ansioso tomaria: marquei para o último dia possível, 9 de junho. Ainda era 5 de março então achei que poderia esquecer da OSCP, me convencer de que não era grande coisa e seguir com a vida normal. Não façam isso. Tirar uma folga de umas 2 semanas para descansar a cabeça é ok, principalmente se você estava rushando pelos labs (90 dias pode ser muito pouco para a maioria), mas qualquer pessoa sã iria sugerir que a prova fosse feita o mais cedo possível porque é bom estar com o conteúdo fresquinho na mente.

Três meses depois lá estava eu, mentalmente abalado mas, de acordo com a equipe de psicólogos que me acompanhava, supostamente preparado. Marquei o inicio do exame para as 21 horas porque, como um bom morcego de computador, sabia que meu cérebro estaria no auge as 02:00 e conseguiria manter o ritmo até o amanhecer sem problemas. Eu não tinha planos para dormir, mas me prometi que faria intervalos regulares de pelo menos 1 hora para ir tomar uma água e respirar outro ar que não fosse do quarto.

Quando o proctor (o carinha, ou a carinha, que nos acompanha durante todo exame) falou comigo, me dei conta que não sabia mais falar inglês e tive que recorrer ao tradutor. Passei umas boas 2 horas para me acostumar que havia alguém me olhando na webcam, vendo minha tela e julgando cada comando errado que eu tentava rodar!

Ou seja, o começo foi uma merda. Eu ainda não sabia, mas a primeira máquina que escolhi atacar seria a única que no fim do dia eu não conseguiria nenhum acesso. Recorri a minha estratégia de não perder muito tempo batendo a cabeça e troquei de alvo. Antes do amanhecer eu tinha ownado as outras duas máquinas standalone. Meu plano era não depender do AD porque, na minha cabeça, eu ainda era um completo noob e que iria falhar com toda certeza caso tentasse. Então voltei a máquina impossível e fiquei por lá até quase umas 6 da manhã.

Após 3 horas eu estaria completando 12 horas, 50% do tempo do exame, e aí precisei decidir: passar mais tempo em uma única máquina que, caso eu conseguisse hackear, me daria os pontos 60 que precisava (com mais 10 dos exercicios e labs e eu teria os 70 da aprovação), ou olhar para o AD, com suas 3 máquinas que só me dariam pontos (40, o que me daria 90 pontos no total) se eu ownasse as três?

Puta que pariu. Parte de mim queria me convencer que era impossível que, das 6 da manhã até as 9 da noite, eu não conseguiria hackear aquela única máquina. Mas outra parte me disse que eu precisava dar uma olhadinha naquele AD. Poderia não ser o monstro que eu imaginava. E se eu batesse na trave, falhando no passo final do AD, poderia me contar a história de que ownei quase uns 70% das máquinas do exame e que talvez não fosse um completo inútil. Que a forma da Offsec avaliar é injusta e bla bla bla. Coisa que todo mundo sabe, mas ainda assim seguimos permitindo que essa seja a certificação mais conceituada do mercado. Somos humanos, fazemos coisas que não faz sentido e gostamos de nos sentir especiais.

Meu cérebro ainda estava incrivelmente fresco, apesar da noite em claro. Então fui tentar a sorte com o AD. Rapidinho peguei um primeiro acesso mas apanhei um pouco para escalar privilégios. Fui na segunda, consegui acesso mas parecia que dessa vez a única coisa que eu iria escalar seria a varanda do apartamento e me jogar.

Tentei não deixar a frustração tomar conta. Era só uma prova. Ironicamente, não provava muita coisa. Não provava meu valor, ou falta dele, como hacker ou qualquer outra coisa. Fiz mais um dos muitos intervalos, tomei bastante água, comi um doce porque li em algum lugar que a glicose ajudaria cérebro a pensar melhor, larguei o AD e voltei para a máquina impossível.

Consegui alguma coisa? Óbvio que não (até porque já dei o spoiler que não iria conseguir essa máquina). Acho que era umas 10 da manhã quando me joguei no sofá e pisquei os olhos só um pouco devagar e logo já tinham passado 30 minutos. Lavei o rosto e voltei para o computador. 20 minutos depois eu era Domain Admin. O reino do AD havia caído em minhas mãos. Eu não era tão lammer assim. 

Nessa energia assim que peguei domain admin (aumente o volume):
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/5SMPVY8UHps" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

De um momento para outro, a certificação OSCP era boa, a Offsec, criando o formato maratona psicológica, estaria nos testando em um ambiente de pressão. Se em 48 horas o cara conseguisse hackear umas máquinas e ainda entregar um relatório coerente, que estrago ele não faria com o prazo de 2 semanas? Tudo fazia sentido. Eu era um hacker especial.

São engraçadas as histórias que nos contamos para nos confortar ou para acariciar o ego, não?

Você deve achar que a partir desse momento eu era só alegria.

Mentira. Durou uns bons minutos, mas logo comecei a criar uma paranoia de que ia reprovar porque não preenchi o relatório direito. Larguei mão da outra máquina que faltava e comecei a coletar metodicamente todas as evidências necessárias para ter um relatório perfeito. Antes das 24 horas totais do exame eu já tinha um rascunho bem adiantado.

No meio da tarde ainda dormi por mais uns 30 minutos mas ainda estava muito ansioso por causa do relatório, então voltei ao computador.

Fim do exame, as 21 do dia seguinte, larguei o relatório basicamente pronto. Quase não consegui dormir então ainda fui jogar vídeo game para baixar a adrenalina. 

Eu juro que não usei nenhum produto químico. Acredito que o misto da ansiedade, euforia e vontade fizeram meu sono desaparecer num determinado grau que eu nunca havia visto no meu eu sóbrio.

No dia seguinte corri para o relatório. O revisei e fiquei chocado ao encontrar erros. Li e reli umas 6 vezes e quando, na penúltima vez, ainda encontrei um pequeno detalhe incorreto, quase surto. Reprovar por causa do relatório é foda, né?

Enfim mandei aquela porra e tentei aceitar que havia acabado. Estava nas mãos do revisor. Mas não ache que isso trouxe alguma paz. Eu fiquei com o sentimento claro de que havia algo extremamente errado com meu relatório e que eu não iria passar. Mas contar a história de que reprovei por causa de algum detalhe que meu carrasco revisor resolveu encrespar era melhor do que a história de que eu não havia conseguido pontos suficientes.

Meu sofrimento durou pouco, menos de 48 horas depois recebi o famoso email de congratulações. Eu havia sido aprovado neste caralho.

Minha experiência não foi o exemplo mais brilhante e não caberia num post estilo coach para ir ao linkedin, mas espero que prove um ponto importante: faça essa merda do seu jeito. Eu li tudo que encontrei sobre a experiência dos outros e reconheço que há conselhos bons por aí, mas se eu não tivesse feito do meu jeito talvez não tivesse sido bem sucedido. Não há receita de bolo. Ainda é possível que no dia de exame você seja amaldiçoado e pegue máquinas que sejam feitas com base nos seus pontos fracos. E aí não tem o que fazer. Hacking é baseado nos detalhes e tem vezes que você conhece 99 deles mas no dia da prova a máquina vai te cobrar o detalhe número 100. Não esqueça de dar seu devido valor e reconhecer seus méritos. É só uma prova. Ela não vai provar seu valor profissional ou pessoal, isso aí quem define é você. Ou não.

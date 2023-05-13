---
layout: post
title: Pwncollege - hackeando e aprendendo
author: obrerodrigues
categories: [Hacking]
tags: [estudo, exploits]
---

Enquanto tento sobreviver a pandemia no meu lockdown solitário, ando usando o tempo livre para estudar e hackear umas coisas. Não é como se antes eu já saísse de casa, mas agora há uma desculpa aceitável socialmente.

E foi em meio a andanças pela internet na busca por algum material de estudo sobre exploitation e engenharia reversa que encontrei, mas ou menos na terceira página do Google usando uma keyword que não me recordo o [https://pwn.college/](https://pwn.college/). 

Quem já leu alguma coisa que escrevi sabe que de vez em quando consigo hacker uma coisa [aqui](https://brerodrigues.github.io/ctfs/combo-chain-lite-write-up) e [ali](https://brerodrigues.github.io/ctfs/favorites/rev01-bh-hackaflag2019-write-up), mas nem sempre me sinto satisfeito com meu desempenho e culpo bastante a falta de conhecimento para se fazer uma boa engenharia reversa ou explorar um overflow de maneiras criativas, que vão além do tradicional. E sinto que esse curso poderia me dar essa mão.

O material faz parte do Computer Systems Security course, CSE466, da Universidade Estadual do Arizona, nos EUA. Foi criado e é ministrado por [Zardus](https://www.yancomm.net/) e [kanak](https://connornelson.com/), esses caras faziam/fazem parte do time de CTF [Shellphish](https://shellphish.net/) e se você joga CTFs há algum tempo deve conhecer que esse é um dos times mais tops por aí. Ficaram desde 2011 entre os 10 primeiros do [CTFtime](https://ctftime.org/team/285) e desde 2015 entre os 4 primeiros.

Sabendo das credenciais dos caras por trás do negócio eu me empolguei. Tava em busca exatamente de um material como esse. Um material que me ajudasse a fortalecer bem as bases do meu conhecimento.

Achei todo o conteúdo muito foda. As aulas foram streamadas no twitcher mas estão no YouTube. Não sou fã de vídeo-aulas. Prefiro o material escrito. Mas há boas exceções, e esse cursinho é uma delas. Minha metodologia é a mais básica e óbvia: assisto as aulas, faço umas anotações do que julgo digno de ser anotado e parto para os challenges. Tem uma caralhada de challenges e até uma infra estrutura própria para a galera treinar em: [https://cse466.pwn.college/](https://cse466.pwn.college/)

Os challs são organizados de uma forma interessante. Primeiro eles tem uma versão “teaching”, que tenta te dar uma luz de como as coisas tão funcionando e te da dicas de como explorar. Por exemplo, os de engenharia reversa dizem o que estão fazendo com o input inserido e mostram o resultado que em seguida é comparado com o resultado esperado, que também é exibido. Já os de shellcode te falam quais constraints tão botando para te obrigar a ser criativo. Em seguida tem a versão do challenge “testing” que costuma ser semelhante, e em uns casos iniciais iguais, a versão “teaching”, mas com a diferença de não te falarem nada para ajudar na exploração. Curti essa ideia. É tipo resolver um problema com o professor e em seguida pegar um problema mais difícil para praticar.

Um porém, para a galera totalmente iniciante, é que no curso se supõe que você já saiba alguma coisa de engenharia da computação, tipo um certo conforto com linguagem de programacao, linha de comando e como os computadores funcionam. Caso ainda queira se arriscar, eles tem até um pequeno módulo de fundamentos que deve ser consumido antes do curso principal.

E, claro, as aulas vão ajudar a entender o conceito geral e resolver os desafios iniciais, mas cada desafio seguinte vai te cobrar a ponto de ser necessário vagar pela internet e tentar várias soluções, a resposta pronta não vai estar nos vídeos. Como qualquer livro ou curso, nunca vai ser possível ensinar tudo. Com a teoria e vontade é possível aprender além do que tem nas aulas matando os challenges mais difíceis.

Pode ser um bom projeto para 2021, não?  Tô me divertindo bastante, principalmente nos challs de engenharia reversa e shellcode. Tô apanhando nos de sandbox porque sou noob mas tô tentando. Ainda não cheguei nos módulos de corrupção de memória e exploração em si, mas estou ansioso.

Se você se interessou e vai se arriscar, da uma chegada lá no discord do curso. Sempre tem alguém on-line disposto a ajudar. Caso deseje, meu contato do telegram tá na página inicial, é só mandar mensagem que sofro  junto na resolução desses queridos desafios.

---
layout: home
permalink: /
permalink_name: /home
title: Hello, friend

detail_image: assets/site-logo.png

---
Eu sei. Eu também quase esqueci que nos dias de hoje as pessoas ainda escrevem conteúdo para a internet.

Mesmo assim, nos tempos de vlogs, tutorias coloridos do youtube, tiktokers, instagramers e conteúdo gerado por IA, uma vez ou outra apareço para contar algo sobre algumas [hackinagens](https://brerodrigues.github.io/hacking/), [CTF’s](https://brerodrigues.github.io/ctfs) que participo (muitos deles com o time do qual faço parte, o [RATF](https://ctf-br.org/wiki/ratf/)) ou [qualquer outra bobagem](https://brerodrigues.github.io/rant) que desperte meu interesse.

Antes de tudo, quero avisar que não sou nenhum 1337 h4x0r do caralho de asas. Pode esperar que irei falar merda muitas vezes, mas aceito de boas sugestões que solucionem o problema de forma mais bela ou que corrijam minha noobice ;)

Também não leve porra nenhuma do que eu fale a sério. Não estou por aqui tentando sustentar alguma identidade ou escrever para me exibir. Se quisesse fazer isso estaria no LinkedIn.

Não sabe por onde começar? Dá uma olhada nos meus textos favoritos: [https://brerodrigues.github.io/favorites](https://brerodrigues.github.io/favorites). Ou escolhe um dos mais recentes:

{% for post in site.posts offset:0 limit:3 %}
[{{ post.title }}]({{ site.url }}{{ post.url }}) - **{{ post.date | date: "%b %-d, %Y" }}**
{% endfor %}

Se gosta do que escrevo, possivelmente pode gostar do que leio. [Aqui](https://brerodrigues.github.io/books) mantenho uma lista dos livros que li e curti.

E para falar comigo basta usar o [twitter](https://twitter.com/obrerodrigues) ou abrir uma [issue](https://github.com/brerodrigues/brerodrigues.github.io/issues/new) nesse repositorio com a label *comment*.

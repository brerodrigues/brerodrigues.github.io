---
layout: post
title: SSH phishing
date: 2024-01-06 19:42
author: obrerodrigues
comments: true
categories: [Hacking]
tags: [ssh, phishing, tools]
---

## O que é

Este pequeno script Python é capaz de simular um servidor SSH e, ao receber uma tentativa de login, registra as credenciais inseridas pelo usuário desavisado. Trata-se de um clássico ataque de phishing, mas, ao invés de uma página falsa, aqui temos um servidor SSH falso.

## Motivação

Há alguns anos, meus antigos colegas de trabalho tinham o hábito de sempre me pedir o endereço de um certo servidor SSH. Não consigo me recordar da razão pela qual ninguém tinha esse endereço salvo ou algo assim. A única coisa que lembro é de pensar: esses caras se conectam a qualquer coisa que eu mandar. Se eu enviar um servidor qualquer, nenhum deles perceberia, e eu poderia roubar suas credenciais, e ter a sensação de que era mais esperto que o resto do mundo.

Fui ao Google e me surpreendi por não ter encontrado nenhuma ferramenta ou pedaço de código que fizesse o que vislumbrei. Então, decidi fazer tudo com minhas próprias mãos.

## Limitações

O ataque tem umas limitações bem bobas, como a de que, se o script não for configurado com a chave privada do servidor original, quando a vitima tentar se conectar vai receber um aviso enorme sobre a identidade do servidor. E qualquer pessoa deveria se assustar e se perguntar o que está acontecendo antes de inserir seu usuário e senha.

![](https://raw.githubusercontent.com/brerodrigues/brerodrigues.github.io/main/assets/powershell-ssh-remote-host-identification-has-changed.png) (imagem copiada direto de https://elbruno.com/2020/01/27/raspberrypi-how-to-solve-the-ssh-warning-warning-remote-host-identification-has-changed/)

Outra limitação é que a vítima não conseguirá ter acesso ao servidor original enquanto estiver tentando fazer login no servidor falso. Acredito que seja possível redirecioná-la para o original, mas não estudei a fundo essa possibilidade porque queria algo simples e rápido de codificar.

## O script

O código é extremamente simples e utiliza o [Paramiko](https://www.paramiko.org/) para realizar todo o trabalho pesado de comunicação SSH. A documentação é fácil de entender, e tudo que eu precisava estava nessa [ServerInterface](https://docs.paramiko.org/en/latest/api/server.html#paramiko.server.ServerInterface). O resto foi sendo copiado de exemplos da internet ou na base da tentativa e erro. Na época que escrevi esse código, ainda não existia ChatGPT e todos nós programávamos como selvagens, lendo documentações e vários snippets do Stack Overflow.

O script pode ser encontrado neste repositório: [ssh_phishing](https://github.com/brerodrigues/ssh_phishing). No README, você pode encontrar uma documentação com tudo que é necessário para fazer o script funcionar e um pequeno exemplo de como as coisas acontecem.

## Conclusão

No final do dia, após uma tarde hackeando para fazer esse código funcionar do jeito que queria, percebi que a ideia de comprometer as credenciais dos meus colegas de trabalho era boba. O que eu poderia fazer? Commitar nos nossos repositórios códigos piores do que eles já escreviam sozinhos? Ser juvenil e trocar seus papéis de parede por algo obsceno?

Fui dormir tranquilo sabendo que tinha o poder, mas que não iria usá-lo. Afinal, se eu tivesse um advogado, ele me aconselharia a dizer que fazer isso seria eticamente questionável. E que você não deve fazer o mesmo. E caso o faça, é por sua conta e risco. No README do script, existe um gigante aviso que você deve seguir.





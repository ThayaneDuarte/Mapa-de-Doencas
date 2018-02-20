# Mapa de Doenças

Trabalho realizado para a disciplina LAB Engenharia de Software(1/2017).

### Instalação/Implantação

Mapa de Doenças necessita de django 1.9.4 e geopy 1.11.0 para seu funcionamento.

### Instalar o Virtualenv
Primeiramente é necessário a intalação do virtualenv. O Virtualenv é um construtor de ambiente python, usado para criar ambientes python isolados. Para instalá-lo, se não tiver no servidor, digite:  
```sh
$ pip install virtualenv
```
### Criar um Ambiente Virtual
Após o passo 1, usa-se o comando virtualenv para criar um novo ambiente com python3 como versão python padrão.  Abra um terminal na pasta em que deseja manter o software e digite:

```sh
$ virtualenv --python=python3 env
```
Nota:
  - python = python3 é um arquivo binário para o python 3.
  - env é o nome do ambiente.

### Ativar o Ambiente Virtual
Agora com o ambiente virtual criado e configurado, ative-o com o comando:
```sh
$ source env/bin/activate
```
### Instalar o pip3
Cheque a versão do pip com o comando:
```sh
$ pip3 -v
```
Ele deverá estar instalado, caso contrário, instale-o com o comando:
```sh
$ apt-get install python3-pip
```
### Instalar o Django
Agora instale o django, que é o framework usado pelo sistema mapa de doenças.
```sh
$ pip3 install django==1.9
```

### Baixar o Sistema
Com todo o ambiente virtual configurado, resta colocar o sistema na pasta raíz (atual), digitando:
```sh
$ git clone https://github.com/ThayaneDuarte/Mapa-de-Doencas.git
```
### Configurar o Domínio
Para configurar o domínio, ou seja qual IP o sistema irá usar, acesse o arquivo settings.py na pasta mapadoencas. 
```sh
e.g.) gedit Mapa-de-Doencas/mapadoencas/settings.py 
```
E acrescente o IP e DNS em ALLOWED_HOSTS
```sh
e.g.) ALLOWED_HOSTS = [‘www.mapadoencas.com.br’, ‘meu_IP’]
```
### Executar o Sistema
Para executar o sistema, entre na pasta que contém o arquivo manager.py
```sh
$ cd Mapa-de-Doencas
```
e digite
```sh
$ ./manager runserver <meu_IP>
```
por padrão o sistema responderá na porta 8000, mas isto pode ser mudado ao digitar o seguinte comando em vez do supracitado:
```sh
$ ./manager runserver <meu_IP>:<minha_porta>
```
#### Acessando o Sistema
Se não tiver um DNS associado ao ip do sistema, digite <meu_IP>:<minha_porta> na barra do navegador.
Caso tenha um DNS, digite-o seguido da porta
```sh
e.g.) www.mapadoencas.com.br:<minha_porta>
```
Se quiser tirar a obrigatoriedade de digitar a porta após o endereço, deve-se configurar o servidor para enviar todas as solicitações que cheguem para a porta escolhida. 
 

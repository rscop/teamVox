# [Team Vox!](https://igorjosemaule.wixsite.com/zenviavox)
![Vox_logo-cor.png](https://static.wixstatic.com/media/a41da5_072e57945e2346579e6bbdb37994f8e3~mv2.png/v1/fill/w_226,h_99,al_c,q_85,usm_0.66_1.00_0.01/Vox_logo-cor.webp)
![vox_tagline.png](https://static.wixstatic.com/media/a41da5_002ab44972b847768b1c0eaa07ce8a80~mv2.png/v1/fill/w_600,h_20,al_c,q_85,usm_0.66_1.00_0.01/vox_tagline.webp)
A VOX é uma startup social com o propósito de garantir experiências de compras positivas para todas as pessoas, independente de suas individualidades.

Contamos com o apoio de tecnologias e inovação para facilitar a jornada de compra de deficientes visuais. Acreditamos que podemos fazer a diferença.

Se você chegou até aqui é porque você também tem vontade de fazer a diferença no mundo, assim como nós :D
Aqui você pode encontrar uma pequena documentação de como configurar o Oio, o nosso mascotezinho.

# Arquivos

Antes de começarmos, existem alguns arquivos que você precisa criar ao dar o pull do repositório:

> webservice.py.cfg

    [production]
    
    listen_ip = (IP do servidor, ou pode deixar 0.0.0.0)
    
    listen_port = (Porta aberta no servidor)
    
    files_path = (Pasta onde ficaram salvos os arquivos usados para enviar text-to-speech)
    
    logfile = (Path de onde estará seu arquivo de logs)
    
    logfile_backup_count = (Número máximo de logs simultaneos)
    
    log_level = (O que será logado no arquivo 'debug')
    
    log_mode = (Modo de funcionamento do log)

> webservice.py.env

    [production]
    SECURE_STRING = (Aqui entra a sua secure-string da zenvia)
    X_API_TOKEN = (Aqui o seu token de acesso da zenvia)
    URL_FOR_FILE = (Aqui você precisa colocar a url:prota ou ip:porta do seu servidor)
      
    DB_URL = (URL do seu MySql)
    DB_PORT = (Porta do banco, por padrão: 3306)
    DB_USER = (Usuário do Banco)
    DB_PASS = (Senha de acesso do usuário)
    DB_NAME = (Nome do banco de dados utilizado)

## Modulos utilizados

 - PIP3
 - Flask
 - Flash_sqlalchemy
 - Flask_httpauth
 - passlib
 - configparser
 - logging
 - mysql-connector-python
 - requests SecretStorage
 - Unidecode
 - difflib
 - urllib3
 - json
 ## Instalação
 Após você ter preparado o ambiente, será necessário, também, configurar sua conta na plataforma da Zenvia, inserindo o dominio em **Message Webhook URL**
 
Também é necessário a criação da infraestrutura do banco de dados.

Após isso, basta executar :

> python webservice.py

### Todo:
 - Documentação
 - Processo de instalação
 - API de integração
 - Dump do Mysql


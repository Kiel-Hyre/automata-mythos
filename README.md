## About Mythos
Mythos is a compiler created by ArrayIndexOutOfBoundsException. A project for
the course Automata of CS in PLM

## Requirements
* [pip3](https://www.python.org/)
* [virtualenv](https://pypi.org/project/virtualenv/)
* [vue-cli](https://cli.vuejs.org/guide/installation.html)
* [django](https://pypi.org/project/Django/)


## Setup
* Virtual Environment

1. Use virtualenv to add a virtual environment
```
    virtualenv venv
```
2. Activate the environment
```
    source venv/bin/activate  #Ubuntu
    venv/Scripts/active #Windows
```
3. Deactivate enviroment
```
    deactivate
```
4. Remove environment
```
    rm -rf venv
```
Check this [info](https://www.liquidweb.com/kb/how-to-setup-a-python-virtual-environment-on-windows-10/)
for windows

* Install requirements for python3
1. (Optional) Upgrade Tools
```
    pip3 install --upgrade setuptools #pip only for Windows
```
2. (Optional) Upgrade Pip
```
    python3 -m pip install --upgrade pip #python only for Windows unless there is other version
```
3. Install requirements in requirements.txt
```
    pip3 install -r requirements.txt
```

* Environment Variables
1. In source folder aligned with manage.py create **.env** file
```
    automata-mythos\
        ... # other files
        .env
        manage.py
```
2. Create variables inside env file
    1. For development, copy the variables inside the development.env to .env
    2. For production, copy the variables inside the production.env to .env

* Vue init
1. yarn the project
```
    yarn
```
2. yarn build
```
    yarn build
```

* Common Commands for Django

1. Makemigrations
```
    python3 manage.py makemigrations
```
2. Migrate Applications
```
    python3 manage.py migrate
```

3. More django commands [info](https://www.djangoproject.com/)


* Common Commands for Vue

1. Project setup
```
yarn install
```

2. Compiles and minifies for production
```
yarn build
```

3. Compiles and hot-reloads for development
```
yarn serve
```



4. See [Configuration Reference](https://cli.vuejs.org/config/).


## Run Servers

1. Run server for Django
```
    python3 manage.py runserver (port) # default is 8000
```

2. Run server for Vue
```
    yarn serve
```


## Notes
1. Sadly this is two way, so need to run both server seperately
2. In future, maybe use different containers
3. ~~Need to seperate production and development key env~~
4. No other db installed, default sqlite3 but can be upgrade
5. No cron sadly but can be upgrade
6. No automatic reloads unless behavior of default runservers
7. Deploy
8. more fixes
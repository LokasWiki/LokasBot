```

 __                 __                           _______              __
|  \               |  \                         |       \            |  \
| $$       ______  | $$   __  ______    _______ | $$$$$$$\  ______  _| $$_
| $$      /      \ | $$  /  \|      \  /       \| $$__/ $$ /      \|   $$ \
| $$     |  $$$$$$\| $$_/  $$ \$$$$$$\|  $$$$$$$| $$    $$|  $$$$$$\\$$$$$$
| $$     | $$  | $$| $$   $$ /      $$ \$$    \ | $$$$$$$\| $$  | $$ | $$ __
| $$_____| $$__/ $$| $$$$$$\|  $$$$$$$ _\$$$$$$\| $$__/ $$| $$__/ $$ | $$|  \
| $$     \\$$    $$| $$  \$$\\$$    $$|       $$| $$    $$ \$$    $$  \$$  $$
 \$$$$$$$$ \$$$$$$  \$$   \$$ \$$$$$$$ \$$$$$$$  \$$$$$$$   \$$$$$$    \$$$$




```
# Toolforge setup

Toolforge setup and job management

- ### Clone and setup virtual environments
- #### remove old repos and clone new repos and setup permissions
    ``` bash
    rm -fdr $HOME/repos && git clone --recurse-submodules https://github.com/LokasWiki/LokasBot.git $HOME/repos && chmod ug+x $HOME/repos/toolforge/bin/setup-venvs.sh
    ```
- #### run setup-venvs.sh to setup virtual environments
    ``` bash
    toolforge-jobs run setup-venvs --command $HOME/repos/toolforge/bin/setup-venvs.sh --image tf-python39
     ```
- #### to check setup-venvs.sh logs (bot setup will finish when see "====\end setup lokas-bot-scripts\n=====" in logs)
  ``` bash
  tail -f $HOME/setup-venvs.*
  ```
  - #### set permissions for all files in repos directory
   ``` bash
   chmod -R ug+x $HOME/repos/*
  ```
- ### copy user-config.py and user-password.py  from home to repos directory
    ``` bash
    cp $HOME/user-config.py  $HOME/repos
    cp $HOME/user-password.py $HOME/repos
    ``` 
- ### to run bot on **many servers** (Load jobs)
- #### for server one  (maintenance and webcite)
    ``` bash  
    toolforge-jobs load $HOME/repos/toolforge/cronjobs1.yaml
    ```

- #### for server two (requests and statistics)
    ``` bash
    toolforge-jobs load $HOME/repos/toolforge/cronjobs2.yaml
    ```
- ### to run bot on **one server** (Load jobs)
    ``` bash
    toolforge-jobs load $HOME/repos/toolforge/cronjobs.yaml
    ```


- ### run job for one time (timed out 300 seconds)
    ```` bash
    toolforge-jobs run script --command $HOME/repos/toolforge/jobs/statistics-daily.sh --image tf-python39 --wait
    ````


- ### run job for one time (without timed out)
    ```` bash
    toolforge-jobs run script --command $HOME/repos/toolforge/jobs/statistics-daily.sh --image tf-python39
    ````


- ### run tool-bot on web
  https://github.com/LokasWiki/LokasBot-web

<hr>

# خطوات تثبيت البوت علي الجهاز المحلي

- ### تثبيت إطار العمل والمكتبات الأساسية والبايثون
  https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation#Install_Python
- ### تثبيت mediawiki
    ```
    # MediaWiki with MariaDB
    #
    # Access via "http://localhost:8080"
    #   (or "http://$(docker-machine ip):8080" if using docker-machine)
    version: '3'
    services:
            mediawiki:
                    image: mediawiki
                    restart: always
                    ports:
                            - 8080:80
                    links:
                            - database
                    volumes:
                            - images:/var/www/html/images
                            # After initial setup, download LocalSettings.php to the same directory as
                            # this yaml and uncomment the following line and use compose to restart
                            # the mediawiki service
                            - ./LocalSettings.php:/var/www/html/LocalSettings.php
            # This key also defines the name of the database host used during setup instead of the default "localhost"
            database:
                    image: mariadb
                    restart: always
                    environment:
                            # @see https://phabricator.wikimedia.org/source/mediawiki/browse/master/includes/DefaultSettings.php
                            MYSQL_DATABASE: my_wiki
                            MYSQL_USER: wikiuser
                            MYSQL_PASSWORD: example
                            MYSQL_RANDOM_ROOT_PASSWORD: 'yes'
                    volumes:
                            - db:/var/lib/mysql

    volumes:
            images:
            db:
    ```
     أو تنزيل النسخة وتثبيتها يدويا من [هنا](https://www.mediawiki.org/wiki/Download)

- ### الاتصال بقاعدة البيانات
    ```
    ssh -N -L 4711:arwiki.analytics.db.svc.wikimedia.cloud:3306 yourusername@logintoolforge.org -i /home/username/.ssh/filename_id   -v
    ```


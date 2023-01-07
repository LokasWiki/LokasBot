# خطوات تثبيت البوت علي الجهاز المحلي
## تثبيت إطار العمل والمكتبات الأساسية والباثون 
https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation#Install_Python
## تثبيت mediawiki
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
 
 ## الاتصال بقاعده البيانات 
```
ssh -N -L 4711:arwiki.analytics.db.svc.wikimedia.cloud:3306 yourusername@login.toolforge.org -i /home/username/.ssh/filename_id   -v
```
 

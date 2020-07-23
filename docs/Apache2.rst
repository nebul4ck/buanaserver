Apache2
#######

Reprepro needs a webserver to publicates the repository. We will use Apache2 + wsgi_mod, also We going to implement SSL/TLS comunications, BasicAuth (User/Passwd) and User Digital Certificate for authentication. 

Install
*******

.. code:: console

  # apt-get install apache2
..

Global and basic configuration
******************************

File global config
==================

.. code:: console

  # vi /etc/apache2/apache2.conf
    Mutex file:${APACHE_LOCK_DIR} default

    ServerSignature Off
    ServerTokens Prod

    PidFile ${APACHE_PID_FILE}
    Timeout 300
    KeepAlive On
    MaxKeepAliveRequests 100
    KeepAliveTimeout 5
    User ${APACHE_RUN_USER}
    Group ${APACHE_RUN_GROUP}
    HostnameLookups Off
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    LogLevel warn

    IncludeOptional mods-enabled/*.load
    IncludeOptional mods-enabled/*.conf

    Include ports.conf


    <Directory /usr/share>
        AllowOverride None
        Require all granted
    </Directory>

    <Directory /var/www/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    #<Directory /srv/>
    # Options Indexes FollowSymLinks
    # AllowOverride None
    # Require all granted
    #</Directory>

    AccessFileName .htaccess

    <FilesMatch "^\.ht">
        Require all denied
    </FilesMatch>

    LogFormat "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
    LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %O" common
    LogFormat "%{Referer}i -> %U" referer
    LogFormat "%{User-agent}i" agent

    IncludeOptional conf-enabled/*.conf
    IncludeOptional sites-enabled/*.conf
..

Virtual Host :80
================

**IMPORTANTE** Actualmente los SITES de Apache se crean solo con el paquete buanaserver.deb. Los siguientes sites son tan solo orientativos.

.. code:: console

  # vi /etc/apache2/sites-available/001-buanarepo-http.conf

  <VirtualHost *:80>

      ServerAdmin nebul4ck@localhost
      ServerName buanarepo.nebul4ck.es
      ServerAlias www.buanarepo.nebul4ck.es

      DocumentRoot /srv/buanarepo-repo/
      RedirectMatch ^/$ /ubuntu
      Redirect "/" "https://buanarepo.nebul4ck.es/"

      ErrorDocument 404 /etc/apache2/buanarepo/custom_404.html
      ErrorDocument 500 /etc/apache2/buanarepo/custom_50x.html
      ErrorDocument 502 /etc/apache2/buanarepo/custom_50x.html
      ErrorDocument 503 /etc/apache2/buanarepo/custom_50x.html
      ErrorDocument 504 /etc/apache2/buanarepo/custom_50x.html

      Alias /ubuntu /srv/buanarepo-repo/ubuntu
      <Directory /srv/buanarepo-repo/ubuntu/>
          Options +Indexes
          AllowOverride None
          AuthType basic
          AuthName "Authentication Required for nebul4ck-org Repo"
          AuthUserFile "/etc/apache2/buanarepo/.saturnaccount"
          Require valid-user
      </Directory>

      <Directory /srv/buanarepo-repo/*/conf>
          Options -Indexes
          AllowOverride None
          Require all denied
      </Directory>

      <Directory /srv/buanarepo-repo/*/db>
          Options -Indexes
          AllowOverride None
          Require all denied
      </Directory>

  </VirtualHost>
..

**Testing config...**

.. code:: console

  # apache2ctl configtest
..

Enable HTTP site
------------------

.. code:: console

  # a2ensite 001-buanarepo-http.conf
..

**Deactivate Default HTTP site**

.. code :: console

  # a2dissite 000-default.conf
..

Owner and directories
---------------------

.. code:: console

  # mkdir /etc/apache2/buanarepo
  # chmod 775 /etc/apache2/buanarepo
  # echo "<h1 style='color:red'>Error 404: Not found :-(</h1>" | sudo tee /etc/apache2/buanarepo/custom_404.html
  # echo "<p>I have no idea where that file is, sorry.  Are you sure you typed in the correct URL?</p>" | sudo tee -a /etc/apache2/buanarepo/custom_404.htm
  # echo "<h1>Oops! Something went wrong...</h1>" | sudo tee /etc/apache2/buanarepo/custom_50x.html
  # echo "<p>We seem to be having some technical difficulties. Hang tight.</p>" | sudo tee -a /etc/apache2/buanarepo/custom_50x.html
..

Buanarepo Apache2 site :8081
============================

BuanaServer API listen on 8081 port. The conexions are over HTTPS and will be need a client User/Passwd in buanaclient site (take a look buanaclient doc).

.. code:: console

  # vi /etc/apache2/sites-available/000-buanarepo-api.conf
  Listen 8081

  <VirtualHost *:8081>

      ServerName buanarepo.nebul4ck.es
      ServerAlias www.buanarepo.nebul4ck.es
      ServerAdmin buanarepo@localhost

      RedirectMatch ^/$ "/get/info"

      ErrorDocument 404 /etc/apache2/buanarepo/custom_404.html
      ErrorDocument 500 /etc/apache2/buanarepo/custom_50x.html
      ErrorDocument 502 /etc/apache2/buanarepo/custom_50x.html
      ErrorDocument 503 /etc/apache2/buanarepo/custom_50x.html
      ErrorDocument 504 /etc/apache2/buanarepo/custom_50x.html

      SSLEngine on
      SSLCertificateFile "/etc/apache2/ssl/buanarepo.nebul4ck.es.crt"
      SSLCertificateKeyFile   "/etc/apache2/ssl/buanarepo.nebul4ck.es.key"

      RewriteEngine On
      RewriteCond %{HTTPS} off
      RewriteRule (.*) https://%{SERVER_NAME}/$1 [R,L] 

      <FilesMatch "\.(cgi|shtml|phtml|php)$">
          SSLOptions +StdEnvVars
      </FilesMatch>

      <Directory /usr/lib/cgi-bin>
          SSLOptions +StdEnvVars
      </Directory>

      WSGIDaemonProcess buanarepo user=buanarepo group=buanarepo processes=2 threads=15\
      python-path=/opt/buanarepo

      WSGIScriptAlias / /opt/buanarepo/api.wsgi
      # Enable Basic Auth in API's (Flask-HTTPAuth)
      WSGIPassAuthorization On

      <Directory "/opt/buanarepo/">
          WSGIProcessGroup buanarepo
          <Files api.wsgi>
              Require all granted
          </Files>
      </Directory>

      ErrorLog ${APACHE_LOG_DIR}/error.log
      CustomLog ${APACHE_LOG_DIR}/access.log combined

  </VirtualHost>
..

**Testing config...**

.. code:: console

  # apache2ctl configtest
..

Activate API site
-----------------

.. code:: console

  # a2ensite 000-buanarepo-api.conf
..

BasicAuth (User/Passwd)
***********************

Uncomment AuthType, AuthName, AuthUserFile and Require, to force user and password login.

You must create a Apache user for login:

.. code:: console

  # htpasswd -c /etc/apache2/buanarepo/.saturnaccount <user>
  passwd: <passwd>

  # chown root:www-data -R /etc/apache2/buanarepo/
  # chown root:www-data /etc/apache2
..

SSL/TLS comunications
*********************

For encrypt the communications We need a server.crt and server.key, In below section We going to create a PKI for Auto-sign some certificates.

Now, We going to configure SSL/TLS communications:

.. code:: console

  # vi /etc/apache2/conf-available/ssl-params.conf
  # Recommendations by Remy van Elst on the Cipherli.st
  SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
  SSLProtocol All -SSLv2 -SSLv3
  SSLHonorCipherOrder On
  # Disable preloading HSTS for now.  You can use the commented out header line that includes
  # the "preload" directive if you understand the implications.
  #Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains; preload"
  Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains"
  Header always set X-Frame-Options DENY
  Header always set X-Content-Type-Options nosniff
  # Requires Apache >= 2.4
  SSLCompression off 
  SSLSessionTickets Off
  SSLUseStapling on 
  SSLStaplingCache "shmcb:logs/stapling-cache(150000)"
  SSLOpenSSLConfCmd DHParameters "/etc/ssl/certs/dhparam.pem"
..

**Enable SSL-params**

.. code:: console

  # a2enconf ssl-params
..

Create HTTPS site :443
======================

**Note:** if you want use HTTPS first you must uncomment "Redirect" line in 001-buanarepo-http.conf

.. code:: console

  # vi /etc/apache2/sites-available/002-buanarepo-https.conf
  <IfModule mod_ssl.c>
      <VirtualHost *:443>

          ServerAdmin nebul4ck@localhost
          ServerName buanarepo.nebul4ck.es
          ServerAlias www.buanarepo.nebul4ck.es

          DocumentRoot /srv/buanarepo-repo/
          RedirectMatch ^/$ /ubuntu

          ErrorDocument 404 /etc/apache2/saturn-repo/custom_404.html
          ErrorDocument 500 /etc/apache2/saturn-repo/custom_50x.html
          ErrorDocument 502 /etc/apache2/saturn-repo/custom_50x.html
          ErrorDocument 503 /etc/apache2/saturn-repo/custom_50x.html
          ErrorDocument 504 /etc/apache2/saturn-repo/custom_50x.html

          SSLEngine on
          SSLCACertificateFile    "/etc/apache2/ssl/buanaCA.crt"
          SSLCertificateFile      "/etc/apache2/ssl/buanarepo.nebul4ck.es.crt"
          SSLCertificateKeyFile   "/etc/apache2/ssl/buanarepo.nebul4ck.es.key"

          <FilesMatch "\.(cgi|shtml|phtml|php)$">
              SSLOptions +StdEnvVars
          </FilesMatch>

          <Directory /usr/lib/cgi-bin>
              SSLOptions +StdEnvVars
          </Directory>

          <LocationMatch ^/ubuntu/.*/Packages$>
              Require all granted
              SSLVerifyClient none
          </LocationMatch>

          Alias /ubuntu /srv/buanarepo-repo/ubuntu
          <Directory /srv/buanarepo-repo/ubuntu/>
              Options +Indexes
              SSLVerifyClient require
              SSLVerifyDepth 1
              SSLRequireSSL
              AllowOverride None
              AuthType basic
              AuthName "Authentication Required for nebul4ck-org Repo"
              AuthUserFile "/etc/apache2/buanarepo/.saturnaccount"
              Require valid-user
          </Directory>

          <Directory /srv/buanarepo-repo/*/conf>
              Options -Indexes
              AllowOverride None
              Require all denied
          </Directory>

          <Directory /srv/buanarepo-repo/*/db>
              Options -Indexes
              AllowOverride None
              Require all denied
          </Directory>

          BrowserMatch "MSIE [2-6]" \
              nokeepalive ssl-unclean-shutdown \
              downgrade-1.0 force-response-1.0

      </VirtualHost>
  </IfModule>
..

**Check config**

.. code:: console

  # apache2ctl configtest
..

Enable HTTPS site
-----------------

.. code:: console

  # a2ensite 002-buanarepo-https.conf
  # a2dissite default-ssl.conf
..

**Activate SSL and headers modules**

.. code:: console

  # a2enmod ssl
  # a2enmod headers
..

**Note**: remember to create buanarepo-server certs (crt and key) and reload apache2 service. See PKI_ section.

.. _PKI:

Client Certificate Authentication
*********************************

Client Certificate Authentication is a mutual certificate based authentication, where the client provides its Client Certificate to the Server to prove its identity. This happens as a part of the SSL Handshake.

For enable Client Certificate Authentication will be necessary uncomment the next lines in 002-buanarepo-https.conf:

* SSLCACertificateFile
* SSLVerifyClient
* SSLVerifyDepth

And a Client Certificate used by client systems to prove their identity to the remote server.
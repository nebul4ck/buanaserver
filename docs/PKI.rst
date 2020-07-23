Public Key Infrastructure
#########################

PKI is a set of roles, policies, and procedures needed to create, manage, distribute, use, store, and revoke digital certificates and manage public-key encryption. We have a self PKI to generate self CA that will sign the rest of certificates (server and clients).

Certificate Authority (CA)
**************************

.. code:: console

  # cd ~ ; mkdir pki; cd pki
  # openssl genrsa -out buanaCA.key 4096
  # chmod 400 buanaCA.key
  # openssl req -x509 -new -nodes -key buanaCA.key -sha256 -days 7300 -out buanaCA.crt
  ES
  Seville
  Seville
  Nebul4ck Org.
  Nebul4ck Labs
  nebul4ck-org Root CA
  agonzalez@nebul4ck.es

  # chmod 444 buanaCA.crt
  # openssl x509 -noout -text -in buanaCA.crt
..

Config SSL
==========

.. code:: console

  # cd /etc/ssl/
  # cp openssl.cnf openssl-san.cnf
  # vi openssl-san.cnf
  ...
  [req]
  req_extensions = v3_req
  ...
  [ v3_req ]
  basicConstraints = CA:FALSE
  #keyUsage = nonRepudiation, digitalSignature, keyEncipherment
  keyUsage = digitalSignature, keyEncipherment
  subjectAltName = @alt_names

  [alt_names]
  DNS.1 = buanarepo.nebul4ck.es
  DNS.2 = mail.nebul4ck.es
  DNS.3 = buanarepo-lab.nebul4ck.es
  DNS.4 = centralkb.nebul4ck.es
  DNS.5 = buanAPTclient
  ...
  [ CA_default ]
  ...
  copy_extensions = copy
  ...
..

Create BuanaServer Cert
***********************

.. code:: console

  # openssl genrsa -out buanarepo-lab.nebul4ck.es.key 2048
  # openssl req -new -key buanarepo-lab.nebul4ck.es.key -out buanarepo-lab.nebul4ck.es.csr
  ES
  Seville
  Seville
  Nebul4ck Org.
  Nebul4ck Labs
  buanarepo.nebul4ck.es
  agonzalez@nebul4ck.es
  []
  []

  # openssl x509 -req -in buanarepo.nebul4ck.es.csr -CA buanaCA.crt -CAkey buanaCA.key -CAcreateserial -out buanarepo.nebul4ck.es.crt -days 7300 -sha256 -extensions v3_req -extfile /etc/ssl/openssl-san.cnf
..

Create Client Cert
******************

.. code:: console

  # openssl req -newkey rsa:2048 -keyout buanAPTclient.key -out buanAPTclient.csr -nodes -days 7300 -subj "/CN=buanAPTclient"
  # openssl x509 -req -in buanAPTclient.csr -CA buanaCA.crt -CAkey buanaCA.key -out buanAPTclient.crt -set_serial 01 -days 7300 -extensions v3_req -extfile /etc/ssl/openssl-san.cnf
  # openssl pkcs12 -export -clcerts -in buanAPTclient.crt -inkey buanAPTclient.key -out buanAPTclient.p12
  Enter Export Password: <passwd>
  Verifying - Enter Export Password: <passwd>
..

Maybe you would like to work with certificates in webbrowser, in this case you only must import de certificate in your favorite webbrowser

* Firefox: https://www.jscape.com/blog/firefox-client-certificate

Also, you should import the buanaCA.crt in the webbrowser for authenticate the conexion between the client and the remote server.
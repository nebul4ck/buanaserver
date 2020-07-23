Reprepro (File-browser)
#######################
Reprepro is able to manage multiple repositories for multiple distribution versions and one package pool. It can process updates from an incoming directory, copy package (references) between distribution versions, list all packages and/or package versions available in the repository, etc.

Install
*******

In buanaserver:

.. code:: console

  $ ssh root@server
  # apt purge gnupg
  # apt autoremove
  # apt update
  # apt install libarchive13 libgpgme11
..

From source
===========

.. code:: console

  # wget ftp.es.debian.org/debian/pool/main/r/reprepro/reprepro_5.1.1-1_amd64.deb
  # dpkg -i reprepro_5.1.1-1_amd64.deb
..

From Ubuntu Repositories
========================

**Note:** Ubuntu Repositories version of reprepro is older than source.

.. code:: console

  # apt update
  # apt install reprepro
..

Configure
*********

Create buanarepo user
=====================

.. code:: console

  # useradd -d /home/buanarepo -m -k /etc/skel -s /bin/bash -c "Buanarepo User" buanarepo
..

Make directory tree
===================

buanarepo-repo
--------------

Reprepro file browser directory tree:

.. code:: console

  # cd /srv/
  # mkdir -p buanarepo-repo/ubuntu/conf
  # vi buanarepo-repo/ubuntu/conf/distributions
    Origin: Nebul4ck Org.
    Label: Nebul4ck Suit Repo
    Suite: stable
    Codename: xenial
    Version: 16.04
    Architectures: amd64
    Components: main
    Description: Packages for Saturn Suit
    SignWith: yes

  # vi buanarepo-repo/ubuntu/conf/options
    ask-passphrase
    #keepunusednewfiles
    waitforlock 6
    show-percent
    verbose
    basedir /srv/buanarepo-repo/ubuntu

  # mkdir /srv/{buanarepo-debs,buanarepo-build}
  # mkdir /srv/buanarepo-debs/oldRelease
..

buanarepo-build
---------------

Buanarepo needs a directory tree for syncs remote dirs. Into */srv/buanarepo-build*, will be create a directory tree with all directories that won't be create during rsync, **ie**: kafka service has some directories that won't be synchronised (logs, store, data...). You should make theses directories.

.. code:: console

  # cd /srv/buanarepo-build
  # mkdir -p {kafka/DEBIAN,kafka/opt/kafka/logs,kafka/opt/kafka/store,kafka/lib/systemd/system,kafka/opt/c_tools}
  # touch kafka/DEBIAN/{control,prerm,postinst,postrm}
  # chmod -R 775 kafka/DEBIAN
..

buanarepo-debs
--------------

Here are all debian packages (either Git packages or rsync packages)

Create Master GPG key
*********************

**Note:** if you are working in the cloud, is a good idea install and launch *rng-tools* before the keys generation. 

The GPG Key owner will be buanarepo user so you must connect to server with buanarepo user.

.. code:: console

  $ ssh buanarepo@buanarepo-server
  $ sudo apt-get install rng-tools
  $ sudo rngd -r /dev/urandom

  $ sudo apt install gpg2
  $ gpg2 --full-gen-key
  1
  4096
  0
  s
  [your name or company]
  [you email]
  V
  Passphrase: <feel free>
  
  pub   rsa2048/6AD6823C 2018-06-11 [S]
        Huella de clave = 42C4 2DA6 9DD5 5A23 E730  A35A A8D7 4C78 6AD6 823C
  uid         [  absoluta ] Alberto González <agonzalez@nebul4ck.es>
  sub   rsa2048/9C7211BE 2018-06-11 []

  $ gpg2 --edit-key 6AD6823C
  gpg> addkey
  4
  4096
  0
  s
  s
  Passphrase: <empty>

  gpg> save

  $ gpg2 --list-public-keys
  /home/buanarepo/.gnupg/pubring.kbx

  pub   rsa2048/6AD6823C 2018-06-11 [SC]
  uid         [  absoluta ] Alberto González <agonzalez@nebul4ck.es>
  sub   rsa2048/9C7211BE 2018-06-11 [E]
  sub   rsa2048/A23420E4 2018-06-11 [S]

  $ gpg2 --export-secret-key 6AD6823C > ca-buanarepo.key
  $ gpg2 --export 6AD6823C >> ca-buanarepo.key
  $ gpg2 --export 6AD6823C > ca-buanarepo.pub
  $ gpg2 --export-secret-subkeys 7B0AAFF6 > buanarepo.pub
..

**Send PUB KEY to Ubuntu Key Server:**

.. code:: console

  $ gpg2 --keyserver hkp://keyserver.ubuntu.com:80 --send-key 7B0AAFF6
..

**optional:**

.. code:: console

  $ gpg2 --delete-secret-key 6AD6823C
  $ gpg2 --import ca-buanarepo.pub buanarepo.pub
  $ gpg2 --list-secret-keys
..

Configure GNUPG
===============

.. code:: console

  $ vi ~/.gnupg/gpg.conf
  pinentry-mode loopback

  $ vi ~/.gnupg/gpg-agent.conf
  allow-loopback-pinentry
..

Some Reprepro's commands
************************

.. code:: console

  $ reprepro -Vb /srv/buanarepo-repo/ubuntu -S utils -C main includedeb xenial ~/kafka_1.2.1-1_amd64.deb
  $ reprepro -Vb /srv/buanarepo-repo/ubuntu -C main remove xenial kafka
  $ reprepro -Vb /srv/buanarepo-repo/ubuntu deleteunreferenced
..
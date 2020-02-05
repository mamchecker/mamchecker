Archived
========

Google App Engine (GAE) is now Google Cloud Platform (GCP)
and Python 3 is finally supported.

Ndb has been ported to Python 3: https://github.com/googleapis/python-ndb
It uses https://github.com/GoogleCloudPlatform/google-cloud-datastore
which on its turn uses
https://github.com/googleapis/python-firestore.

Conversion and further development is done in: https://github.com/chcko/chcko

- Adapt to changes in used 3rd party packages
- Create an installer using specific versions of 3rd party packages
- Allow using content repos from other github accounts

Purpose
=======

Mamchecker creates and checks exercises programmatically using python over the internet.

``Mam`` comes from ``MAtheMathics``.

Servers
=======

It is available at

- `appspot <http://mamchecker.appspot.com>`_ 

It can be run locally, though, using
`dev_appserver <https://cloud.google.com/appengine/docs/python/tools/devserver>`_, 
which is part of the 
`appengine SDK <https://cloud.google.com/appengine/downloads>`_.

.. code::

    #serves on port :8080
    #from above the repository
    dev_appserver.py mamchecker --host=0.0.0.0

Settings are done via the `GCP console <https://console.cloud.google.com/project/mamchecker>`_.

Development
===========

Getting Started
---------------

Mamchecker uses `github <https://github.com/mamchecker/mamchecker>`_
to exchange exercises and content. Discussion related to development
can be done there.

Further communication can be done via the
`Mamchecker Mailing List <https://groups.google.com/d/forum/mamchecker>`_.

After cloning from github, before running ``dev_appserver``::

    cd mamchecker
    git submodule update --init --recursive
    cd mamchecker
    doit -kd. html
    cd ..
    doit initdb
    doit test #needs py.test2, else do `py.test mamchecker`

You can find out more via these links

- `purpose <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/cz/en.rst>`_

- `ideas <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/da/en.rst>`_

- `queries <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/db/en.rst>`_

- `query rights <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/de/en.rst>`_

- `participate <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/dc/en.rst>`_

- `history <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/df/en.rst>`_

- `try in class <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/dd/en.rst>`_


.. mamchecker/r/cz/en.rst
   mamchecker/r/da/en.rst
   mamchecker/r/db/en.rst
   mamchecker/r/de/en.rst
   mamchecker/r/dc/en.rst
   mamchecker/r/df/en.rst
   mamchecker/r/dd/en.rst


Also look at the example exercises in the
`r <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r>`_ folder.

A setup on Linux (ArchLinux, 2019-11-26)::

  cd ~/.local/opt/
  curl -OLs https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-272.0.0-linux-x86_64.tar.gz
  tar -xf google-cloud-sdk-272.0.0-linux-x86_64.tar.gz
  rm google-cloud-sdk-272.0.0-linux-x86_64.tar.gz
  cd google-cloud-sdk
  ./install.sh

  #new terminal
  gcloud components install app-engine-python app-engine-python-extras

  cd ~
  git clone https://github.com/mamchecker/mamchecker
  cd mamchecker
  tar -xf doit-0.29.0.tar.gz
  pip2 install --user doit-0.29.0/
  rm -rf doit-0.29.0
  pip2 install --user numpy==1.6.1 matplotlib==1.2.0 sympy pyyaml pytest coverage mock lxml sphinx sphinxcontrib-tikz sphinxcontrib-texfigure webtest

  cd ~/mamchecker/mamchecker
  doit -kd. html
  cd ..
  doit initdb
  python2 -m pytest mamchecker
  doit cov
  cd ..
  python2 `which dev_appserver.py` mamchecker --host=0.0.0.0

  #upload
  cd mamchecker
  gcloud init --console-only
  gcloud app deploy app.yaml


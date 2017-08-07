Mamchecker creates and checks exercises programmatically using python over the internet.

``Mam`` comes from ``MAtheMathics``.

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

Mamchecker uses `github <https://github.com/mamchecker/mamchecker>`_
to exchange exercises and content. Discussion related to development
can be done there. 

Further communication can be done via the
`Mamchecker Mailing List <https://groups.google.com/d/forum/mamchecker>`_.

After cloning from github, before running ``dev_appserver``::

    sudo pip2 install doit-0.29.0.tar.gz
    git submodule update --init --recursive
    cd mamchecker/mamchecker
    doit -kd. html
    cd ..
    doit initdb

You can find out more via these links

- `purpose <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/cz/en.rst>`_

- `ideas <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/da/en.rst>`_

- `queries <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/db/en.rst>`_

- `query rights <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/de/en.rst>`_

- `participate <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/dc/en.rst>`_

- `history <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/df/en.rst>`_

- `try in class <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/dd/en.rst>`_

Also look at the example exercises in the 
`r <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r>`_ folder.


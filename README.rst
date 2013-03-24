.. code-block:: python

    # -*- coding: utf-8 -*-
    from virtup.emulator.qemu import Box


    class Web(Box):
        base = 'Ubuntu.12.04.64.qcow2'


    web1 = Web('web1')
    web1.start()

# -*- coding: utf-8 -*-
from virtup.box import Box as BaseBox


class Box(BaseBox):
    type = 'qemu'
    connection_uri = "qemu:///session"

    @property
    def emulator(self):
        return "/usr/bin/qemu-system-%s" % self.arch

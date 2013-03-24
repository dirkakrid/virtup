# -*- coding: utf-8 -*-
import unittest
from xml.etree.ElementTree import tostring

from virtup.box import Box


class TestBox(Box):
    type = 'qemu'
    uuid = '641811a3-3dd3-4627-8410-1b4068bde4dd'
    base = 'base'
    emulator = '/usr/bin/emulator'
    working_image_path = '/dev/an/image'


class BoxTest(unittest.TestCase):
    def test_domain_xml_defaults(self):
        box = TestBox('my box')
        box.type = 'qemu'
        self.assertIn(tostring(box.os_xml), tostring(box.domain_xml))
        self.assertIn(tostring(box.devices_xml), tostring(box.domain_xml))
        self.assertEqual(tostring(box.domain_xml),
            '<domain type="qemu">'
            "<name>my box</name>"
            "<uuid>641811a3-3dd3-4627-8410-1b4068bde4dd</uuid>"
            "<vcpu>1</vcpu>"
            "<currentMemory>256000</currentMemory>"
            "<memory>256000</memory>"
            '<clock offset="utc" />'
            "<on_poweroff>destroy</on_poweroff>"
            "<on_reboot>restart</on_reboot>"
            "<on_crash>destroy</on_crash>"
            "%s%s" % (tostring(box.os_xml), tostring(box.devices_xml)) + \
            "</domain>")

    def test_devices_xml(self):
        box = TestBox('my box')
        self.assertIn(tostring(box.disk_xml), tostring(box.devices_xml))

    def test_disk_xml(self):
        box = TestBox('my box')
        self.assertEqual(tostring(box.disk_xml),
            '<disk device="disk" type="block">'
            '<target bus="ide" dev="hda" />'
            '<source dev="/dev/an/image" />'
            '</disk>')


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-
import libvirt
from uuid import uuid4
from xml.etree.ElementTree import Element, SubElement, tostring


class Box(object):
    # Configs
    memory = 256000
    cpu = 1
    arch = "x86_64"
    type = None
    base = None
    emulator = None
    # Connections
    connect_uri = None
    _connections = {}

    def __init__(self, name, memory=None, cpu=None, uuid=None):
        if self.type is None:
            raise NotImplementedError("Can't instanciate virtup.Box")
        if self.base is None:
            raise NotImplementedError("A base image is required")

        self.name = name
        if memory is not None:
            self.memory = memory
        if cpu is not None:
            self.cpu = cpu
        if not hasattr(self, 'uuid'):
            if uuid is None:
                self.uuid = str(uuid4())
            else:
                self.uuid = uuid

    @property
    def connection(self):
        if not self.connection_uri in self._connections:
            self._connections[self.connection_uri] = \
                libvirt.open(self.connection_uri)
        return self._connections[self.connection_uri]

    @property
    def domain(self):
        if not self.name in self.connection.listDefinedDomains():
            self.connection.defineXML(tostring(self.domain_xml))
        return self.connection.lookupByName(self.name)

    @property
    def domain_xml(self):
        domain = Element('domain')
        domain.attrib['type'] = self.type
        SubElement(domain, "name").text = self.name
        SubElement(domain, "uuid").text = str(self.uuid)
        SubElement(domain, "vcpu").text = str(self.cpu)
        SubElement(domain, "currentMemory").text = str(self.memory)
        SubElement(domain, "memory").text = str(self.memory)
        SubElement(domain, "clock").attrib['offset'] = "utc"
        SubElement(domain, "on_poweroff").text = "destroy"
        SubElement(domain, "on_reboot").text = "restart"
        SubElement(domain, "on_crash").text = "destroy"
        domain.append(self.os_xml)
        domain.append(self.devices_xml)
        return domain

    @property
    def devices_xml(self):
        devices = Element("devices")
        SubElement(devices, "emulator").text = self.emulator
        devices.append(self.disk_xml)
        return devices

    @property
    def disk_xml(self):
        disk = Element("disk")
        disk.attrib["type"] = "block"
        disk.attrib["device"] = "disk"
        target = SubElement(disk, "target")
        target.attrib["dev"] = "hda"
        target.attrib["bus"] = "ide"
        target = SubElement(disk, "source")
        target.attrib["dev"] = self.working_image_path
        return disk

    @property
    def os_xml(self):
        os = Element("os")
        type_ = SubElement(os, "type")
        type_.attrib["arch"] = self.arch
        type_.attrib["machine"] = "pc"
        type_.text = 'hvm'
        return os

    @property
    def working_image_path(self):
        return self.base

    def start(self):
        return self.domain.create()

    def stop(self):
        self.domain.destroy()
        self.domain.undefine()

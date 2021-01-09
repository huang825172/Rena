#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/9 0009
# @Email : happy.huangyang@gmail.com

""" Input handling """

import event
import keyboard


class KeyEvent(event.Event):
    """
    Event triggers on hooking keys down/up.
    :param key: Name of key in the event
    :param action: Action of key, down or up
    """

    def __init__(self, key: str, action: str):
        super(KeyEvent, self).__init__(self.__class__.__name__)
        self.key = key
        self.action = action


class KeyboardInput:
    """
    Keyboard input instance.
    :param event_bus: EventBus for emitting KeyEvents.
    """

    def __init__(self, event_bus: event.EventBus):
        self._event_bus = event_bus
        self._is_active = False

    def hook(self, key):
        """
        Add event emit for a key.
        :param key: Trigger key
        """
        keyboard.hook_key(key, self._create_event)

    def active(self, is_active: True):
        """
        Set whether this input module is active functioning.
        :param is_active: Active status
        """
        self._is_active = is_active

    def _create_event(self, e: keyboard.KeyboardEvent):
        if self._is_active:
            self._event_bus.emit(KeyEvent(e.name, e.event_type))

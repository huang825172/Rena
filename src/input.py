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
        super(KeyEvent, self).__init__('KeyEvent')
        self.key = key
        self.action = action


class KeyboardInput:
    """
    Keyboard input instance.
    :param event_bus: EventBus for emitting KeyEvents.
    """

    def __init__(self, event_bus: event.EventBus):
        self._event_bus = event_bus

    def hook(self, key):
        """
        Add event emit for a key.
        :param key: Trigger key
        """
        keyboard.hook_key(key, self._create_event)

    def _create_event(self, e: keyboard.KeyboardEvent):
        self._event_bus.emit(KeyEvent(e.name, e.event_type))

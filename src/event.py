#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/9 0009
# @Email : happy.huangyang@gmail.com

""" Event handling """

import typing


class Event:
    """
    Event base.
    :param name: Name of specific event
    """

    def __init__(self, name: str):
        self.name = name


class EventBus:
    """
    Eventbus
    """

    def __init__(self):
        self.event_table = []
        self.callbacks = []

    def emit(self, event: Event):
        """
        Emit event and call callbacks.
        :param event: Event to emit
        """
        for e in self.event_table:
            if isinstance(event, e[0]):
                for c in e[1]:
                    self.callbacks[c](event)
                break

    def on(self, event: type, callback: typing.Callable):
        """
        Add callback for event
        :param event: Event to response
        :param callback: Callback function to call
        """
        for e in self.event_table:
            if event == e[0]:
                self.callbacks.append(callback)
                e[1].append(len(self.callbacks) - 1)
                return
        self.callbacks.append(callback)
        self.event_table.append([event, [len(self.callbacks) - 1]])

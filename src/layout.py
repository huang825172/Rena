#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/8 0008
# @Email : happy.huangyang@gmail.com

""" Image, menu rendering """

import render


class Layout:
    """ Layout base. """

    def __init__(self, parent=None):
        self.parent = parent
        if parent:
            parent.children.append(self)
        self.children = []


class UI:
    """
    UI instance.
    :param root: Root layout of UI
    :param renderer: Renderer for rendering
    """

    def __init__(self, root: Layout, renderer: render.Renderer):
        self.root_layout = root
        self.renderer = renderer

    def draw(self):
        """
        Draw controls onto framebuffer.
        """
        self._layout(self.renderer, self.root_layout)

    def _layout(self, renderer: render.Renderer, layout: Layout):
        w = 1
        h = 1
        if layout == self.root_layout:
            w = renderer.frame_width
            h = renderer.frame_height
        else:
            if isinstance(layout, Horizontal):
                w = layout.parent.w
                h = layout.h
            elif isinstance(layout, Vertical):
                w = layout.w
                h = layout.parent.h
        if isinstance(layout, Horizontal):
            x = 1
            is_container = True
            for i in layout.children:
                if isinstance(i, Vertical):
                    is_container = False
                    r = render.Renderer(i.w, h)
                    r.clear(i.back_color)
                    x += i.ml
                    self._layout(r, i)
                    renderer.paste_fb(x, 1, r)
                    x += i.w
                    x += i.mr
                else:
                    if not is_container:
                        break
                    if isinstance(i, Image):
                        x_offset = w // 2 - i.get_width() // 2
                        y_offset = h // 2 - i.get_height() // 2
                        renderer.string(i.image, x + x_offset, 1 + y_offset, i.fore_color, i.back_color)
                        break
        elif isinstance(layout, Vertical):
            y = 1
            is_container = True
            for i in layout.children:
                if isinstance(i, Horizontal):
                    is_container = False
                    r = render.Renderer(w, i.h)
                    r.clear(i.back_color)
                    y += i.mt
                    self._layout(r, i)
                    renderer.paste_fb(1, y, r)
                    y += i.h
                    y += i.mb
                else:
                    if not is_container:
                        break
                    if isinstance(i, Image):
                        x_offset = w // 2 - i.get_width() // 2
                        y_offset = h // 2 - i.get_height() // 2
                        renderer.string(i.image, 1 + x_offset, y + y_offset, i.fore_color, i.back_color)
                        break


class Vertical(Layout):
    """
    Vertical linear layout.
    :param w: Layout width in character
    :param parent: Parent layout, None for root
    :param margin_left: Left margin width
    :param margin_right: right margin width
    :param back_color: Layout background color
    """

    def __init__(self, w: int, parent: Layout = None,
                 margin_left: int = 0, margin_right: int = 0,
                 back_color: str = ''):
        super(Vertical, self).__init__(parent)
        self.w = w
        self.ml = margin_left
        self.mr = margin_right
        self.back_color = back_color


class Horizontal(Layout):
    """
    Horizontal linear layout.
    :param h: Layout height in character
    :param parent: Parent layout, None for root
    :param margin_top: Top margin height
    :param margin_bottom: Bottom margin height
    :param back_color: Layout background color
    """

    def __init__(self, h: int, parent: Layout = None,
                 margin_top: int = 0, margin_bottom: int = 0,
                 back_color: str = ''):
        super(Horizontal, self).__init__(parent)
        self.h = h
        self.mt = margin_top
        self.mb = margin_bottom
        self.back_color = back_color


class Control(Layout):
    """
    Control base.
    :param parent: Parent layout
    """

    def __init__(self, parent: Layout):
        super(Control, self).__init__(parent)


class Image(Control):
    """
    Image, ASCII art control.
    :param image: Image string
    :param parent: Parent layout
    :param fore_color: Character color
    :param back_color: Background color
    """

    def __init__(self, image: str, parent: Layout, fore_color: str = 'black', back_color: str = ''):
        super(Image, self).__init__(parent)
        self.image = image
        self.fore_color = fore_color
        self.back_color = back_color

    def get_width(self):
        """
        Get width of the image.
        :return: Max line width
        """
        return max(map(len, self.image.split('\n')))

    def get_height(self):
        """
        Get height of the image.
        :return: Lines amount
        """
        return len(self.image.split('\n'))

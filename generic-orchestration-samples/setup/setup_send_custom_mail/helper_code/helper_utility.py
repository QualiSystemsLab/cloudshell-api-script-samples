"""
Module for storing utility functions to be used across sandbox helper files
"""


def html_red(err_str):
    """
    For use in sb_print statements. Wraps output in red.
    :param err_str:
    :return:
    """
    return "<span style='color: red'>{err_str}</span>".format(err_str=err_str)


def html_wrap(content_str, elm, color="white"):
    """
    For use in sb_print statements. Wraps output in custom element and color:
    :param err_str:
    :return:
    """
    return "<{elm} style='color: {color}'>{content_str}</{elm}>".format(content_str=content_str,
                                                                        elm=elm,
                                                                        color=color)



"""
Module for storing general utility functions
"""


def html_err_wrap(err_str):
    """
    For use in sb_print statements. Wraps output in red.
    :param err_str:
    :return:
    """
    return "<span style='color: red'>{err_str}</span>".format(err_str=err_str)


def html_wrap(content, color="white", elm="span"):
    """
    custom html wrapping, set custom color or html element
    :param str content: the message string
    :param str elm: the html element
    :param str color: the color
    :return:
    """
    return "<{elm} style='color: {color}'>{content}</{elm}>".format(content=content,
                                                                    elm=elm,
                                                                    color=color)


def html_link_wrap(url, link_text):
    """
    wrap text in hyperlink anchor tag, will be opened in new tab
    :param str url: ex: "http://www.google.com"
    :param str link_text: whatever you want the link to be displayed as
    :return:
    """
    return """<a href={url} 
           style="text-decoration: underline"
           target = "_blank"
           rel = "noopener noreferrer"
           >{link_text}</a>""".format(url=url, link_text=link_text)



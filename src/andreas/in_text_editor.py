from talon import Module, Context

mod = Module()

mod.tag("cursorless_in_text_editor", desc="Tag for when cursorless is in a text editor")


ctx = Context()
ctx.matches = r"""
app: vscode
win.title: /\[Text Editor\]$/
"""

ctx.tags = ["user.cursorless_in_text_editor"]

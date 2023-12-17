from talon import Context, actions
from ..targets.target_types import ImplicitDestination, PrimitiveTarget

ctx = Context()
ctx.matches = r"""
app: vscode
win.title: /\[Text Editor\]$/
"""

target = PrimitiveTarget(None, None)


@ctx.action_class("user")
class Actions:
    def edit_cut():
        actions.user.cursorless_command("cutToClipboard", target)

    def edit_copy():
        actions.user.cursorless_command("copyToClipboard", target)

    def edit_paste():
        actions.user.private_cursorless_paste(ImplicitDestination())

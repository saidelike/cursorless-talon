from talon import Context, actions
from ..targets.target_types import (
    ImplicitDestination,
    PrimitiveDestination,
    PrimitiveTarget,
)

ctx = Context()
ctx.matches = r"""
app: vscode
win.title: /\[Text Editor\]$/
"""

primitive_target = PrimitiveTarget(None, None)
primitive_destination = PrimitiveDestination("to", primitive_target)
implicit_destination = ImplicitDestination()


@ctx.action_class("user")
class Actions:
    def edit_cut():
        actions.user.cursorless_command("cutToClipboard", primitive_target)

    def edit_copy():
        actions.user.cursorless_command("copyToClipboard", primitive_target)

    def edit_paste(expand: bool):
        if expand:
            actions.user.private_cursorless_paste(primitive_destination)
        else:
            actions.user.private_cursorless_paste(implicit_destination)

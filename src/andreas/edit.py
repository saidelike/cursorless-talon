from talon import Context, actions
from ..targets.target_types import PrimitiveTarget, PrimitiveDestination


ctx = Context()
ctx.matches = r"""
app: vscode
tag: user.cursorless_in_text_editor
"""

target = PrimitiveTarget(None, None)
destination = PrimitiveDestination("to", target)


@ctx.action_class("edit")
class Actions:
    def cut():
        actions.user.cursorless_command("cutToClipboard", target)

    def copy():
        actions.user.cursorless_command("copyToClipboard", target)

    def paste():
        actions.user.private_cursorless_paste(destination)

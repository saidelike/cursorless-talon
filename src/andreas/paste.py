from talon import Module, actions
from ..targets.target_types import ImplicitDestination


mod = Module()


@mod.action_class
class Actions:
    def c_edit_paste():
        """Paste from clipboard using Cursorless"""
        actions.user.private_cursorless_paste(ImplicitDestination())

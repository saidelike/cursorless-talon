from talon import Context, actions

ctx = Context()

ctx.matches = r"""
app: vim
"""

ctx.tags = ["user.cursorless"]

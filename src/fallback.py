from talon import Context, actions
from typing import Any, Union
from .actions.bring_move import BringMoveTargets
from .targets.target_types import (
    CursorlessDestination,
    CursorlessTarget,
    ImplicitDestination,
    ImplicitTarget,
    PrimitiveDestination,
    PrimitiveTarget,
)
from .actions.get_text import cursorless_get_text_action

ctx = Context()
ctx.matches = r"""
app: vscode
not win.title: /\[Text Editor\]$/
"""


def replace_with_target(target: CursorlessTarget):
    """Insert target as text"""
    texts = cursorless_get_text_action(target)
    text = "\n".join(texts)
    actions.insert(text)


def wrap_with_paired_delimiter(pair: list[str]):
    """Wrap selection with paired delimiters"""
    actions.user.delimiters_pair_wrap_selection_with(pair[0], pair[1])


fallback_action_callbacks = {
    "setSelection": actions.skip,
    "copyToClipboard": actions.edit.copy,
    "cutToClipboard": actions.edit.cut,
    "pasteFromClipboard": actions.edit.paste,
    "clearAndSetSelection": actions.edit.delete,
    "remove": actions.edit.delete,
    "applyFormatter": actions.user.reformat_selection,
    "editNewLineBefore": actions.edit.line_insert_up,
    "editNewLineAfter": actions.edit.line_insert_down,
    "nextHomophone": actions.user.homophones_cycle_selected,
    "replaceWithTarget": replace_with_target,
    "wrapWithPairedDelimiter": wrap_with_paired_delimiter,
}

fallback_target_callbacks = {
    "selection": actions.skip,
    "extendThroughStartOf": actions.user.select_line_start,
    "extendThroughEndOf": actions.user.select_line_end,
    "containing_document": actions.edit.select_all,
    "containing_paragraph": actions.edit.select_paragraph,
    "containing_line": actions.edit.select_line,
    "containing_token": actions.edit.select_word,
}


@ctx.action_class("user")
class UserActions:
    def cursorless_command(action_name: str, target: CursorlessTarget):
        if use_fallback(target):
            perform_fallback_command(action_name, target)
        else:
            actions.next(action_name, target)

    def private_cursorless_reformat(target: CursorlessTarget, formatters: str):
        if use_fallback(target):
            perform_fallback_command("applyFormatter", target, formatters)
        else:
            actions.next(target, formatters)

    def private_cursorless_wrap_with_paired_delimiter(
        action_name: str, target: CursorlessTarget, paired_delimiter: list[str]
    ):
        if use_fallback(target):
            perform_fallback_command(
                action_name,
                target,
                paired_delimiter,
            )
        else:
            actions.next(action_name, target, paired_delimiter)

    def private_cursorless_bring_move(action_name: str, targets: BringMoveTargets):
        if use_fallback(targets.destination):
            perform_fallback_command(action_name, targets.destination, targets.source)
        else:
            actions.next(action_name, targets)


def perform_fallback_command(
    action_name: str,
    target: Union[CursorlessTarget, CursorlessDestination],
    args: Any = None,
):
    """Perform non Cursorless fallback command"""
    actions.user.debug(
        "Current command targets selection and is not in a text editor. Perform fallback command."
    )
    try:
        action_callback = get_fallback_action_callback(action_name)
        target_callback = get_fallback_target_callback(target)
        target_callback()
        if args is not None:
            action_callback(args)
        else:
            action_callback()
    except ValueError as ex:
        actions.app.notify(str(ex))


def get_fallback_action_callback(action_name: str):
    """Return action callback"""
    if action_name in fallback_action_callbacks:
        return fallback_action_callbacks[action_name]
    raise ValueError(f"Unknown Cursorless fallback action: {action_name}")


def get_fallback_target_callback(
    target: Union[CursorlessTarget, CursorlessDestination]
):
    """Get target selection callable"""
    if isinstance(target, (ImplicitTarget, ImplicitDestination)):
        return fallback_target_callbacks["selection"]

    if isinstance(target, PrimitiveDestination):
        return get_fallback_target_callback(target.target)

    if not target.modifiers:
        return fallback_target_callbacks["selection"]

    if len(target.modifiers) == 1:
        modifier = target.modifiers[0]
        modifier_type = modifier["type"]
        if modifier_type == "containingScope":
            modifier_type = f"containing_{modifier['scopeType']['type']}"
        if modifier_type in fallback_target_callbacks:
            return fallback_target_callbacks[modifier_type]
        raise ValueError(f"Unknown Cursorless fallback modifier type: {modifier_type}")

    raise ValueError(f"Unknown Cursorless fallback target: {target}")


def use_fallback(target: Union[CursorlessTarget, CursorlessDestination]) -> bool:
    """Returns true if fallback is to be used"""
    return target_is_selection(target)


def target_is_selection(target: Union[CursorlessTarget, CursorlessDestination]) -> bool:
    """Returns true if target is selection"""
    if isinstance(target, (ImplicitTarget, ImplicitDestination)):
        return True
    if isinstance(target, PrimitiveDestination):
        return target_is_selection(target.target)
    if isinstance(target, PrimitiveTarget):
        return not target.mark or target.mark["type"] == "cursor"
    return False

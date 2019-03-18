"""Util functions and globals shared between many CLI modules"""
from PyInquirer import style_from_dict, Token, prompt, Separator, ValidationError


def print_tags(tags, prefix="Tags:"):
    """prints tag lists to screen"""
    print(prefix)
    for tag in tags:
        print(f"    {tag}")


def check_number(string):
    """Checks a string can be parsed to a number"""
    try:
        float(string)
        return True
    except ValueError:
        message = 'Please input a number.'
        raise ValidationError(message=message)


def check_integer(string):
    """Checks a string can be parsed to a number"""
    try:
        int(string)
        return True
    except ValueError:
        message = 'Please input a number.'
        raise ValidationError(message=message)


def validate_image_id(new_id, used_ids):
    """Validates a component ID against the IDS in an assetpack"""
    if len(new_id) < 3:
        message = 'Try an ID with more than 2 characters.'
        raise ValidationError(message=message)
    if len(new_id.split()) > 1:
        message = "Please don't use whitespace for ID's"
        raise ValidationError(message=message)
    if new_id in used_ids:
        message = 'This image name already exists.'
        raise ValidationError(message=message)
    return True


STYLE = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

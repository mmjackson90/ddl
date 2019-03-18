"""Util functions and globals shared between many CLI modules"""
from PyInquirer import style_from_dict, Token, prompt, Separator


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
        raise PyInquirer.ValidationError(message=message)


STYLE = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

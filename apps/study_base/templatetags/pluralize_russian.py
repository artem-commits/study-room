from django import template

register = template.Library()


@register.filter
def pluralize_participants(number):
    number = abs(int(number))
    if number == 0:
        return "участников"
    last_two = number % 100
    last_one = number % 10

    if 11 <= last_two <= 14:
        return "участников"
    if last_one == 1:
        return "участник"
    if 2 <= last_one <= 4:
        return "участника"
    return "участников"
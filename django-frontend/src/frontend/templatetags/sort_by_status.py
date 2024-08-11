from django import template

register = template.Library()

@register.filter
def sort_by_status(users):
  order = {
    'online': 0,
    'ingame': 1,
    'offline': 2,
  }
  return sorted(users, key=lambda user: order[user['status']])
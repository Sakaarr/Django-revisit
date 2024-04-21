from django import template

register = template.Library()

@register.filter
def format_time(hour):
    """Formats the given hour into a 12-hour time format with AM/PM."""
    ampm = 'AM' if hour < 12 else 'PM'
    hour_formatted = hour if hour <= 12 else hour - 12
    return f"{hour_formatted} {ampm}"

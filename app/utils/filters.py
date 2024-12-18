def format_date(date):
    return date.strftime('%m/%d/%y')

# This code removes all extraneous information from a URL string, leaving only the domain name
def format_url(url):
    return url.replace('http://', '').replace('https://','').replace('www.', '').split('/')[0].split('?')[0]

# address the issue of correctly pluralizing words
def format_plural(amount, word):
    if amount != 1:
        return word + 's'
    
    return word

from datetime import datetime
# Test the filters | % python3 app/utils/filters.py
print(format_date(datetime.now()))
print(format_url('http://google.com/test/'))
print(format_url('https://www.google.com?q=test'))
print(format_plural(2, 'cat'))
print(format_plural(1, 'dog'))
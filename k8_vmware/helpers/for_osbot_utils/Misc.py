import string
import random

def random_password(length=24, prefix=''):

    password = prefix + ''.join(random.choices(string.ascii_lowercase  +
                                               string.ascii_uppercase +
                                               string.punctuation     +
                                               string.digits          ,
                                               k=length))
    # replace these chars with _  (to make prevent errors in command prompts)
    items = ['"', '\'', '`','\\','}']
    for item in items:
        password = password.replace(item, '_')
    return password

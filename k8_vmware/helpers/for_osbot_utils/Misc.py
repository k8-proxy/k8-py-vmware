import string
import random

def random_password(length=24, prefix=''):
    return prefix + ''.join(random.choices(string.ascii_lowercase +
                                           string.ascii_uppercase +
                                           string.punctuation.replace('"','').replace('\'','') + # remove "  and ' (to make prevent errors in command prompts)
                                           string.digits          ,
                                           k=length))

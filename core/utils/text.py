def extract_hashtags(text) :
    hashtags = [token.strip("#")  for  token in  text.split() if token.startswith("#") ]
    return hashtags

def extract_mentions(text) :
    return [token.strip("@") for token in  text.split() if token.startswith("@") ]

def to_consize_digits(number) :
    """ turns 10453 to 10.4k 1223343 to 1.2M etc"""
    return number
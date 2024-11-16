from django import template


register = template.Library()

@register.filter()
def startswith_vowel(word) :
    if not isinstance(word,str) :
        return False
    return word.lower()[0] in ['a','e','i','o','u']    


@register.filter()
def capitalize(word) :
    try : return word.capitalize()
    except : pass


@register.filter()
def pluralize(count,word) :
    #use the count to determine weather to add "s" to a word or not
    try : 
        if count > 1 :
            return word + "s"
        else : 
            return word    
    except : 
        pass
    
    return word    


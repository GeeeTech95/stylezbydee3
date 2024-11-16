
def get_item_type(request) :
    return  request.path.strip("/").split("/")[0]
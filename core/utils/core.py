import os

def get_file_type(file_path) :
       
    extensions = {
        'video':['.mp4','.avi','.3gp'],
        'image' : ['.jpg','.jpeg','.png','.jfif']
        }

    
    filename,file_ext = os.path.splitext(file_path)

    file_ext = file_ext.lower()

    if file_ext in extensions['video'] :
        return "video"
    elif file_ext in extensions['image']  :
        return "image"
    else :
        return None



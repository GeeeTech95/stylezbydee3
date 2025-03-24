from typing import Any
from django.views import generic
from shop.models import Product
import os
import shutil
from django.conf import settings
from PIL import Image

class HomePage(generic.TemplateView) :
    template_name = "index.html"


    def process_images(self,src_folder, dest_folder, quality=85):
        """
        Recursively processes images in the src_folder, converting them to WebP, 
        and saves them in dest_folder while maintaining the folder structure.
        """
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        for root, dirs, files in os.walk(src_folder):
            # Preserve folder structure
            relative_path = os.path.relpath(root, src_folder)
            dest_path = os.path.join(dest_folder, relative_path)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            for file in files:
                src_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_path, os.path.splitext(file)[0] + ".webp")
                
                try:
                    with Image.open(src_file_path) as img:
                        # Only convert valid images to WebP
                        img.convert("RGB").save(dest_file_path, "webp", quality=quality)
                        print(f"Processed: {src_file_path} -> {dest_file_path}")
                except Exception as e:
                    print(f"Error processing {src_file_path}: {e}")





    def get_context_data(self, **kwargs) :
        source_folder = os.path.join(settings.STATICFILES_DIRS[0], "img")  # Adjust index if multiple dirs
        destination_folder = os.path.join(settings.STATICFILES_DIRS[0], "img2")  # Change STATICFILES_DIRS[0] to STATIC_ROOT if needed
        # Run the function
        #self.process_images(source_folder, destination_folder)
        ctx = super(HomePage,self).get_context_data(**kwargs)
        ctx['new_arrivals'] = Product.objects.all().order_by("-created_at")[:6]
        ctx['best_selling'] = Product.objects.all()[:6]
        return ctx
        


class Contact(generic.TemplateView) :
    template_name = "contact.html"

    def get_context_data(self, **kwargs: Any) :
        ctx = super(Contact,self).get_context_data(**kwargs)
        return ctx



class TestTemplate(generic.TemplateView):
    template_name = "email/security/verification-code-mail.html"

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        context['user_obj'] = self.request.user
        context['reset_link'] = 'https://example.com/reset-password'  # Example URL for password resetontext
        context['verification_code'] = '123456'  #
        return context
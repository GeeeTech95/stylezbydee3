from collections import defaultdict

from django.db import models
from django.db.models import Exists, OuterRef
from django.db.models.constants import LOOKUP_SEP
from treebeard.mp_tree import MP_NodeQuerySet


class CategoryQuerySet(MP_NodeQuerySet):

    def browsable(self):
        """
        Excludes non-public categories
        """
        return self.filter(
            is_public=True, 
            ancestors_are_public=True
            )


class CustomManager(models.Manager) :

    def bulk_get_or_create(self,objs,lookup_field =  None,create_fields = None,extra_params=None) :
        assert lookup_field, "not set 'lookup_field' for custom bulk_get_or_create"
        
        #extra_params is a dictionary  used in adding more conditions 
        #like return created : to return only created objects or return all to return all objects
        lookup = {f'{lookup_field}__in' : [getattr(obj,lookup_field) for obj in objs]}
        existing_objects = [
            obj for obj in self.get_queryset().filter(**lookup)
        ]
        existing_object_lookup_fields = [
            getattr(obj,lookup_field) for obj in existing_objects
        ]
        non_existing_objects = [
            obj for obj in objs if getattr(obj,lookup_field) not in existing_object_lookup_fields
        ]
        
        #set attrs for create fields
        if create_fields : 
            for obj in non_existing_objects :
                for field,value in create_fields.items() :
                    setattr(obj,field,value)

        self.bulk_create(non_existing_objects,batch_size=999)
        #if we shd return both created and matching queries
        if extra_params.get("return_all",False) :
            return super().get_queryset().filter(**lookup)


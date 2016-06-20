"""Gallery page model, and assoicated image and image groups
"""
# future imports
from __future__ import absolute_import

# third-party imports
from google.appengine.ext import ndb

# local imports
from base.models import BaseModel
from base.models import OrderMixin
# from base.models import UploadMixin
from modules.pages.models import PageBaseModel


class GalleryPage(PageBaseModel):
    page_tag = 'gallery'


class ImageGroup(BaseModel, OrderMixin):
    pass


class Image(BaseModel, OrderMixin):
    group = ndb.KeyProperty(kind='ImageGroup', required=False)

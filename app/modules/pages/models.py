"""Base models and functionality for all pages of the app
"""
# future imports
from __future__ import absolute_import

# third-party imports
from google.appengine.ext import ndb

# local imports
from app.models.base import BaseModel
from app.models.base import OrderMixin


class PageBaseModel(BaseModel):
    """Base model for all pages
    """

    # Note 'visible' is set to false by default, to prevent new pages
    # from automatically being displayed publicily before content
    # is populated
    visible = ndb.BooleanProperty(default=False, indexed=True)
    nav = ndb.KeyProperty(kind='Nav', required=True)
    meta = ndb.KeyProperty(kind='MetaData', required=True)
    tag = ndb.StringProperty(required=True, indexed=True)

    @classmethod
    def get_by_tag(cls, tag):
        return cls.query(cls.tag == tag).get()


class PageNav(BaseModel, OrderMixin):
    """Records used to displaying links for each page
    """

    visible = ndb.BooleanProperty(default=False, indexed=True)
    title = ndb.StringProperty(required=True, indexed=True)
    path = ndb.StringProperty(required=True, indexed=True)


class PageMeta(BaseModel):
    """Records used managing the meta data for each page
    """

    title = ndb.StringProperty(required=True, indexed=False)
    description = ndb.StringProperty(required=False, indexed=False)
    tags = ndb.StringProperty(required=False, repeated=True, indexed=False)

    def update(self, form):
        """Update a records property values from a form's request data.
        """
        # Tags are displayed as a comma separated list, but saved as
        # a list of strings
        form.tags.data = [
            t.strip() for t in form.tags.data.split(',') if t
        ]
        return super(PageMeta, self).update(form)

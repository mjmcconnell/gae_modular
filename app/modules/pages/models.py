"""Base models and functionality for all pages of the app
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import logging

# third-party imports
from google.appengine.ext import ndb

# local imports
from base.models import BaseModel
from base.models import OrderMixin


logger = logging.getLogger(__name__)


class DuplicateTagException(Exception):
    pass


class ExistingTagException(Exception):
    pass


class PageNav(BaseModel, OrderMixin):
    """Records used to displaying links for each page
    """

    # If true, displays the nav element on the public site
    visible = ndb.BooleanProperty(default=False, indexed=True)
    title = ndb.StringProperty(required=False, indexed=False)

    @classmethod
    def fetch_by_tag(cls, tag=None):
        if tag is None:
            tag = cls.page_tag
        return cls.query(cls.tag == tag).fetch()


class PageBaseModel(BaseModel):
    """Base model for all pages
    """

    # Note 'visible' is set to false by default, to prevent new pages
    # from automatically being displayed publicily before content
    # is populated
    visible = ndb.BooleanProperty(default=False, indexed=True)
    is_draft = ndb.BooleanProperty(default=True, indexed=True)
    owner = ndb.StringProperty(required=False, indexed=True)
    contributors = ndb.StringProperty(
        required=False,
        repeated=True,
        indexed=False
    )

    nav = ndb.KeyProperty(kind='PageNav', required=True)

    meta_title = ndb.StringProperty(required=False, indexed=False)
    meta_description = ndb.StringProperty(required=False, indexed=False)
    meta_tags = ndb.StringProperty(
        required=False,
        repeated=True,
        indexed=False
    )

    @classmethod
    def register(cls, title):
        """Register a modules page record, if one does not already exist
        """
        record = cls.query().get()
        if record is None:
            nav_key = PageNav(title=title).put()
            record = cls(
                nav=nav_key,
                is_draft=False,
                meta_title=title,
            ).put()

    @classmethod
    def get_published(cls):
        return cls.query(cls.is_draft == False).get()

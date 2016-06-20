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
    title = ndb.StringProperty(required=False, indexed=True)
    # Value used for build route, using "uri_for"
    uri_name = ndb.StringProperty(required=False, indexed=True)


class PageBaseModel(BaseModel):
    """Base model for all pages
    """

    # Unique tag to identify the page
    tag = ndb.StringProperty(required=True, indexed=True)
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
    def fetch_by_tag(cls, tag=None):
        if tag is None:
            tag = cls.page_tag
        return cls.query(cls.tag == tag).fetch()

    @classmethod
    def register(cls):
        """Register a modules page record
        """
        queryset = cls.query(cls.tag == cls.page_tag)
        r_count = queryset.count()

        # Create a page record, for the give tag,
        # if no records with that tag exist
        if r_count == 0:
            nav_key = PageNav(
                uri_name=cls.page_tag
            ).put()
            cls(
                tag=cls.page_tag,
                nav=nav_key,
                is_draft=False
            ).put()
        # Log error if duplicate records are found for the same tag
        elif r_count > 1:
            raise DuplicateTagException(
                'Duplicate records found for the tag %s',
                cls.page_tag
            )
        # If a record exist, ensure is of the current model class
        else:
            record = queryset.get()
            if record.key.kind() != cls.__name__:
                raise ExistingTagException(
                    ('Page tag is not unique, failed to create record for %s '
                     'with the tag of %s, duplicate page_tag of %s'),
                    cls.__name__,
                    cls.page_tag,
                    record.key.kind(),
                )

    @classmethod
    def get_published(cls, tag=None):
        if tag is None:
            tag = cls.page_tag

        tag_queryset = cls.query(cls.tag == tag)
        return tag_queryset.query(cls.is_draft == False).get()

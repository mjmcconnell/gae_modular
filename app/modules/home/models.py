"""Home page model
"""
# future imports
from __future__ import absolute_import

# local imports
from modules.pages.models import PageBaseModel


class HomePage(PageBaseModel):

    # Set page tag to identify the assoicated page naviagation record
    page_tag = 'home'

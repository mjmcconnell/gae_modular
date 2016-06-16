"""Functions related to the cloudstorage lib
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import os
import logging
import re

# third-party imports
import cloudstorage as gcs
from cloudstorage import NotFoundError
from google.appengine.api import app_identity
from google.appengine.api.images import delete_serving_url
from google.appengine.api.images import get_serving_url
from google.appengine.ext.blobstore.blobstore import create_gs_key

# local imports
from app.base import constants


logger = logging.getLogger(__name__)


def _abs_filename(filename):
    """Workout the bucket location
    """
    bucket_name = app_identity.get_default_gcs_bucket_name()
    bucket_prefix = '/' + bucket_name + '/'
    return bucket_prefix + filename


def get_public_serving_url(filename):
    """Fetches the private gcs file, and creates a public link.
    """
    return_url = ''

    # ensure a filename is provided, and is acutally a file
    # we are just checking to ensure it has an extension
    if filename and os.path.splitext(filename)[1]:
        blob_key = create_gs_key('/gs' + _abs_filename(filename))

        try:
            return_url = get_serving_url(blob_key)
        except Exception, e:  # pylint: disable=broad-except
            logger.error(e)

        # Ensure we deliver the original dimensions
        return_url += '=s0'

    if not constants.IS_DEV_APPSERVER:
        # force https on all remote image urls on live env
        return_url = re.sub('http:', 'https:', return_url)

    return return_url


def store_file(filename, data, mimetype=None):
    """Save a file to the cloudstorage
    """
    bucket_path = _abs_filename(filename)

    # Clear out any previous versions of an image
    blob_key = create_gs_key('/gs' + _abs_filename(filename))
    delete_serving_url(blob_key)

    if mimetype:
        gcs_file = gcs.open(bucket_path, 'w', content_type=mimetype)
    else:
        gcs_file = gcs.open(bucket_path, 'w')

    gcs_file.write(data)
    gcs_file.close()
    return stat_file(filename)


def remove_file(filename):
    """Remove a file to the cloudstorage
    """
    try:
        gcs.delete(_abs_filename(filename))
        return True
    except gcs.NotFoundError:
        return False


def read_file(filename):
    """Read a file to the cloudstorage
    """
    try:
        gcs_file = gcs.open(_abs_filename(filename))
    except NotFoundError as e:
        logger.error(e)
        return None

    data = gcs_file.read()
    gcs_file.close()
    return data


def list_dir(path):
    """List the contents of a given directory.
    """
    return gcs.listbucket(_abs_filename(path))


def stat_file(filename):
    """Get the statistics of a file
    """
    st = gcs.stat(_abs_filename(filename))
    return {
        'filename': st.filename,
        'is_dir': st.is_dir,
        'st_size': st.st_size,
        'st_ctime': st.st_ctime,
        'etag': st.etag,
        'content_type': st.content_type,
        'metadata': st.metadata,
    }


def get_mimetype(filename):
    """Simple map of filenames to values we can use in Content-Type headers
    """
    filename, ext = os.path.splitext(filename)
    return {
        '.css': 'text/css',
        '.html': 'text/html',
        '.js': 'application/javascript',
        '.svg': 'image/svg+xml',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.jpeg': 'image/jpeg',
        '.woff': 'application/x-font-woff',
        '.swf': 'application/x-shockwave-flash',
    }.get(ext, 'application/octet-stream')

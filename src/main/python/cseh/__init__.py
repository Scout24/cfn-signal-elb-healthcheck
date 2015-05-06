import logging

from boto.utils import get_instance_metadata


logger = logging.getLogger(__name__)

def _get_instance_id():
    return get_instance_metadata()['instance-id']


def get_region():
    return get_instance_metadata()['availability-zone'][:-1]

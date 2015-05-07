import logging

from boto.utils import get_instance_metadata


logger = logging.getLogger(__name__)


def get_instance_id():
    return get_instance_metadata().get('instance-id')


def get_region():
    return get_instance_metadata().get('placement')['availability-zone'][:-1]

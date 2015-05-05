from boto.utils import get_instance_metadata


def _get_instance_id():
    return get_instance_metadata()['instance-id']


def _get_region():
    return get_instance_metadata()['availability-zone'][:-1]


def signal_elb_healthcheck(elb_name):
    instance_id = _get_instance_id()
    pass



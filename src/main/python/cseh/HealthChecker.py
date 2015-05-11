import logging
from time import sleep

from boto.ec2.elb import connect_to_region
from cseh import get_region, get_instance_id
from cseh.Signaller import Signaller


INTERVAL = 5


class HealthChecker(object):
    def __init__(self, logical_resource_id, stack_name, region=None, instance_id=None):
        self.stack_name = stack_name
        self.logical_resource_id = logical_resource_id
        self.region = region or get_region()
        self.instance_id = instance_id or get_instance_id()
        self.elb_conn = connect_to_region(self.region)
        self.logger = logging.getLogger(__name__)
        self.signaller = Signaller(instance_id, region)

    def elb_healthcheck(self, elb_name):
        instance_state = self.elb_conn.describe_instance_health(elb_name, [self.instance_id])
        state = instance_state[0].state
        self.logger.info("ELB state for instance {0}: {1}".format(self.instance_id, state))
        return state == 'InService'

    def wait_for_elb_healthcheck(self, elb_name, timeout):
        for i in range(0, timeout / INTERVAL):
            if self.elb_healthcheck(elb_name) is True:
                return self.signaller.signal(self.logical_resource_id, self.stack_name, True)
            else:
                sleep(INTERVAL)

        return self.signaller.signal(self.logical_resource_id, self.stack_name, False)

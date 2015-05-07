import logging
from time import sleep

from boto.ec2.elb import connect_to_region
from cseh import get_region, _get_instance_id


class HealthChecker(object):

    def __init__(self, region=None, instance_id=None):
        self.region = region or get_region()
        self.instance_id = instance_id or _get_instance_id()
        self.elb_conn = connect_to_region(self.region)
        self.logger = logging.getLogger(__name__)

    def elb_healthcheck(self, elb_name):
        instance_state = self.elb_conn.describe_instance_health(elb_name, [self.instance_id])
        state = instance_state[0].state
        self.logger.info("ELB state for instance {0}: {1}".format(self.instance_id, state))
        return state == 'InService'

    def wait_for_elb_healthcheck(self, elb_name):
        for i in range(0, 24):
            if self.elb_healthcheck(elb_name) is True:
                return True
            else:
                sleep(5)

        raise Exception("Instance: {0} did not come up in region: {1} within 2 minutes".format(self.instance_id,
                                                                                               self.region))


if  __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S', level=logging.INFO)
    print HealthChecker("eu-west-1", "i-490816e2").wait_for_elb_healthcheck("baufi-preappro-elb-2JG40W506GZR")
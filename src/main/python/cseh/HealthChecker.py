import logging
from time import sleep

import botocore.session
from cseh import get_region, get_instance_id
from cseh.Signaller import Signaller

INTERVAL = 5


class HealthChecker(object):
    def __init__(self, logical_resource_id, stack_name, region=None, instance_id=None):
        self.stack_name = stack_name
        self.logical_resource_id = logical_resource_id
        self.region = region or get_region()
        self.instance_id = instance_id or get_instance_id()
        self.elb_client = botocore.session.get_session().create_client("elb", region_name=self.region)
        self.logger = logging.getLogger(__name__)
        self.signaller = Signaller(instance_id, region)

    def elb_healthcheck(self, elb_name):
        self.logger.info("trying describe instance health at ELB API")
        result = self.elb_client.describe_instance_health(LoadBalancerName=elb_name, Instances=[{"InstanceId": self.instance_id}])
        state = result["InstanceStates"][0]["State"]
        self.logger.info("ELB state for instance {0}: {1}".format(self.instance_id, state))
        return state == 'InService'

    def wait_for_elb_healthcheck(self, elb_name, timeout_in_seconds):
        for i in range(0, timeout_in_seconds / INTERVAL):
            if self.elb_healthcheck(elb_name):
                return self.signaller.signal(self.logical_resource_id, self.stack_name, True)
            else:
                sleep(INTERVAL)

        return self.signaller.signal(self.logical_resource_id, self.stack_name, False)

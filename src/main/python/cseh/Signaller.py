import logging

import botocore.session
from cseh import get_region, get_instance_id


class Signaller(object):
    def __init__(self, instance_id=None, region=None):
        self.region = region or get_region()
        self.instance_id = instance_id or get_instance_id()
        self.cfn_client = botocore.session.get_session().create_client("cloudformation", region_name=self.region)
        self.logger = logging.getLogger(__name__)

    def signal(self, logical_resource_id, stack_name, healthy=True):
        if self.cfn_client.describe_stacks(StackName=stack_name)["Stacks"][0]["StackStatus"] == "UPDATE_COMPLETE":
            self.logger.info("Stack: {0} already in state UPDATE_COMPLETE, skipping signalling".format(stack_name))
            return

        status = "SUCCESS" if healthy else "FAILURE"
        self.logger.info("Signalling: {0} resource: {1} in stack: {2}".format(
            status, logical_resource_id, stack_name))
        return self.cfn_client.signal_resource(LogicalResourceId=logical_resource_id,
                                               StackName=stack_name,
                                               Status=status,
                                               UniqueId=self.instance_id)

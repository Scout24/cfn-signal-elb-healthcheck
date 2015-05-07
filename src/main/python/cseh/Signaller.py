import logging

import botocore.session
from cseh import get_region


class Signaller(object):

    def __init__(self, region=None):
        self.region = region or get_region()
        self.cfn_client = botocore.session.get_session().create_client('cloudformation', region_name=self.region)

    def signal(self, logical_resource_id, stack_name, instance_id, healthy=True):
        self.cfn_client.signal_resource(LogicalResourceId=logical_resource_id,
                                        StackName=stack_name,
                                        Status="SUCCESS" if healthy else "FAILURE",
                                        UniqueId=instance_id)

if  __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S', level=logging.INFO)
    Signaller("eu-west-1").signal("bla", "bla", "bla")
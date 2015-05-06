from boto.cloudformation import connect_to_region
from cseh import get_region


class Signaller(object):

    def __init__(self, region):
        self.region = region if region is not None else get_region()
        self.cfn_conn = connect_to_region(region)

    def signal(self, healthy):
        pass
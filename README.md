# cfn-signal-elb-healthcheck
Useful for using CloudFormation rolling updates on web applications.

*Work in Progress*

Determines instance-id of the instance it is running, monitors the ELB state for this id for some time
and signals CloudFormation either SUCCESS or FAILURE.



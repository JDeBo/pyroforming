#!/usr/bin/env python
from constructs import Construct
from cdktf import App, NamedRemoteWorkspace, TerraformStack, TerraformOutput, RemoteBackend
from cdktf_cdktf_provider_aws import AwsProvider, ec2


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, "AWS", region="us-east-1")
        
        instance = ec2.instance(self, "compute", 
                                ami="ami-0022f774911c1d690",
                                instance_type="t2.micro",
                                )

        TerraformOutput(self, "public_ip",
                        value=instance.public_ip,
                        )

app = App()
stack = MyStack(app, "pyroforming")

RemoteBackend(stack,
              hostname='app.terraform.io',
              organization='jdebo-automation',
              workspaces=NamedRemoteWorkspace('pyroforming')
              )

app.synth()

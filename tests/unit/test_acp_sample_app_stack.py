import aws_cdk as core
import aws_cdk.assertions as assertions

from acp_sample_app.acp_sample_app_stack import AcpSampleAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in acp_sample_app/acp_sample_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AcpSampleAppStack(app, "acp-sample-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

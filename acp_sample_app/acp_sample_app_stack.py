#!/usr/bin/env python3

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,
)
from constructs import Construct
import os


class AcpSampleAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello_world_lambda = self.build_lambda()

        acp_app_apigateway = self.build_apigateway()

        test_api = acp_app_apigateway.root.add_resource('test', default_cors_preflight_options=_apigateway.CorsOptions(
            allow_methods=['GET', 'OPTIONS'],
            allow_origins=_apigateway.Cors.ALL_ORIGINS)
        )

        test_api.add_method(
            'GET',
            _apigateway.LambdaIntegration(
                hello_world_lambda,
                proxy=False,
                integration_responses=[
                    _apigateway.IntegrationResponse(
                        status_code="200",
                        response_parameters={
                            'method.response.header.Access-Control-Allow-Origin': "'*'"
                        }
                    )
                ]
            ),
            method_responses=[
                _apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

    def build_lambda(self) -> _lambda.Function:
        path = os.path
        asset_path = path.join(path.realpath(
            __file__).split(path.sep)[-2], 'lambda')
        hello_world_lambda = _lambda.Function(self, 'helloWorldLambda',
                                              handler='helloWorld.handler',
                                              runtime=_lambda.Runtime.PYTHON_3_12,
                                              code=_lambda.Code.from_asset(asset_path))
        return hello_world_lambda

    def build_apigateway(self) -> _apigateway.RestApi:
        return _apigateway.RestApi(self, 'helloWorldApigateway',
                                   rest_api_name='helloWorldApigateway')

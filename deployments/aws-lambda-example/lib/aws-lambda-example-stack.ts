import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as lambda from "aws-cdk-lib/aws-lambda";

export class AwsLambdaExampleStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'AwsLambdaExampleQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });

    const dockerFunc = new lambda.DockerImageFunction(this, "DockerFunc", {
      code: lambda.DockerImageCode.fromImageAsset("./docker-image"), // Docker image location
      memorySize: 1024, // Memory allocated for the function (1 GB)
      timeout: cdk.Duration.seconds(10), // Function timeout (10 seconds)
      architecture: lambda.Architecture.ARM_64, // Architecture for the Lambda function (ARM 64-bit)
    });

    const functionUrl = dockerFunc.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE, // No authentication is required
      cors: {
        // CORS configuration
        allowedMethods: [lambda.HttpMethod.ALL], // Allows all HTTP methods (GET, POST, etc.)
        allowedHeaders: ["*"], // Allows all headers
        allowedOrigins: ["*"], // Allows all origins (any domain)
      },
    });

    // Using AWS CDK to output the Lambda Function URL after deployment.
    new cdk.CfnOutput(this, "FunctionUrlValue", {
      value: functionUrl.url,
    });
  }
}

# Command line interface for AWS.
The AWS Command Line Interface (AWS CLI) is an open source tool that enables you to interact with AWS services using commands in your command-line shell. 

References:
- https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html

## Install 

### Ubuntu 
`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`
`unzip awscliv2.zip`
`sudo ./aws/install`

### Mac
`curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"`
`sudo installer -pkg AWSCLIV2.pkg -target`
`which aws`

## Configuring settings for AWS CLI
This section explains how to configure the settings that the AWS Command Line Interface (AWS CLI) uses to interact with AWS. These include the following:
- Credentials: identify who is calling the API. Access credentials are used to encrypt the request to the AWS servers to confirm your identity and retrieve associated permissions policies. These permissions determine the actions you can perform. 
- Other configuration details to tell the AWS CLI how to process requests, such as the default output format and the default AWS Region.

https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html

 - First generate keys as shown in the video https://www.youtube.com/watch?v=pEUuJiIGtqk&list=PLqoUmUbJ_zDHPwK-ZWATXiYrUXwWkLY65&index=5
   - Go to IAM -> Users -> vivek -> Security credentials -> Create access key
 - `aws configure` and the fill in the keys as asked.


Uses:

#### List spaces
`aws sagemaker list-spaces --region us-east-1`

#### Describe a space
`aws sagemaker describe-space \
  --domain-id d-cgsnsysn4who \
  --space-name CanvasManagedSpace-cde4218fe3419915b1f416842bcd0af1 \
  --region us-east-1`

#### list apps
`aws sagemaker list-apps \
  --domain-id-equals d-cgsnsysn4who \
  --region us-east-1`

#### Delete an app
`aws sagemaker delete-app \
  --domain-id d-cgsnsysn4who \
  --user-profile-name user-profile-vivek-usaeast1 \
  --app-name default \
  --app-type Canvas \
  --region us-east-1`

#### Delete a space
`aws sagemaker delete-space \
  --domain-id d-cgsnsysn4who \
  --space-name CanvasManagedSpace-cde4218fe3419915b1f416842bcd0af1 \
  --region us-east-1`

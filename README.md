

#### Video and Blog Link References
 For Learning

 - Github: https://github.com/aws/amazon-sagemaker-examples/tree/main/end_to_end/fraud_detection
 - Be Better Dev, Youtube Channel: https://www.youtube.com/@BeABetterDev
 - 


### AWS Accounts:
 - Root Account: Has full administrative access to all AWS services and resources in the account.
   - It can revoke access to any other account in the root account.
   - It can create new IAM users, groups, and roles.
 - IAM User: Has limited access to AWS services and resources in the account.

When you first sign up on aws you create a root account, then there you can create a IAM account. 
Always use IAM account for day to day work. Never use root account for day to day work. Root account should 
be used only for billing and creating new IAM accounts.

### IAM Core Concepts:
Identity an Access Management (IAM) is a web service that helps you securely control access to AWS resources. '
Resources are the things you create in AWS, such as EC2 instances, S3 buckets, and RDS databases. Users attempts to perform
"Actions" on resources i.e. S3::CreateBucket. Authorization to perform an Action depends on a policy. A policy is json file 
that defines what different users can perform differnt actions.

    - Users: End users such as employees of an organization.
    - Groups: A collection of users under one set of permissions. i.e. Group Admins, Group Developers, Group Testers.
    - Roles: A way to delegate permissions to users or services. A role can be assumed by an entity i.e. user or service.
    - Policies: A document that defines permissions.
    - Trust Relationship: A trust relationship is a configuration in which one entity grants permissions to another entity to 
      assume a role. The entity that grants the permission is the trustor, and the entity that receives the permission is the 
      trustee. The trustor and trustee can be AWS accounts or IAM roles.

For example, a user wants to access an S3 bucket, the user needs to have a policy that allows the user to access the S3 bucket.
The policy can be attached to the user, group, or role. Also a user can assume the role to access the S3 bucket.

The policy can be inline or managed. Managed policies are policies that
are created and managed by AWS. Inline policies are policies that are created and managed by the user.

Ways that a user can interect with AWS services?
- AWS console that you will use your account_id, username and password to login.
- AWS CLI that you will use your access_key_id and secret_access_key to login.
- AWS SDK that you will use your access_key_id and secret_access_key to login.

Pro Tips

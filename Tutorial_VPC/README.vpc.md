
## AWS Networking
references:
 - AWS docs: https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
 - Travis Media Youtube: https://www.youtube.com/watch?v=2doSoMN2xvI

### VPC - Virtual Private Cloud.
A VPC is a virtual network that closely resembles a traditional network that you'd operate in your own data center.
After you create a VPC, you can add subnets.
It is logically isolated from other  virtual networks in the AWS cloud. 
You can launch your AWS resources, such  as Amazon EC2 instances, into your VPC.

### Subnet
A subnet is a range of IP addresses in your VPC. A subnet must reside in a single Availability Zone. 
After you add subnets, you can deploy AWS resources in your VPC.
 - A public subnet: can be access from public IPs (out of VPC). SSH. HTTP
 - A private subnet: can't be access from public IPs (out of VPC). Can only be access from other subnets in the VPC.


### Internet Gateway
A gateway connect your vpc to other networks, i.e. internet gateway connects the VPC to the internet.



For aws networking, when you are not able to access a resource from public ip, follow
following steps
- Create A vpc for a region. 
- Create a subnet in the vpc for different availability zone.
  - Create a public subnet by allowing enable auto-assign public ip. and provide a range of ip.
  - Create a private subnet by disabling auto-assign public ip.
- Create a internet gateway and attach it to the vpc.
- Create a route table, add vpc, go to subnet association, edit subnet association, select the subnet for the route table.
- Now go to the routes in the route table. Edit Routes, add a route, destination=0.0.0.0/0, target=Internet Gateway.
- And now you can access any service or EC2 instance from public ip.

## Docker and Deploy to AWS.


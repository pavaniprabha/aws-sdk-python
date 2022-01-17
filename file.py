import boto3

ec2 = boto3.resource('ec2')

class aws:
     @staticmethod
     
    #-----------------------creating  a VPC--------------------------------------
     def vpc():
        try:
            global  vpc
            vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
            vpc.create_tags(Tags=[{"Key": "Name", "Value": "my_vpc_sdk"}])
            print(vpc.id+ "Vpc created")
        except Exception as err:
            print(err, "error occured in vpc..........")

    #-----------------------creating an InternetGateway----------------------------
     def internetGateway():
        try:
            global internetgateway
            internetgateway = ec2.create_internet_gateway()
            internetgateway.create_tags(Tags=[{"Key": "Name", "Value": "IGW"}])
            vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)
            print(internetgateway.id+ "InternetGateWayId")
            return internetgateway.id
        except Exception as err:
            print(err, "error occured in internet-gateway............")
    #-----------------------creating Subnet------------------------------------
     def subnet():
            try:
                global public_subnet
                global private_subnet
                public_subnet= ec2.create_subnet(VpcId = vpc.id , CidrBlock = "10.0.0.0/17" , AvailabilityZone = "ap-south-1a")
                public_subnet.create_tags(Tags=[{"Key": "Name", "Value": "public_subnet_sdk"}])
                print(public_subnet.id+ "public subnet is created")
                private_subnet= ec2.create_subnet(VpcId = vpc.id , CidrBlock = "10.0.128.0/17" , AvailabilityZone = "ap-south-1b")
                private_subnet.create_tags(Tags=[{"Key": "Name", "Value": "private_subnet_sdk"}])
                print(private_subnet.id+ "private subnet is created")
                return public_subnet.id
            except Exception as err:
                print(err, "error occured in subnet.................")
    #-----------------------creating a route_table------------------------------
     def routetable():
            try:
                routetable = vpc.create_route_table()
                route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)
                routetable.associate_with_subnet(SubnetId=public_subnet.id)
                print(routetable.id+ "Route table created")
            except Exception as err:
                    print(err, "error occured in routetable.................")
    #-----------------------creating an security group----------------------------
     def security_group():
             try:
                global securitygroup
                securitygroup = ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=vpc.id)
                securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
                securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=8000, ToPort=8000)
                securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=80, ToPort=80)

                print(securitygroup.id+ "security group created")
             except Exception as err:
                    print(err, "error occured in securitygroup.................")
    #----------------------- launching an ec2-instance-----------------------------
     def  ec2_instance():
                try:
                    instances = ec2.create_instances(
                    ImageId='ami-08ee6644906ff4d6c',
                    InstanceType='t2.micro',
                    MaxCount=1,
                    MinCount=1,
                    NetworkInterfaces=[{
                    'SubnetId': public_subnet.id,
                    'DeviceIndex': 0,
                    'AssociatePublicIpAddress': True,
                    'Groups': [securitygroup.group_id]
                     }],
                    KeyName='frontend')
                    print(str(instances.id)+ "instance is launched" )
                except Exception as err:
                    print(err, "error occured in instance.............")

aws.vpc()
aws.internetGateway()
aws.subnet()
aws.routetable()
aws.security_group()
aws.ec2_instance()
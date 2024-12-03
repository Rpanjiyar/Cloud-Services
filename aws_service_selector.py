import boto3
import random
import string
import time
from datetime import datetime, timedelta

# AWS Clients
iam_client = boto3.client('iam')
sts_client = boto3.client('sts')

# List of Supported Services
SUPPORTED_SERVICES = [
    "Amazon EC2", "Amazon S3", "Amazon RDS", "Amazon DynamoDB",
    "AWS Lambda", "Amazon CloudWatch", "Amazon VPC", "AWS IAM",
    "Amazon API Gateway", "Amazon Route 53", "AWS Elastic Beanstalk",
    "Amazon SNS", "Amazon SQS", "AWS CloudFormation", "AWS Glue",
    "AWS Step Functions", "Amazon Redshift"
]

def get_account_id():
    """Retrieve AWS account ID."""
    try:
        return sts_client.get_caller_identity()["Account"]
    except Exception as e:
        print(f"Error retrieving account ID: {e}")
        return None

def generate_password():
    """Generate a random password for IAM users."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))

def create_iam_user(user_name, account_id):
    """Create an IAM user and return credentials."""
    try:
        # Create IAM user
        iam_client.create_user(UserName=user_name)

        # Create login profile for console access
        password = generate_password()
        iam_client.create_login_profile(
            UserName=user_name,
            Password=password,
            PasswordResetRequired=False
        )

        # Attach policies
        iam_client.attach_user_policy(
            UserName=user_name,
            PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
        )

        # Generate access keys
        keys = iam_client.create_access_key(UserName=user_name)

        login_url = f"https://{account_id}.signin.aws.amazon.com/console"

        return {
            "UserName": user_name,
            "Password": password,
            "AccessKeyId": keys["AccessKey"]["AccessKeyId"],
            "SecretAccessKey": keys["AccessKey"]["SecretAccessKey"],
            "AccountId": account_id,
            "LoginURL": login_url
        }
    except Exception as e:
        print(f"Error creating IAM user {user_name}: {e}")
        return None

def deploy_service(service_name, iam_user):
    """Simulate the deployment of AWS services for a given IAM user."""
    print(f"Deploying {service_name} for user {iam_user['UserName']}...")
    if service_name == "Amazon EC2":
        print(f"Simulated EC2 instance deployment for user {iam_user['UserName']}.")
    elif service_name == "Amazon S3":
        bucket_name = f"user-{iam_user['UserName']}-bucket-{random.randint(1000, 9999)}"
        print(f"Simulated S3 bucket creation: {bucket_name}.")
    else:
        print(f"{service_name} deployment simulation completed.")

def display_iam_details(users):
    """Display IAM user credentials in the Bash console."""
    print("\nIAM User Details:")
    print("=" * 50)
    for user in users:
        print(f"User Name: {user['UserName']}")
        print(f"Password: {user['Password']}")
        print(f"Access Key ID: {user['AccessKeyId']}")
        print(f"Secret Access Key: {user['SecretAccessKey']}")
        print(f"Account ID: {user['AccountId']}")
        print(f"Login URL: {user['LoginURL']}")
        print("=" * 50)

def main():
    print("Supported AWS Services:")
    for idx, service in enumerate(SUPPORTED_SERVICES, start=1):
        print(f"{idx}. {service}")
    print("\nEnter the numbers of the services to deploy (comma-separated, e.g., 1,2,5):")
    services_input = input("Services: ").strip()
    
    try:
        selected_indices = [int(i.strip()) - 1 for i in services_input.split(",")]
        selected_services = [SUPPORTED_SERVICES[i] for i in selected_indices if 0 <= i < len(SUPPORTED_SERVICES)]
    except ValueError:
        print("Invalid input. Please enter valid service numbers.")
        return
    
    if not selected_services:
        print("No services selected. Exiting.")
        return

    iam_user_count = int(input("Enter the number of IAM users to create: "))
    duration_days = int(input("Enter the number of days to run services: "))
    duration_hours = int(input("Enter the number of hours to run services: "))

    account_id = get_account_id()
    if not account_id:
        print("Unable to retrieve AWS account ID. Exiting.")
        return

    users = []
    for i in range(iam_user_count):
        user_name = f"user-{i+1}"
        credentials = create_iam_user(user_name, account_id)
        if credentials:
            users.append(credentials)

    # Display IAM user details
    display_iam_details(users)

    # Deploy services for each IAM user
    for user in users:
        for service in selected_services:
            deploy_service(service, user)

    # Simulate resource lifecycle
    end_time = datetime.now() + timedelta(days=duration_days, hours=duration_hours)
    print(f"\nResources will run until: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while datetime.now() < end_time:
        time.sleep(10)  # Simulating active resources

    print("\nTime's up! Cleaning up IAM users...")

    # Delete IAM users
    for user in users:
        try:
            iam_client.delete_user(UserName=user["UserName"])
            print(f"Deleted IAM user: {user['UserName']}")
        except Exception as e:
            print(f"Error deleting IAM user {user['UserName']}: {e}")

    print("\nCleanup completed.")

if __name__ == "__main__":
    main()

import random
import string
import time
from datetime import datetime, timedelta
from aliyunsdkcore.client import AcsClient
from aliyunsdkram.request.v20150501.CreateUserRequest import CreateUserRequest
from aliyunsdkram.request.v20150501.CreateAccessKeyRequest import CreateAccessKeyRequest
from aliyunsdkram.request.v20150501.AttachPolicyToUserRequest import AttachPolicyToUserRequest
from aliyunsdkram.request.v20150501.DeleteUserRequest import DeleteUserRequest
from aliyunsdkram.request.v20150501.DeleteAccessKeyRequest import DeleteAccessKeyRequest

# Configuration
ACCESS_KEY_ID = "your-access-key-id"
ACCESS_KEY_SECRET = "your-access-key-secret"
REGION_ID = "cn-hangzhou"  # Change to your desired region

# Supported Alibaba Cloud Services
SUPPORTED_SERVICES = [
    "Elastic Compute Service (ECS)", "Object Storage Service (OSS)",
    "ApsaraDB RDS", "Alibaba Cloud Function Compute",
    "Alibaba Cloud Monitoring", "Alibaba Cloud VPC",
    "Alibaba Cloud CDN", "Alibaba Cloud Message Queue"
]

# Initialize Alibaba Cloud client
client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)


def generate_password():
    """Generate a random password for RAM users."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))


def create_ram_user(user_name):
    """Create a RAM user and generate access keys."""
    try:
        # Create RAM user
        request = CreateUserRequest()
        request.set_UserName(user_name)
        request.set_DisplayName(user_name)
        response = client.do_action_with_exception(request)
        print(f"Created RAM user: {user_name}")

        # Create Access Key
        access_key_request = CreateAccessKeyRequest()
        access_key_request.set_UserName(user_name)
        access_key_response = client.do_action_with_exception(access_key_request)
        access_key_data = eval(access_key_response)  # Convert byte response to dict

        return {
            "UserName": user_name,
            "AccessKeyId": access_key_data["AccessKey"]["AccessKeyId"],
            "AccessKeySecret": access_key_data["AccessKey"]["AccessKeySecret"]
        }
    except Exception as e:
        print(f"Error creating RAM user {user_name}: {e}")
        return None


def assign_policy_to_user(user_name, policy_name="AliyunFullAccess"):
    """Assign a policy to a RAM user."""
    try:
        request = AttachPolicyToUserRequest()
        request.set_PolicyType("System")  # Use "System" for Alibaba Cloud predefined policies
        request.set_PolicyName(policy_name)
        request.set_UserName(user_name)
        client.do_action_with_exception(request)
        print(f"Assigned policy {policy_name} to user {user_name}.")
    except Exception as e:
        print(f"Error assigning policy to user {user_name}: {e}")


def deploy_service(service_name, user_name):
    """Simulate the deployment of Alibaba Cloud services."""
    print(f"Deploying {service_name} for user {user_name}...")
    if service_name == "Elastic Compute Service (ECS)":
        print(f"Simulated ECS instance deployment for user {user_name}.")
    elif service_name == "Object Storage Service (OSS)":
        bucket_name = f"user-{user_name}-bucket-{random.randint(1000, 9999)}"
        print(f"Simulated OSS bucket creation: {bucket_name}.")
    else:
        print(f"{service_name} deployment simulation completed.")


def delete_ram_user(user_name):
    """Delete a RAM user and associated access keys."""
    try:
        # Delete Access Key
        access_key_request = DeleteAccessKeyRequest()
        access_key_request.set_UserName(user_name)
        client.do_action_with_exception(access_key_request)

        # Delete User
        delete_user_request = DeleteUserRequest()
        delete_user_request.set_UserName(user_name)
        client.do_action_with_exception(delete_user_request)

        print(f"Deleted RAM user: {user_name}")
    except Exception as e:
        print(f"Error deleting RAM user {user_name}: {e}")


def display_ram_user_details(users):
    """Display RAM user credentials."""
    print("\nRAM User Details:")
    print("=" * 50)
    for user in users:
        print(f"User Name: {user['UserName']}")
        print(f"Access Key ID: {user['AccessKeyId']}")
        print(f"Access Key Secret: {user['AccessKeySecret']}")
        print("=" * 50)


def main():
    print("Supported Alibaba Cloud Services:")
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

    ram_user_count = int(input("Enter the number of RAM users to create: "))
    duration_days = int(input("Enter the number of days to run services: "))
    duration_hours = int(input("Enter the number of hours to run services: "))

    users = []
    for i in range(ram_user_count):
        user_name = f"user-{i+1}"
        credentials = create_ram_user(user_name)
        if credentials:
            assign_policy_to_user(user_name)
            users.append(credentials)

    # Display RAM user details
    display_ram_user_details(users)

    # Deploy services for each RAM user
    for user in users:
        for service in selected_services:
            deploy_service(service, user["UserName"])

    # Simulate resource lifecycle
    end_time = datetime.now() + timedelta(days=duration_days, hours=duration_hours)
    print(f"\nResources will run until: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while datetime.now() < end_time:
        time.sleep(10)  # Simulating active resources

    print("\nTime's up! Cleaning up RAM users...")

    # Delete RAM users
    for user in users:
        delete_ram_user(user["UserName"])

    print("\nCleanup completed.")

if __name__ == "__main__":
    main()

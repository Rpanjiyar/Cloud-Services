import random
import string
import time
from datetime import datetime, timedelta
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import IamIdentityV1, ResourceControllerV2

# Constants
IBM_API_KEY = "your-ibm-api-key"
IBM_RESOURCE_GROUP = "your-resource-group-id"
IBM_REGION = "us-south"  # Replace with your region

# Supported IBM Cloud Services
SUPPORTED_SERVICES = [
    "IBM Cloud Object Storage", "IBM Cloud Kubernetes Service",
    "IBM Cloud Databases", "IBM Watson Assistant",
    "IBM Cloud Functions", "IBM Cloud Monitoring",
    "IBM Cloud Internet Services", "IBM Cloud Virtual Servers"
]

# Authenticate with IAM
authenticator = IAMAuthenticator(IBM_API_KEY)
iam_client = IamIdentityV1(authenticator=authenticator)
resource_controller = ResourceControllerV2(authenticator=authenticator)

def generate_password():
    """Generate a random password for IAM users."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))

def create_iam_user(user_name):
    """Create an API key for an IAM user."""
    try:
        response = iam_client.create_api_key(
            name=f"{user_name}-apikey",
            iam_id=user_name,
            description=f"API key for {user_name}"
        ).get_result()
        print(f"API key created for user {user_name}.")
        return response
    except Exception as e:
        print(f"Error creating API key for {user_name}: {e}")
        return None

def assign_service_role(api_key_id, service_name):
    """Simulate assigning a role to a user for a service."""
    print(f"Assigning role for service {service_name} using API key {api_key_id}...")
    # Simulate role assignment
    print(f"Role assigned for {service_name}.")

def deploy_service(service_name, user_name):
    """Simulate the deployment of IBM Cloud services."""
    print(f"Deploying {service_name} for user {user_name}...")
    if service_name == "IBM Cloud Object Storage":
        bucket_name = f"user-{user_name}-bucket-{random.randint(1000, 9999)}"
        print(f"Simulated Cloud Object Storage bucket creation: {bucket_name}.")
    elif service_name == "IBM Cloud Virtual Servers":
        print(f"Simulated Virtual Server deployment for {user_name}.")
    else:
        print(f"{service_name} deployment simulation completed.")

def display_iam_details(users):
    """Display IAM user details."""
    print("\nIAM User Details:")
    print("=" * 50)
    for user in users:
        print(f"User Name: {user['user_name']}")
        print(f"API Key: {user['api_key']}")
        print("=" * 50)

def main():
    print("Supported IBM Cloud Services:")
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

    users = []
    for i in range(iam_user_count):
        user_name = f"user-{i+1}"
        api_key_data = create_iam_user(user_name)
        if api_key_data:
            users.append({
                "user_name": user_name,
                "api_key": api_key_data.get("apikey"),
                "api_key_id": api_key_data.get("id"),
            })

    # Display IAM user details
    display_iam_details(users)

    # Deploy services for each IAM user
    for user in users:
        for service in selected_services:
            deploy_service(service, user["user_name"])

    # Simulate resource lifecycle
    end_time = datetime.now() + timedelta(days=duration_days, hours=duration_hours)
    print(f"\nResources will run until: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while datetime.now() < end_time:
        time.sleep(10)  # Simulating active resources

    print("\nTime's up! Cleaning up IAM users...")

    # Clean up IAM users (delete API keys)
    for user in users:
        try:
            iam_client.delete_api_key(id=user["api_key_id"])
            print(f"Deleted API key for user: {user['user_name']}")
        except Exception as e:
            print(f"Error deleting API key for user {user['user_name']}: {e}")

    print("\nCleanup completed.")

if __name__ == "__main__":
    main()

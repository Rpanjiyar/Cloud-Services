import os
import random
import string
import subprocess
from datetime import datetime, timedelta
import time

# Supported Services (simulated)
SUPPORTED_SERVICES = [
    "Web Server", "Database Server", "File Storage", 
    "Backup Service", "Monitoring Service", "Compute Workload"
]

def generate_password():
    """Generate a random password for local users."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))

def create_local_user(user_name):
    """Create a local user with a generated password."""
    password = generate_password()
    try:
        # Create user (Linux example)
        subprocess.run(['sudo', 'useradd', '-m', user_name], check=True)
        subprocess.run(['sudo', 'chpasswd'], input=f"{user_name}:{password}".encode(), check=True)
        print(f"Created local user: {user_name}")
        return {"UserName": user_name, "Password": password}
    except subprocess.CalledProcessError as e:
        print(f"Error creating user {user_name}: {e}")
        return None

def deploy_service(service_name, user_name):
    """Simulate the deployment of services."""
    print(f"Deploying {service_name} for user {user_name}...")
    if service_name == "Web Server":
        print(f"Simulated web server deployment for user {user_name}.")
    elif service_name == "Database Server":
        print(f"Simulated database server deployment for user {user_name}.")
    elif service_name == "File Storage":
        user_dir = f"/home/{user_name}/storage"
        os.makedirs(user_dir, exist_ok=True)
        print(f"Simulated file storage setup at {user_dir}.")
    else:
        print(f"{service_name} deployment simulation completed.")

def delete_local_user(user_name):
    """Delete a local user."""
    try:
        subprocess.run(['sudo', 'userdel', '-r', user_name], check=True)
        print(f"Deleted local user: {user_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting user {user_name}: {e}")

def display_user_details(users):
    """Display local user credentials."""
    print("\nLocal User Details:")
    print("=" * 50)
    for user in users:
        print(f"User Name: {user['UserName']}")
        print(f"Password: {user['Password']}")
        print("=" * 50)

def main():
    print("Supported Local Server Services:")
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

    user_count = int(input("Enter the number of local users to create: "))
    duration_days = int(input("Enter the number of days to run services: "))
    duration_hours = int(input("Enter the number of hours to run services: "))

    users = []
    for i in range(user_count):
        user_name = f"user-{i+1}"
        credentials = create_local_user(user_name)
        if credentials:
            users.append(credentials)

    # Display user details
    display_user_details(users)

    # Deploy services for each user
    for user in users:
        for service in selected_services:
            deploy_service(service, user["UserName"])

    # Simulate resource lifecycle
    end_time = datetime.now() + timedelta(days=duration_days, hours=duration_hours)
    print(f"\nResources will run until: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while datetime.now() < end_time:
        time.sleep(10)  # Simulating active resources

    print("\nTime's up! Cleaning up local users...")

    # Delete local users
    for user in users:
        delete_local_user(user["UserName"])

    print("\nCleanup completed.")

if __name__ == "__main__":
    main()

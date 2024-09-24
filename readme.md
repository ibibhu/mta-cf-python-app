# Cloud Foundry Python Buildpack MTA-Based Application

This repository contains a Python application designed to run on SAP Cloud Foundry using the Multi-Target Application (MTA) model. The application utilizes the Destination service to connect to external OData services.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Building and Deploying](#building-and-deploying)
- [Running the Application](#running-the-application)
- [Key Concepts](#key-concepts)
- [Folder Structure](#folder-structure)
- [Improvements and TODOs](#improvements-and-todos)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following:
- An SAP Cloud Foundry account with access to a subaccount.
- The Cloud Foundry CLI installed on your machine. Follow [this link](https://docs.cloudfoundry.org/cf-cli/install-go.html) for installation instructions.
- The Multi-Target Application Build Tool (`mbt`) installed. You can download it from the [SAP Help Portal](https://developers.sap.com/tutorials/mta-build-application.html).
- Python (3.x) and pip installed locally for development purposes.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your local environment by creating a `.env` file based on the provided `.env.example` and populating it with appropriate values.

## Setup

1. **Create a Destination Service Instance**:
   - In your SAP Cloud Foundry cockpit, create a Destination service instance with the "lite" plan.
   - Choose the correct space for your application.

2. **Create a Service Key**:
   - After creating the Destination service instance, create a service key for it to retrieve the necessary credentials:
     ```bash
     cf create-service-key <destination-service-instance-name> <service-key-name>
     ```

3. **Fetch the Service Key Credentials**:
   - Retrieve the service key credentials:
     ```bash
     cf service-key <destination-service-instance-name> <service-key-name>
     ```

4. **Bind the Service to Your Application**:
   - Bind the Destination service instance to your application:
     ```bash
     cf bind-service <app-name> <destination-service-instance-name>
     ```

## Building and Deploying

### Building the Application

1. Ensure your project is structured as a Multi-Target Application (MTA) with an appropriate `mta.yaml` file.

2. Run the following command to build your application:
   ```bash
   mbt build
   ```
   This command creates a `.mtar` file in the `mta_archives` directory.

### Deploying the Application

1. Deploy the generated `.mtar` file using the Cloud Foundry CLI:
   ```bash
   cf deploy mta_archives/<your-application-name>.mtar
   ```

## Running the Application

To run the application locally for development, use the following command:
```bash
flask run
```
Ensure that your `.env` file is set up correctly, as it contains necessary configurations for the local environment.

## Key Concepts

### Connecting to Cloud Foundry Services

1. **VCAP_SERVICES**:
   - When a service is bound to your application, Cloud Foundry automatically injects a `VCAP_SERVICES` environment variable. This variable contains configuration details for all bound services, including the Destination service.

2. **Accessing Destination Service**:
   - The application retrieves the service credentials from `VCAP_SERVICES` to authenticate and access the Destination service API.
   - Use the provided service key credentials to obtain an access token and call the Destination service endpoints.

3. **Error Handling**:
   - Ensure to implement error handling to gracefully handle scenarios where services might be unavailable or credentials are incorrect.

## Folder Structure

```
my-flask-app/
│
├── .env                  # Environment variables for local development
├── Procfile              # Process types that should be run for your application
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── mta.yaml              # MTA descriptor file
└── README.md             # This README file
```

### Description of Files:
- **.env**: Environment variables for local development.
- **app.py**: The main Flask application that handles requests and integrates with the Destination service.
- **requirements.txt**: Lists the Python dependencies required by the application.
- **mta.yaml**: The descriptor file that defines the structure of your MTA project.
- **Procfile**: Text file used by Cloud Foundry to declare the process types that should be run for your application.
- **.env**: The `.env` file is used to define environment variables that are loaded into the application at runtime. It is particularly useful for storing    sensitive information such as API keys, client IDs, and secrets. 


### Example .env File

Here is an example of the variables you should include in your `.env` file:

CLIENT_ID= 
CLIENT_SECRET= 
TOKEN_URL=


### Explanation of Variables

- **CLIENT_ID**: The client ID used for authenticating with the Destination service.
- **CLIENT_SECRET**: The client secret associated with the client ID for authentication.
- **TOKEN_URL**: The URL of the OAuth token endpoint from which to obtain an access token.

### Where to Get Values

You can retrieve the values for these variables from the service key of your Destination service instance in SAP Cloud Foundry. After creating the service key, you can run the following command to see the credentials:

```bash
cf service-key <destination-service-instance-name> <service-key-name>
```

Copy the values for clientid, clientsecret, and url from the output, and populate your .env file accordingly.

## Improvements and TODOs

- **Implement mTLS Authentication**: For enhanced security, consider implementing mutual TLS authentication.
- **Error Handling**: Improve error handling by defining specific exceptions.
- **Logging**: Integrate logging for better visibility into application performance.
- **Testing**: Write unit tests for critical components of the application.
- **Documentation**: Expand the documentation to include more detailed usage instructions.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss potential changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Key Changes
- **Installation Section**: Added steps for cloning the repository and installing dependencies.
- **Running Section**: Explained how to run the application locally.
- **Key Concepts Section**: Clarified how to connect to the Cloud Foundry services, focusing on the Destination service.
- **Table of Contents**: Improved navigation with a structured table of contents.

Feel free to modify any part of the `README.md` to fit your specific requirements or style! Let me know if you need further adjustments.
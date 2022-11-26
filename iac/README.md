# Infrastructure as Code

## Terraform (Declarative)

Terraform is an IaC tool that lets you build, change, and version cloud and on-prem resources safely and efficiently.

The configuration files under the folder `iac` describe to Terraform the components needed to run the web application.

In this case, AWS was used to deploy the Docker image of the Web Application using AWS ECS, make sure you're logged in
your AWS account in order to run the following commands.

Terraform flow:

````shell
terraform login     # To login in terraform cloud (optional)
terraform init      # Initialize terraform in current folder
terraform fmt       # Formats terraform files
terraform validate  # Validates terraform files, syntax
terraform plan      # Shows plan (what are the things that will be deployed and what hasn't change from the .tfstate)
terraform apply     # Applies the previous plan
terraform destroy   # Destroys all resources
````

After executing `terraform apply` you will have to wait a couple of minutes for the process to finish. Once everything
is deployed in AWS you will get an output variable, the one under `terraform > outputs.tf` file, the Application Load 
Balancer DNS name. This is the public URL to access the Web Application in any browser.

This whole process is now automatize using GitHub Actions. See the workflow in `.github > workflows > cd_terraform.yaml`
file. It is triggered in every push/pull request and the deployment and .tfstate updated accordingly.

**Deployment architecture:**

![Deployment architecture of the Streaming Monitoring System](../image/deployment.png "Deployment")


#### Useful links:
https://aws.amazon.com/es/blogs/opensource/deploying-python-flask-microservices-to-aws-using-open-source-tools/

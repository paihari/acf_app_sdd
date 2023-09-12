import os
import wmill
import oci


# You can import any PyPi package.
# See here for more info: https://www.windmill.dev/docs/advanced/imports#python

# you can use typed resources by doing a type alias to dict
# postgresql = dict

def stack_placement_compartment_id()
    return "ocid1.compartment.oc1..aaaaaaaazj4nizp2zmgb5takyevh7tn7yovysrosao6ykzt4fxtd2kh3e64q"


def main(
    repository_url = "https://github.com/avaloqcloud/acf_app_sdd",
    branch_name = "main", 
    stack_placement_compartment_id = "ocid1.compartment.oc1..aaaaaaaazj4nizp2zmgb5takyevh7tn7yovysrosao6ykzt4fxtd2kh3e64q",
    stack_name="WINDMILL-OCI-STACK-FROM-GITHUB-RESOURCE-MANAGER",
    stack_description="WINDMILL-OCI-STACK-FROM-GITHUB-RESOURCE-MANAGER",
):
    # retrieve variables, resources, states using the wmill client
    try:
        key_content = wmill.get_variable("f/alpha/oci_key")
    except:
        return {"Error": "Key Content Not Available"}


    try:
        user = wmill.get_variable("f/alpha/oci_user")
    except:
        return {"Error": "User OCID not available"}


    try:
        fingerprint = wmill.get_variable("f/alpha/oci_user_fingerprint")
    except:
        return {"Error": "Finger Print Not Available"}

    try:
        tenancy = wmill.get_variable("f/alpha/oci_tenancy")
    except:
        return {"Error": "Tenancy Not Available"}


    try:
        region = wmill.get_variable("f/alpha/oci_region")
    except:
        return {"Error": "Region Not Available"}


    try:
        github_service_provider = wmill.get_variable("f/alpha/oci_github_service_provider")
    except:
        return {"Error": "OCI GitHub Service  Provider Not Available"}


    config = {
        "user": user,
        "fingerprint": fingerprint,
        "tenancy": tenancy,
        "region": region,
        "key_content": key_content,
    }

    oci.config.validate_config(config)

    resource_manager_client = oci.resource_manager.ResourceManagerClient(config)

    variables = {
        "prt": stack_placement_compartment_id,
        "loc": "eu-zurich-1",
        "org": "Topology",
        "prj": "CI",
        "own": "hariprasad.bantwal@avaloq.com",
        "stg": "DEV",
        "src": "URL",
        "acp": "false",
        "client": "false",
        "capi": "true",
        "cls": "false",
        "cis": "false",
        "pci": "true",
        "c5": "false",
        "itg": "false",
        "inet": "false"

    }

    stack_details = oci.resource_manager.models.CreateStackDetails(compartment_id=stack_placement_compartment_id, 
                                                                   config_source=oci.resource_manager.models.CreateGitConfigSourceDetails(config_source_type="GIT_CONFIG_SOURCE",
                                                                                                                       configuration_source_provider_id=github_service_provider,
                                                                                                                       repository_url=repository_url,
                                                                                                                       branch_name=branch_name),
                                                                   display_name=stack_name,
                                                                   description=stack_description,
                                                                   terraform_version="1.0.x",
                                                                   variables=variables)

    create_stack_response = resource_manager_client.create_stack(stack_details)


    print(f"Stack Created Created")

    return {"RM": create_stack_response}

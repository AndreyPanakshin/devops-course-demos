terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

variable "token" {}
variable "cloud_id" {}
variable "folder_id" {}

provider "yandex" {
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  token     = var.token
  zone = "ru-central1-a" # https://yandex.cloud/ru/docs/overview/concepts/geo-scope
}

resource "yandex_storage_bucket" "demo_bucket" {
  bucket = "bucket-from-terraform"
  grant {
    uri         = "http://acs.amazonaws.com/groups/global/AllUsers"
    permissions = ["READ"]
    type        = "Group"
  }

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}


resource "yandex_storage_object" "index_html" {
  bucket = yandex_storage_bucket.demo_bucket.bucket
  key    = "index.html"
  source = "index.html"
  acl    = "public-read"
  content_type = "text/html"
}

############################################################
# Cloud Function
############################################################

resource "yandex_function" "info_function" {
  name        = "devops-demo-info"
  user_hash   = data.archive_file.function_zip.output_base64sha256
  description = "Returns info for API"
  runtime     = "python39"
  entrypoint  = "index.handler"
  tags        = ["latest"]


  memory = 128
  execution_timeout = 5

  content {
    zip_filename = data.archive_file.function_zip.output_path
  }
}

resource "yandex_function_iam_binding" "function-public-access-binding" {
  function_id = yandex_function.info_function.id
  role        = "serverless.functions.invoker"

  members = [
    "system:allUsers",
  ]
}


# Archive Cloud Function code
data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "function_src"
  output_path = "function.zip"
}

############################################################
# API Gateway
############################################################

resource "yandex_api_gateway" "demo_gateway" {
  name = "devops-demo-gw"

  spec = <<EOF
openapi: 3.0.0
info:
  title: DevOps demo website
  version: 1.0.0
paths:
  /:
    get:
      x-yc-apigateway-integration:
        type: object_storage
        bucket: ${yandex_storage_bucket.demo_bucket.bucket}
        object: index.html
        error_object: error.html
  /api/info:
    get:
      x-yc-apigateway-integration:
        type: cloud_functions
        function_id: ${yandex_function.info_function.id}
        tag: "$latest"
EOF
}

output "gateway_url" {
  value = yandex_api_gateway.demo_gateway.domain
}
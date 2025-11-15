terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  zone = "ru-central1-a" # https://yandex.cloud/ru/docs/overview/concepts/geo-scope
}

resource "yandex_compute_disk" "boot-disk-1" {
  name     = "boot-disk-1"
  type     = "network-hdd"
  zone     = "ru-central1-a"
  size     = "20"
  image_id = "fd84mnbiarffhtfrhnog" # yc compute image list --folder-id standard-images --format json | jq -r '.[] | select(.name == "ubuntu-24-04-lts-v20251006") | .id'
}

resource "yandex_compute_instance" "vm-1" {
  name = "vm-from-terraform"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    disk_id = yandex_compute_disk.boot-disk-1.id
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("terraform_demo_rsa.pub")}"
  }
}

resource "yandex_vpc_network" "network-1" {
  name = "network-from-terraform"
}

resource "yandex_vpc_subnet" "subnet-1" {
  name           = "subnet-from-terraform"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

output "internal_ip_address_vm_1" {
  value = yandex_compute_instance.vm-1.network_interface.0.ip_address
}

output "external_ip_address_vm_1" {
  value = yandex_compute_instance.vm-1.network_interface.0.nat_ip_address
}


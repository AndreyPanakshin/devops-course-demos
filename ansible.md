# Ansible

myhost 192.168.57.1  
demo (ubuntu 24) 192.168.57.5  
slave1 (alpine 3.22) 192.168.57.10  
slave2 (alpine 3.22) 192.168.57.20  

## Добавим ssh ключи на слейвы
```bash
ssh-copy-id slave1@192.168.57.10
ssh-copy-id slave2@192.168.57.20
```

## Ansible на минималках
```bash
ssh slave1@192.168.57.10 'cat /etc/os-release'
ssh slave2@192.168.57.20 'cat /etc/os-release'

ssh slave1@192.168.57.10 'touch ~/file.txt'
ssh slave1@192.168.57.10 'ls -la ~'
```

## Установка Ansible

### Настройка прокси для apt
```bash
sudo tee /etc/apt/apt.conf.d/95proxies > /dev/null <<EOF
Acquire::http::Proxy "http://192.168.57.1:3142/";
Acquire::https::Proxy "http://192.168.57.1:3142/";
EOF
```

### Настройка прокси для pip
```bash
mkdir $HOME/.pip/
tee $HOME/.pip/pip.conf > /dev/null <<EOF
[global]
index-url = http://192.168.57.1:3141/root/pypi/+simple/
trusted-host = 192.168.57.1
EOF
```

### Создание виртуального окружения и установка пакетов
```bash
sudo apt install python3-pip
sudo apt install python3-virtualenv
virtualenv .venv
. .venv/bin/activate
pip install ansible==12.0.0
```

## Базовые команды Ansible

```bash
ansible -m ping localhost

tee hosts.yaml > /dev/null <<EOF
all:
  children:
    slaves:
      hosts:
        slave1:
          ansible_user: slave1
          ansible_host: 192.168.57.10
        slave2:
          ansible_user: slave2
          ansible_host: 192.168.57.20
EOF

ansible -i hosts.yaml -m ping all
ansible -i hosts.yaml -m command -a 'touch new.txt' slave1
ansible -i hosts.yaml -m command -a 'ls' slave1

tee ansible.cfg > /dev/null <<EOF
[defaults]
inventory = ./hosts.yaml
EOF

ansible -m command -a 'ls' slave1

ansible -m command -a 'apk add nginx' slave1 
ansible -m command -a 'whoami' slave1
 
ansible -m command -a 'whoami' -b --become-method=su --ask-become-pass slave1

ansible -m ansible.builtin.lineinfile \
  -a 'path=/etc/apk/repositories line="https://mirror.yandex.ru/mirrors/alpine/v3.22/community" state=present' \
  -b --become-method=su --ask-become-pass slave1

ansible -m ansible.builtin.apk -a "update_cache=yes" \
  -b --become-method=su --ask-become-pass slave1

ansible -m ansible.builtin.apk -a "name=sudo state=present" \
  -b --become-method=su --ask-become-pass slave1

ansible -m ansible.builtin.user -a "name=slave1 groups=wheel append=yes" \
  -b --become-method=su --ask-become-pass slave1

ansible -m ansible.builtin.copy \
  -a 'dest=/etc/sudoers.d/wheel mode=0440 content="%wheel ALL=(ALL) NOPASSWD: ALL\n"' \
  -b --become-method=su --ask-become-pass slave1

ansible -m command -a 'whoami' slave1 -b
ansible -m command -a 'apk add nginx' slave1 -b
```

## Ansible плейбук
```bash
tee playbook.yaml > /dev/null <<EOF
---
- name: Настройка Alpine серверов
  hosts: all
  become: yes
  become_method: su
  vars:
    apk_repo: "https://mirror.yandex.ru/mirrors/alpine/v3.22/community"
    user_name: "{{ ansible_user }}"
  tasks:
    - name: Добавить зеркало community в apk repositories
      ansible.builtin.lineinfile:
        path: /etc/apk/repositories
        line: "{{ apk_repo }}"
        state: present

    - name: Обновить кеш пакетов
      ansible.builtin.apk:
        update_cache: yes
      changed_when: false

    - name: Установить sudo
      ansible.builtin.apk:
        name: sudo
        state: present

    - name: Добавить пользователя в группу wheel
      ansible.builtin.user:
        name: "{{ user_name }}"
        groups: wheel
        append: yes

    - name: Настроить sudo без пароля для группы wheel
      ansible.builtin.copy:
        dest: /etc/sudoers.d/wheel
        mode: '0440'
        content: "%wheel ALL=(ALL) NOPASSWD: ALL\n"

    - name: Установить nginx
      ansible.builtin.apk:
        name: nginx
        state: present

EOF

ansible-playbook playbook.yaml -l slave2 --ask-become-pass
```
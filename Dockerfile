# Dockerfile для построения образа - среды выполнения плэйбука
FROM ubuntu:20.04
RUN apt update
RUN ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN apt install ansible  -y
RUN apt install python3-pip -y
RUN pip install proxmoxer
RUN ansible-galaxy collection install community.general
RUN mkdir ~/.ssh && chmod 700 ~/.ssh

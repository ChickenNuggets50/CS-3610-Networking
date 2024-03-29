#!/bin/bash

# Install
# This part will be done for you on the gitlab-ci.
# You may do it manually on your VM.

## Fedora
# sudo dnf install httpd
# Enable incoming http/https using firewall GUI (optional)

## Debain (just fyi, it will behave differently than the grade container).
# sudo apt install apache2
# Use gufw or ufw to enable incoming http/https (optional)

echo "Runing on OS:"
cat /etc/os-release

if grep 'docker\|lxc' /proc/1/cgroup >/dev/null 2>&1; then
    # Apache on the remote docker container
    # (for grading)

    # Enable and start Apache
    # Since systemctl is not on docker,
    # run apache directly in the background.
    httpd -k start

    # Get the goal_files/ in the right place to be served:
    # Use sudo here
    sudo cp -r goal_files/* /var/www/html/

    # Set permissions for web directories
    sudo chmod -R a+rx /var/www/html/
    sudo chmod -R a+rx /var/www/cgi-bin
    sudo cp -r scripts/* /var/www/cgi-bin
else
    # Apache on your local machine
    # (for easier development)

    # Enable and start Apache
    sudo systemctl enable httpd
    sudo systemctl start httpd

    # Get the goal_files/ in the right place to be served:
    sudo cp -r goal_files/* /var/www/html/

    # Set permissions for web directories
    sudo chmod -R a+rx /var/www/html/
    sudo chmod -R a+rx /var/www/cgi-bin
    sudo cp -r scripts/* /var/www/cgi-bin
fi

#!/bin/bash
# Pterodactyl Clean Script
# Author: CoRamTix
# Purpose: Completely remove Pterodactyl Panel & Wings from VPS and prepare for fresh install

echo '🛑 Stopping services...'
systemctl stop pteroq wings nginx redis mariadb 2>/dev/null

echo '🗑 Removing Panel & Wings files...'
rm -rf /var/www/pterodactyl /etc/pterodactyl /var/lib/pterodactyl
rm -f /etc/systemd/system/pteroq.service /etc/systemd/system/wings.service
rm -f /etc/nginx/sites-enabled/pterodactyl.conf /etc/nginx/sites-available/pterodactyl.conf

echo '🧹 Removing Node.js & Yarn...'
apt purge -y nodejs npm yarn 2>/dev/null

echo '🚀 Starting MariaDB...'
systemctl start mariadb

echo '🗑 Removing old database & user...'
mysql -u root -p -e "DROP DATABASE IF EXISTS panel; DROP USER IF EXISTS 'pterodactyl'@'127.0.0.1'; FLUSH PRIVILEGES;"

echo '🧹 Cleaning system cache...'
apt autoremove -y && apt clean
rm -rf /tmp/* /var/tmp/*

echo '✅ VPS clean complete, starting fresh install...'
bash <(curl -s https://pterodactyl-installer.se)

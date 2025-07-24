sudo dpkg -i install_overwatch.deb
sudo systemctl daemon-reexec
sudo systemctl enable --now install_overwatch-init.service

sudo dpkg -i install-overwatch_1.0.deb
sudo systemctl daemon-reexec
sudo systemctl enable --now install_overwatch-init.service

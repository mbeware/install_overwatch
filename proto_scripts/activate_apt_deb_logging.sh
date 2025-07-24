sudo tee /etc/apt/apt.conf.d/99log-install > /dev/null <<EOF
DPkg::Post-Invoke { "logger -p local1.info '[APT] Installed/Removed packages, command: apt'; echo \"\$(date) APT command run: \$0 \$@\" >> $INSTALL_LOG; }; 
EOF

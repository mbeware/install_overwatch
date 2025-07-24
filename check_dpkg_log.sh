awk '/ install / { print $1, $2, "dpkg", $5 }' /var/log/dpkg.log >> $INSTALL_LOG
# tail -f /var/log/dpkg.log | grep "install "

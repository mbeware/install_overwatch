export INSTALL_LOG="/var/log/app_installs.log"
export CURL_LOG="/var/log/curl_downloads.log"
sudo touch $INSTALL_LOG $CURL_LOG
sudo chmod a+rw $INSTALL_LOG $CURL_LOG

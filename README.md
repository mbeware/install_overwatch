# install_overwatch

Logs installation/removal events across multiple package managers and `curl` commands.

## Installation

```bash
make install
```

---

## Uninstall

```bash
sudo dpkg -r install_overwatch
```

---

## Usage

1. Run 'make install'

---

## Info 

- This replace pip, flatpack, apt, cargo and curl with wrappers
- The log locations are defined/used in these scripts
  - /etc/apt/apt.conf.d/99log-install
  - /usr/lib/install_overwatch/logger.sh
- The default log locations are : 
  - for apt, cargo, pip and flatpack '/var/log/install_overwatch.log'
  - for curl : '/var/log/install_overwatch_curl_downloads.log'
- curl is in a separated log because not all usage of it is to install new applications. 
- the proto_scripts folders is old/test/experimentation stuff. Feel free to NOT look into it... 
- 


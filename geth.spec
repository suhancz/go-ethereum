# Prevent attemts to strip binaries as this is what we want to push.
%global __os_install_post %{nil}

Name:                   ethereum-go
Version:                1.9.25
Release:                1
Summary:                Ethereum Go Toolkit
Packager:               Richard Nason <rnason@clusterfrak.com>
License:                Ethereum
Group:                  System/Base
Vendor:                 Ethereum
Url:                    https://geth.ethereum.org
BuildArch:              x86_64
BuildRoot:              %{_tmppath}/%{name}-%{version}-tmp
# BuildRequires:
# Requires:

%description
Ethereum is a decentralized platform that runs smart contracts, applications that run
 exactly as programmed without possibility of downtime, censorship, fraud or third party interference.

%prep
# There is nothing to prep as we are dealing with pre-built binaries.

%build
# This section will remain empty as we are not compiling anything, just building the RPM

%install

# create directories where the files will be located
mkdir -p $RPM_BUILD_ROOT/usr/local/bin
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system
mkdir -p $RPM_BUILD_ROOT/usr/local/share/info/ethereum

# Deploy the binary files (-m argument = permissions)
install -m 554 $RPM_SOURCE_DIR/geth $RPM_BUILD_ROOT/usr/local/bin/geth
install -m 554 $RPM_SOURCE_DIR/geth.service $RPM_BUILD_ROOT/etc/systemd/system/geth.service
install -m 554 $RPM_SOURCE_DIR/COPYING $RPM_BUILD_ROOT/usr/local/share/info/ethereum/LICENSE

%pre
# Pre install commands or scripts if any

if (( $(ps -ef | grep -v grep | grep geth | wc -l) > 0 ))
then
    echo -e "\n"
    echo -e "============================="
    echo -e "Stoping geth.service"
    echo -e "Initializing Installation..."
    echo -e "============================="
    echo -e "\n"

    # Set variables to check for running unit files
    GETH=`systemctl list-units | grep geth.service`

    # Check and stop geth.service
    if [ -z "$GETH" ]; then
        echo -e "geth.service is not running... "
    else
        sudo systemctl stop geth.service
    fi

else
    echo -e "\n"
    echo -e "========================================="
    echo -e "Existing geth.service not detected.."
    echo -e "Initializing Installation..."
    echo -e "========================================="
    echo -e "\n"
fi

%post
# Post install commands or scripts if any.

FIREWALL=`systemctl list-units | grep firewalld.service`

# Check and amend firewalld.service
if [ -z "$FIREWALL" ]; then
    echo -e "\n"
    echo -e "Firewalld not found skipping step...:"
else
    # Open the ports ethereum needs in order to run
    echo -e "Opening ports 30301 and 30303 on Firewalld"
    firewall-cmd --permanent --add-port=30301/tcp
    firewall-cmd --permanent --add-port=30303/tcp
    firewall-cmd --reload
fi

# Reload the unit file cache
systemctl daemon-reload

echo -e "Enabling geth.service to start on boot:"
sudo systemctl enable geth.service
# sudo systemctl start geth.service

echo -e "\n"
echo -e "======================================================"
echo -e "Ethereum Installation has completed!                  "
echo -e "======================================================"
echo -e "\n"

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_tmppath}/%{name}
rm -rf $RPM_BUILD_ROOT/%{name}

# List files that are deployed to the server.
%files
%defattr(-,root,root)
/usr/local/bin/geth
/etc/systemd/system/geth.service
/usr/local/share/info/ethereum/LICENSE

%changelog
* Sun Feb 21 2021  Akos Balla <akos.balla@sirc.hu>
- New build using ethereum 1.9.25

* Mon Jun 05 2017  Richard Nason <rnason@clusterfrak.com>
- Initial build using ethereum 1.6.5

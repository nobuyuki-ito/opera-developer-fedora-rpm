opera-developer-fedora
======================
### How to Create RPM for Fedora

# download .deb package file from Ubuntu repository
wget http://example.com/somewhere

# build rpm package
rpmbuild -bb opera-developer.spec

# create symlink for udev library
ln -rs /usr/lib64/libudev.so.1.3.2 /usr/lib64/libudev.so.0

# install rpm
rpm -ivh --nodeps opera-developer-24.0.1537.0-0.fc18.x86_64.rpm

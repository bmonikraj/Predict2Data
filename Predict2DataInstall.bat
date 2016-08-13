:: installing the Python and required modules
msiexec /i python2711.msi TARGETDIR=C:\python27 ALLUSERS=1 ADDLOCAL=Extensions
echo Python Installation Complete
setx python "C:\python27"
pip install matplotlib
pip install scipy
pip install numpy
pip install pandas
pip install sklearn
echo All required files installation complete
exit
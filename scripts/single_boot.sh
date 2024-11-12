# login as a root
su -

#generate grub password such as: thisissupersecretgrubpassword
grub-mkpasswd-pbkdf2

#copy password that will look like this: grub.pbkdf2.sha512.10000.<hash>

#open /etc/grub.d/40_custom and add these lines at the end
nano /etc/grub.d/40_custom
set superusers=root
password_pbkdf2 root grub.pbkdf2.sha512.10000.[�] #genearted password

# open /etc/grub.d/10_linux and find line that beggins with CLASS and modify it
nano /etc/grub.d/10_linux
CLASS="--class gnu-linux --class gnu --class os --unrestricted"

#update grub
update-grub
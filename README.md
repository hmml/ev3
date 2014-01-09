Program Lego Mindstorms EV3 with python.
========================================

Updating module on EV3 brick
----------------------------

Configuring key based authorisation. This step is required only once:

	$ ssh root@10.0.1.1 mkdir -p .ssh
	$ cat ~/.ssh/id_rsa.pub | ssh root@10.0.1.1 'cat >> .ssh/authorized_keys'

Whenever you want to update `ev3` module just invoke:

	$ ./update.sh

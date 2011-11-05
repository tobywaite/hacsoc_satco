import os, time, sys

from boto.ec2.connection import EC2Connection
from boto.exception import BotoClientError

AWS_SECRET_KEY_ID = 'AKIAIQPPZD5BNMWR7IOA' # Don't commit your keys to github! This is not a real key.
AWS_SECRET_ACCESS_KEY = 'Mypa3FSJSyzbHil/19FNQzyFbceAoZ4K0075hA0s' # Don't commit your keys to github! This is not a real key.
AWS_UBUNTU_IMAGE_ID = 'ami-2768a64e'

conn = EC2Connection(AWS_SECRET_KEY_ID, AWS_SECRET_ACCESS_KEY)

def main(case_id):
	
        # Create a key-pair for this user and save it in the current directory.
	key_pair = create_key_pair(conn, case_id)
	print 'created keypair: %s' % key_pair

	# find the HacSoc security group
	all_sgs = conn.get_all_security_groups()
	sgs = [sg for sg in all_sgs if sg.name=='HacSoc']

	#create an instance for this user.
	reservation = conn.run_instances(AWS_UBUNTU_IMAGE_ID, key_name=key_pair.name, security_groups=sgs, instance_type='t1.micro')
        instance = reservation.instances[0]

        while not instance.update() == 'running':
            print 'waiting for instance to start...'
            time.sleep(5)

	print "congrats! you're good to go! Please type 'ssh -i %s.pem ubuntu@%s' into your terminal to connect to your EC2 instance!" % (key_pair.name, instance.public_dns_name)

        import mailer
        msg = mailer.Message()
        msg.From = ('toby.waite@case.edu')
        msg.To = ('%s@case.edu' % case_id)
        msg.Subject = ('HacSoc Satco: Your EC2 Server info')
        msg.Body = ("congrats! you're good to go! Download this attachement, then in your favorite terminal, change directories (using the 'cd' command) to the locatino where you downloaded the file. Then type 'chmod 400 %s.pem', followed by 'ssh -i %s.pem ubuntu@%s' to connect to your EC2 instance!" % (key_pair.name, key_pair.name, instance.public_dns_name))
        msg.attach("%s.pem" % case_id)

        sender = mailer.Mailer('smtp.cwru.edu')
        sender.send(msg)

def create_key_pair(conn, key_name):
    print "trying to create keypair for '%s'" % key_name
    try:
        key_pair = conn.create_key_pair(key_name)
        print 'key_pair created on aws as %s' % key_name
        key_pair.save('.')
        print 'key_pair saved locally as %s.pem' % key_name
        return key_pair
    except BotoClientError, e:
        print 'BotoClientError encountered, this keypair exists locally.'
        os.remove('./%s.pem' % key_name)
        print 'local keyfile removed, trying again'
        return create_key_pair(conn, key_name)
    except Exception, e:
        if 'InvalidKeyPair.Duplicate' in [error[0] for error in e.errors]:
            print 'keypair exists on aws. Removing it and trying again'
            conn.delete_key_pair(case_id)
            return create_key_pair(conn, key_name)
        else:
            raise

if __name__ == '__main__':
 
    print sys.argv

    for case_id in sys.argv[1:]:
        main(case_id)

    print "Job Done!"

import paramiko

def get_user_details():
  f1 = open('./vm.txt', 'r')
  content = f1.readlines()
  users = []
  for eachline in content:
    each = eachline.rstrip('\n').split(':')
    users.append(each)
  return users
 
def add_user():
###
#useradd -d /home/<user> -m -s /bin/bash <userid>
   user_list = get_user_details()
   admin = 'abdul'
   adminpass = 'tiger'
   key_file='/home/sabeerz/work/Monday-Reports.pem'
   ssh = paramiko.SSHClient()
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   for ip,user,passwd in user_list:
     #print ">>>%s, >>>%s, >>>%s" % (ip,user,passwd)
     ssh.connect(ip, username=admin, password=adminpass)
     #ssh.connect('x.x.x.x', username='ec2-user', password=None, key_filename=key_file)
     stdin,stdout,stderr = ssh.exec_command("grep %s /etc/passwd" % user)
     name = stdout.read().split(':')[0]
     if name:
       print "server: %s user: %s available" % (ip, user)
     else:
       print "need to create: %s with pass: " % user
       stdin,stdout,stderr = ssh.exec_command("sudo /usr/sbin/useradd -d /home/%s -m -p %s -s /bin/bash %s" % (user,passwd,user))
       #stdin,stdout,stderr = ssh.exec_command("uptime")
       response = stderr.read()
       if response:
         print "err: ", response
       else:
         print "%s user successfully created" % user
   return None

#print get_user_details()
print add_user()
    

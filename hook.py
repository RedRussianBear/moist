from subprocess import call
file = open('/home/moist/git/moist/message.txt', 'w')
file.write("This works!")
file.close()
call(["cd", "/home/moist/git/moist/"])
call(["git", "push"])
from subprocess import Popen, PIPE, STDOUT
p = Popen(['java', '-jar', 'ExtractorPacman.jar'], stdout=PIPE, stderr=STDOUT)
for line in p.stdout:
    print (line.decode('utf-8'),end=" ");

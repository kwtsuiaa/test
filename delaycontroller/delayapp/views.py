from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import mainform
import paramiko
from .models import vm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='/login/')
def index(request):
    print request.method
    if request.method == 'POST':
        form = mainform(request.POST)
        if form.is_valid():
            VM = vm.objects.get(pk=request.POST["Delay_vm"])
            if request.POST["action"] == 'Check':
                command = 'tc qdisc list | grep delay'
                # output= command + '\n'
                output = cmd(VM.hostname, VM.user, VM.password, VM.sshport, command)

                if output == '':
                    output = 'Current delay on '+ VM.name +' is 0ms'
                else:
                    output_word_list = output.split()
                    delaytime = output_word_list[-1]
                    output = 'Current delay on '+ VM.name +' is '+ delaytime
                messages.add_message(request, messages.INFO, output)

            if request.POST["action"] == 'Add':
                command = 'tc qdisc add dev '+ VM.interface +' root netem delay '+request.POST["Delay_Time"]+'ms'
                output = cmd(VM.hostname, VM.user, VM.password, VM.sshport, command)

                if output == '':
                    output = 'Add Successfully'

                messages.add_message(request, messages.INFO, output)

            if request.POST["action"] == 'Remove':
                command = 'tc qdisc del dev '+ VM.interface +' root'
                output = cmd(VM.hostname, VM.user, VM.password, VM.sshport, command)

                if output == '':
                    output = 'Remove Successfully'
                messages.add_message(request, messages.INFO, output)

            return redirect('index')


    else:
        form = mainform
    return render(request, 'index.html', {'form': form})


def cmd(hostname, user, password, sshport, command):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname, sshport, user, password)
    (stdin, stdout, stderr) = s.exec_command(command)
    output = stdout.read()
    output += stderr.read()
    s.close()
    return output

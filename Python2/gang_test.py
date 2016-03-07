

txt = "<vuln-solution>A patch exists and is available via anonymous FTP from 'net-dist.mit.edu' in the directory '/pub/telnet'. \
The patch (which is also included in this message) can be found in the file '/pub/telnet/telnet.patch'. The file '/pub/telnet/telnet.patch.sig' conta</vuln-solution>"

print txt.replace("'", '"')
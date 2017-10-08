import pexpect

COMMAND_PROMPT = "\[PEXPECT\]\$ "


def main():
    child = pexpect.spawn('/bin/sh')
    child.setecho(False)
    child.waitnoecho()
    child.sendline("PS1='[PEXPECT]\$ '")
    r = child.expect([COMMAND_PROMPT, pexpect.EOF, pexpect.TIMEOUT], 2)
    print(r)
    child.sendline('echo pristup21 | sudo -S  readlink /proc/18141/exe || echo n/a; ps u --pid 18141 || echo n/a')
    r = child.expect([COMMAND_PROMPT, pexpect.EOF, pexpect.TIMEOUT], 2)
    print(r)
    lines = child.before.decode('utf-8').split("\n")
    for line in lines:
        print(line)
    child.close()


if __name__ == '__main__':
    main()

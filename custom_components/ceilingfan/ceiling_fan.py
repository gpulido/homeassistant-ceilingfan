from enum import Enum
import paramiko



class CeilingFanCommand(Enum):
    STOP = 0
    SPEED_1 = 1
    SPEED_2 = 2
    SPEED_3 = 3
    SPEED_4 = 4
    SPEED_5 = 5
    SPEED_6 = 6
    REVERSE = 7
    LIGHT = 8

commands = {
        CeilingFanCommand.STOP:"1011001011011011011001001001001011001",                                   
        CeilingFanCommand.SPEED_1:"1011001011011011011001001011001001001",
        CeilingFanCommand.SPEED_2:"1011001011011011011001001011001011001",
        CeilingFanCommand.SPEED_3:"1011001011011011011001011001001001001",
        CeilingFanCommand.SPEED_4:"1011001011011011011001011011001001001",
        CeilingFanCommand.SPEED_5:"1011001011011011011011001001001011001",
        CeilingFanCommand.SPEED_6:"1011001011011011011011001001001001001",                                                
        CeilingFanCommand.REVERSE:"1011001011011011011001001001011001001",
        CeilingFanCommand.LIGHT:"1011001011011011011001001001001001011"
    }



class CeilingFanGateway():
    
    #base_command = "sudo ./rpitx/sendook -f 430000000 -0 300 -1 300 -r 10 -p 10000"
    command_params = "-f 430000000 -0 300 -1 300 -r 10 -p 10000"
    
    def __init__(self, server, username, password, sendook_path = 'rpitx/sendook'):
        self._server = server
        self._username = username
        self._password = password
        self._sendook_path = sendook_path

    def _execute_command(self, command: CeilingFanCommand):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self._server, username=self._username, password=self._password)        
        cmd_to_execute = f"sudo ./{self._sendook_path} {CeilingFanGateway.command_params} {commands[command]}"
        print('sending command: ' + cmd_to_execute)        
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
        stdout=ssh_stdout.readlines()
        ssh.close()
        for line in stdout:
            print(line)        
    
    def turn_light(self):
        self._execute_command(CeilingFanCommand.LIGHT)
        
    def stop_fan(self):
        self._execute_command(CeilingFanCommand.STOP)
    
    def set_fan_speed(self, speed: int):
        #TODO: check right speed
        cmd = CeilingFanCommand(speed)
        self._execute_command(cmd)

    def reverse_fan(self):        
        self._execute_command(CeilingFanCommand.REVERSE)


if __name__ == '__main__':
    gateway = CeilingFanGateway('192.168.1.118', 'pi', 'raspberry')
    gateway.stop_fan()
    gateway.turn_light()
    #gateway.reverse_fan()


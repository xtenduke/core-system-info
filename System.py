import subprocess
import re
import math


class System:

    @staticmethod
    def memory_gb():
        memory_kb = int(System.run_command('grep MemTotal /proc/meminfo', 1, '[0-9]+'))
        return str(math.floor(memory_kb / 1000000))

    @staticmethod
    def core_count():
        return System.run_command('grep \"cpu cores\" /proc/cpuinfo', 1, '\\: (.*)')

    @staticmethod
    def processor_count():
        return System.run_command('grep processor /proc/cpuinfo | wc -l', 0, '')

    @staticmethod
    def cpu_name():
        output = System.run_command('grep \"model name\" /proc/cpuinfo', 1, '\\: (.*)')

        # Needed to tidy up output data
        replacements = [
            ('Intel(R) Core(TM)2 Duo CPU', 'C2D '),
            ('Intel(R) Core(TM)2 Quad CPU', 'C2Q '),
            ('Intel(R) Core(TM) ', ''),
            ('Intel(R) Xeon(R) CPU ', 'Xeon'),
            ('CPU', '')
        ]

        for replacement in replacements:
            if replacement[0] in output:
                output = output.replace(replacement[0], replacement[1])

        return output

    @staticmethod
    def run_command(command, lines, regex):
        result = subprocess.getoutput(command)

        if len(regex) > 0:
            result = re.findall(regex, result)

        if lines > 0:
            result = '\\n'.join(result[:lines])

        if 'Permission denied' in result:
            result = 'err'

        return result

    # Displays
    @staticmethod
    def get_displays():
        # hope we don't need to pull scale factor
        r = 1
        output = subprocess.getoutput('xrandr').splitlines()
        displays = []

        for i, line in enumerate(output, start=1):
            if " connected" in line:
                dimensions = line.split()[-3:]

                width = float(dimensions[0].replace('mm', ''))
                height = float(dimensions[2].replace('mm', ''))
                dimension_mm = ((width ** 2) + (height ** 2)) ** 0.5
                # turn dimens into inches
                dimension_in = str(round(dimension_mm / 25.4, r))

                resolution = output[i].split()[0]
                displays.append([resolution, dimension_in])

        # only support one display
        return displays[0]

    # Disks
    @staticmethod
    def get_disks():
        ignore_size = 31
        output = subprocess.getoutput('lsblk -d -o rota,size').splitlines()[1:]
        disks = []
        for disk in output:
            split = disk.split()
            infoStr = str(split[1]).replace('\'\'', '')
            unit = infoStr[-1]
            sizeStr = infoStr[:-1]

            if unit == 'M':
                size = float(sizeStr) * 1000
            else:
                size = float(sizeStr)

            style = 'SSD' if split[0] == '0' else 'HDD'
            if float(size) > ignore_size:
                disks.append(str(size) + ' ' + style)

        return disks

    # Make
    # REQUIRES ROOT
    @staticmethod
    def get_make():
        output = System.run_command('dmidecode -s system-manufacturer', 0, '')
        return output

    # Model name
    # REQUIRES ROOT
    @staticmethod
    def get_model_name():
        output = System.run_command('dmidecode -s system-version', 0, '')
        return output

    # Serial number
    # REQUIRES ROOT
    @staticmethod
    def get_serial_number():
        output = System.run_command('dmidecode -s system-serial-number', 0, '')
        return output

    # GPU Info
    # REQUIRES package 'glxinfo'
    @staticmethod
    def get_gpu():
        output = System.run_command('glxinfo | grep \'Device\'', 0, 'Device: (.*?) \\(.*')
        return output

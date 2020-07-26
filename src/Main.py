import requests
import os
import time
from dotenv import load_dotenv
from src.system.System import System
# load envvars

load_dotenv()

class Main:
    version = '1.0.0'

    def __init__(self):
        pass

    def run(self):
        display = System.get_displays()

        manuf = System.get_make()
        model = System.get_model_name()
        serial_number = System.get_serial_number()
        cpu = System.cpu_name() + ' ' + System.core_count() + 'c' + System.processor_count() + 't'
        memory_gb = System.memory_gb()
        displays = System.get_displays()
        screen_size = displays[1]
        screen_resolution = displays[0]
        graphics = System.get_gpu()[0]

        diskTypes = []
        diskSizes = []
        disks = System.get_disks()
        for disk in disks:
            split = disk.split()
            diskSizes.append(split[0])
            diskTypes.append(split[1])

        hdd_type = ','.join(diskTypes)
        hdd_gb = ','.join(diskSizes)

        # Print info
        print('Sysytem report begin')
        print('manuf: ' + manuf)
        print('model: ' + model)
        print('S/N: ' + serial_number)
        print('CPU: ' + cpu)
        print('RAM: ' + memory_gb + 'gb')
        print('HDD: ' + ','.join(disks))
        print('DISP: ' + screen_size + '\" ' + screen_resolution)
        print('GPU: ' + graphics)
        print('\n')

        # ask to do other things
        upload = input('Upload report? [Y/n]')
        if upload.lower() in 'y':
            self.send_report(manuf,
                             model,
                             serial_number,
                             cpu,
                             memory_gb,
                             displays,
                             screen_size,
                             graphics,
                             hdd_type,
                             hdd_gb)
        else:
            print('Goodbye')

    # Send report as json body to url specified in env
    def send_report(self, manuf,
                    model,
                    serial_number,
                    cpu,
                    memory_gb,
                    displays,
                    screen_size,
                    graphics,
                    hdd_type,
                    hdd_gb):
        print('Firing request')

        dict = {
            'manuf': manuf,
            'model': model,
            'serial_number': serial_number,
            'cpu': cpu,
            'memory_gb': memory_gb,
            'displays': displays,
            'screen_size': screen_size,
            'graphics': graphics,
            'hdd_type': hdd_type,
            'hdd_gb': hdd_gb,
        }

        start = time.time()
        response = requests.post(
            os.getenv('FUNCTION_APP_URL'),
            json=dict
        )

        print('Completed in ' + str(time.time() - start))

        if response.status_code > 199 & response.status_code < 300:
            print('Successfully sent')
        else:
            print('Something went wrong')
            print('Reason' + response.reason)

        print('Status code', response.status_code)

    def say_hello(self):
        print("""\
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@ ..........  &@@@@@@@@@@/......,&@@@@@@@@@@@@@&&&@@@*******@@@@@@@@@@#********@@@@@@
@@@ ../@@@@@@@@@@@% . @@@,...(@@@@@@@@%....@@@@@@@@@,***,@@@@@@@@,*,@@@***,@@@@@@@@@,***@@
@@/..@@@@@@@@@@@@@@,,,@@...@@@ @@@@@@ @@@...@@@@@@@@,**@@@@@@@@@@@**#@,**@@@@@@@@@@@@@,**@
@@ ..@@@@@@@@@@@@@@@@@@@...@@@   **   @@@@..@@@@@@@@,**@@@@@@@@@@@@@@@,**,,,,,,,**,**,***@
@@ ..@@@@@@@@@@@@@@@@@@@...@@@ @@@@@@ @@@&..@@@@@@@@,**@@@@@@@@@@@@@@@,*,@@@@@@@@@@@@@@@@@
@@@ .(@@@@@@@@@@@@@ ..@@,..@@@@@@@@@@@@@@...@@@@@@@@,**@@@@@@@@@@@@@@@,**@@@@@@@@@@@@@%**@
@@@@ ...  ,*//, . .. @@@@&....&@@@@@@@(... @@,**@@@@,**@@@@@@@@@@@@@@@@%****#%&@@&&#*****@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@""")
        print('CORE SYSTEM INFO')
        print('Version: ' + self.version + '\n')

if __name__ == '__main__':
    main = Main()
    main.say_hello()
    main.run()
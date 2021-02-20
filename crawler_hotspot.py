import subprocess
from random import randint
from time import sleep

SLEEP_TIME = 10


def import_hotspot_codes(filename):
    codes = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            codes.append(line.strip())
    #print('codes:', codes)
    return codes


def hotspot_connect_random(codes):

    disconnect_command = "hotspotshield disconnect"
    status_command = "hotspotshield status"

    disconnected = False

    while not disconnected:
        print(f"Sleeping for {SLEEP_TIME} seconds...")
        sleep(SLEEP_TIME)
        print("Trying to disconnect...")
        try:
            subprocess.check_output(disconnect_command, shell=True, timeout=20)
            disconnected = True
        except Exception as exc:
            print(f"Could not disconnect: {exc}")
    print('Successfully disconnected')

    connected = False
    while not connected:
        print(f"Sleeping for {SLEEP_TIME} seconds...")
        sleep(SLEEP_TIME)
        rand_idx = randint(0, len(codes)-1)
        code = codes[rand_idx]
        print(f"Trying to connect to {code}...")
        conn_command = f"hotspotshield connect {code}"
        try:
            subprocess.check_output(conn_command, shell=True, timeout=20)
            print(f"Sleeping for {SLEEP_TIME/5} seconds...")
            sleep(SLEEP_TIME/5)
            try:
                out = subprocess.check_output(status_command, shell=True, timeout=20)
                out = out.decode('utf-8')
                print(f"Sleeping for {SLEEP_TIME/10} seconds...")
                sleep(SLEEP_TIME/10)
                print('Connection verified:', out)
                connected = True
            except Exception as exc:
                print(f"Could not verify connection to {code}: {exc}")
                continue
        except Exception as exc:
            print(f"Could not connect to {code}: {exc}")
    



def crawl_with_hotspot_shield(base_url, route_id, base_dir):

    command = f"curl '{base_url}/{route_id}' \
    --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'\
    -b cookies.txt -c cookies.txt \
    --dump-header {base_dir}/{route_id}_header.txt \
    > {base_dir}/{route_id}.html"

    err_file = open(f"{base_dir}/{route_id}_logs.txt", 'w')
    out_file = open(base_dir+f"/{route_id}.html", 'w')

    try:
        out = subprocess.check_output(command, shell=True, timeout=20, stderr=err_file)
        #out = out.decode('utf-8')
        #out_file.write(out)

    except subprocess.CalledProcessError as exc:
        print(f"Status: FAILED, code: {exc.returncode}")
        raise
    finally:
        err_file.close()
        out_file.close()




if __name__=='__main__':
    codes = import_hotspot_codes("hotspot_shield_codes.txt")
    hotspot_connect_random(codes)
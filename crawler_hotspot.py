import subprocess
from random import randint
from time import sleep


def import_hotspot_codes(filename):
    codes = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            codes.append(line.strip())
    #print('codes:', codes)
    return codes


def hotspot_disconnect(sleep_time=10):

    disconnect_command = "hotspotshield disconnect"
    disconnected = False

    while not disconnected:
        #print(f"[HOTSPOT_DISCONNECT]: Sleeping for {sleep_time} seconds...")
        sleep(sleep_time)
        print("[HOTSPOT_DISCONNECT]: Trying to disconnect...")
        try:
            subprocess.check_output(disconnect_command, shell=True, timeout=20)
            status_ret = hotspot_status()
            if status_ret is None or status_ret is True:
                print("[HOTSPOT_CONNECT_DISCONNECT]: Failed to disconnect. Keep trying...")
                continue
            disconnected = True
        except Exception as exc:
            print(f"[HOTSPOT_DISCONNECT]: Could not disconnect: {exc}")
            continue

    print('[HOTSPOT_DISCONNECT]: Successfully disconnected')
    return True

def hotspot_connect_random(codes, sleep_time=10):

    connected = False

    while not connected:
        #print(f"[HOTSPOT_CONNECT_RANDOM]: Sleeping for {sleep_time} seconds...")
        sleep(sleep_time)
        rand_idx = randint(0, len(codes)-1)
        code = codes[rand_idx]
        #print(f"[HOTSPOT_CONNECT_RANDOM]: Trying to connect to {code}...")
        conn_command = f"hotspotshield connect {code}"
        try:
            subprocess.check_output(conn_command, shell=True, timeout=20) # conn_command does not return anything. Thus, no need to store to a variable
            status_ret = hotspot_status()
            if status_ret is None or status_ret is False:
                print(f"[HOTSPOT_CONNECT_RANDOM]: Failed to connect to {code}. Trying a new code...")
                continue
            connected = True
        except Exception as exc:
            print(f"[HOTSPOT_CONNECT_RANDOM]: Could not connect to {code}: {exc}")
            continue
    
    print(f"[HOTSPOT_CONNECT_RANDOM]: Connected to {code} successfully!")
    return True


def hotspot_status(sleep_time=10):

    ret_val = None
    status_command = "hotspotshield status"
    #print(f"[HOTSPOT_status]: Sleeping for {sleep_time/2} seconds...")
    sleep(sleep_time/2)
    print(f"[HOTSPOT_STATUS]: Checking status with {status_command}...")
    try:
        status_out = subprocess.check_output(status_command, shell=True, timeout=20)
        status_out = status_out.decode('utf-8')
        print(f"[HOTSPOT_STATUS]: {status_command} returned:\n{status_out}")
        if 'disconnected' in status_out:
            ret_val = False
        else:
            ret_val = True
    except Exception as exc:
        print(f"[HOTSPOT_STATUS]: {status_command} resulted in an error: {exc}")
        raise

    return ret_val
    

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
    '''
    while True: # manual testing
        print("[crawler_hotspot.py]: sleeping for 5 seconds...")
        sleep(5)
        disc_ret = hotspot_disconnect()
        print(f"[crawler_hotspot.py]: disconnect returned: {disc_ret}")
        conn_ret = hotspot_connect_random(codes)
        print(f"[crawler_hotspot.py]: connect returned: {conn_ret}")
    '''
import subprocess

def crawl(base_url, route_id, base_dir, api_key):

    command = f"curl '{base_url}/{route_id}' \
    -U {api_key}: \
    -vx https://proxy.crawlera.com:8013 \
    --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'\
    -b --junk-session-cookies cookies.txt -c cookies.txt"

    err_file = open(f"{base_dir}/{route_id}_logs.txt", 'w')
    out_file = open(base_dir+f"/{route_id}.html", 'w')

    try:
        out = subprocess.check_output(command, shell=True, timeout=20, stderr=err_file)
        out = out.decode('utf-8')
        out_file.write(out)

    except subprocess.CalledProcessError as exc:
        print(f"Status: FAILED, code: {exc.returncode}")
        raise
    finally:
        err_file.close()
        out_file.close()
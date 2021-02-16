import subprocess

def crawl(base_url, route_id, base_dir):

    command = f"curl --location --request GET '{base_url}/{route_id}' \
    --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'"

    err_file = open('errors.txt', 'a')
    out_file = open(base_dir+f"/{route_id}.html", 'w')

    try:
        out = subprocess.check_output(command, shell=True, stderr=err_file)
        out = out.decode('utf-8')
        out_file.write(out)

    except subprocess.CalledProcessError as exc:
        print(f"Status: FAILED, code: {exc.returncode}")
        raise
    finally:
        err_file.close()
        out_file.close()
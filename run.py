import subprocess
from random import randint

BASE_URL = 'https://vrbo.com'
rand_id = randint(100000, 10000000)


def crawl(base_url, route_id):

    command = f"curl --location --request GET '{BASE_URL}/{route_id}' \
    --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'"

    err_file = open('errors.txt', 'w')
    out_file = open(f"{rand_id}.html", 'w')

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


if __name__=='__main__':
    crawl(BASE_URL, rand_id)


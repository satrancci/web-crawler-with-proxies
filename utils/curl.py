'''
Copyright (c) 2021 Alex Ipatov

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


import subprocess

def crawl(base_url, route_id, city, base_dir, api_key):

    '''
    route_id includes '/'
    '''

    if api_key is None:
        command = f"curl '{base_url}{route_id}' \
        --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'\
        -b cookies.txt -c cookies.txt"
    else:
        command = f"curl '{base_url}{route_id}' \
        -U {api_key}: \
        -vx https://proxy.crawlera.com:8013 \
        --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'\
        -b --junk-session-cookies cookies.txt -c cookies.txt"

    err_file = open(f"{base_dir}/{route_id}_{city}_logs.txt", 'w')
    out_file = open(base_dir+f"/{route_id}_{city}.html", 'w')

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
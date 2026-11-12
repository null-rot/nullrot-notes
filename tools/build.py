"""Build every PDF and the web app data for every device (or the ones named).

    python3 build.py              # all devices
    python3 build.py sp404mk2     # just one

Per guide: light A4 booklet, dark A4 booklet, foldable A5 booklet. Then docs/data.js.
Fails if any A4 page's content runs into its footer.
"""
import ast, os, subprocess, sys
sys.path.insert(0, '.')
import devices

PY = sys.executable


def run(*args):
    r = subprocess.run([PY, *args], capture_output=True, text=True, encoding='utf-8')
    sys.stdout.write(r.stdout)
    if r.returncode:
        sys.stderr.write(r.stderr)
        sys.exit(f'failed: {" ".join(args)}')
    return r.stdout


def a4_pdf(html, pdf):
    out = run('topdf.py', f'../build/{html}.html', pdf)
    pages = ast.literal_eval(out.strip().splitlines()[-1])
    bad = [i + 1 for i, (bottom, footer) in enumerate(pages) if bottom >= footer]
    if bad:
        sys.exit(f'overflow: {pdf} page(s) {bad} run into the footer')


def build_device(dev):
    os.makedirs('../build', exist_ok=True)
    os.makedirs('../pdf', exist_ok=True)
    for g in devices.device(dev)['guides']:
        gid = g['id']
        print(f'== {dev} / {gid}')
        run('sheet_a4.py', dev, gid)
        a4_pdf(g['html'], f"../pdf/{g['pdf']}.pdf")
        run('make_dark.py', dev, gid)
        a4_pdf(g['dark_html'], f"../pdf/{g['pdf']}-dark.pdf")
        run('make_a5.py', dev, gid)
        run('impose.py', f"../build/{g['a5_name']}-a5.pdf", f"../pdf/{g['foldable']}.pdf")


if __name__ == '__main__':
    ids = sys.argv[1:] or devices.all_ids()
    for dev in ids:
        build_device(dev)
    # web app data covers every device, even when only some PDFs were rebuilt
    run('extract.py', *devices.all_ids())
    print('done: pdf/ and docs/data.js updated')

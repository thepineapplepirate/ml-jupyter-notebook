# See http://ipython.org/ipython-doc/1/interactive/public_server.html for more information.
# Configuration file for ipython-notebook.
import os
import psutil

c = get_config()
c.NotebookApp.token = ''
c.NotebookApp.password = ''
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = True
c.ServerApp.profile = u'default'
c.IPKernelApp.matplotlib = 'inline'

CORS_ORIGIN = ''
CORS_ORIGIN_HOSTNAME = ''

if os.environ['CORS_ORIGIN'] != 'none':
    CORS_ORIGIN = os.environ.get('CORS_ORIGIN', '')
    CORS_ORIGIN_HOSTNAME = CORS_ORIGIN.split('://')[1]

headers = {
    'X-Frame-Options': 'ALLOWALL',
        'Content-Security-Policy': """
            default-src 'self' %(CORS_ORIGIN)s;
            img-src 'self' %(CORS_ORIGIN)s;
            connect-src 'self' %(WS_CORS_ORIGIN)s;
            style-src 'unsafe-inline' 'self' %(CORS_ORIGIN)s;
            script-src 'unsafe-inline' 'self' %(CORS_ORIGIN)s;
        """ % {'CORS_ORIGIN': CORS_ORIGIN, 'WS_CORS_ORIGIN': 'ws://%s' % CORS_ORIGIN_HOSTNAME}
}

c.NotebookApp.allow_origin = '*'
c.NotebookApp.allow_credentials = True

c.ServerApp.base_url = '%s/ipython/' % os.environ.get('PROXY_PREFIX', '')
c.NotebookApp.tornado_settings = {
    'static_url_prefix': '%s/ipython/static/' % os.environ.get('PROXY_PREFIX', '')
}

if os.environ.get('NOTEBOOK_PASSWORD', 'none') != 'none':
    c.NotebookApp.password = os.environ['NOTEBOOK_PASSWORD']
    del os.environ['NOTEBOOK_PASSWORD']

if CORS_ORIGIN:
    c.NotebookApp.allow_origin = CORS_ORIGIN

# monitor resource usage
c.ResourceUseDisplay.mem_limit = psutil.virtual_memory().total
c.ResourceUseDisplay.track_cpu_percent = True
c.ResourceUseDisplay.cpu_limit = os.cpu_count()

c.NotebookApp.contents_manager_class = "jupytext.TextFileContentsManager"
c.NotebookApp.tornado_settings['headers'] = headers

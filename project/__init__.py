''' server logging '''
import logging
from pathlib import Path


path = Path('.').parent
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    filename=path / 'logs' / 'deploy.log',
                    filemode='w')

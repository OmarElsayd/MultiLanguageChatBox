import logging
import os
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GOOGLE CLOUD INIT")


def _execute_command(command):
    try:
        logger.info("Executing command gcloud")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as error:
        logger.error(f"Command execution failed with return code {error.returncode}")
        raise


class GCloud:
    def __init__(self, project_id=None, account=None):
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        self.account = account or os.getenv('GOOGLE_ACCOUNT')

    def init(self):
        logger.info('Initializing GCloud')
        init_command = f"gcloud init --skip-diagnostics --project={self.project_id} --account={self.account}"
        config_command = f"gcloud config set project {self.project_id}"

        _execute_command(init_command)
        _execute_command(config_command)

import os
import pathlib

from dotenv import load_dotenv


def set_environment(env_name: str = "test_local"):
    """
    Defines the file from which environment variables will be taken
    :param env_name: "dev_remote", "dev_local",
                     "test_local" "test_remote", "prod"
    """
    # Get file_name
    env_file = {"dev_remote": ".dev.remote", "dev_local": ".dev.local",
                "test_local": ".test.local", "test_remote": ".test.remote",
                }

    # Get absolute path to env_file and set it
    env_file_path = os.path.join(pathlib.Path(__file__).parent,
                                 ".env", env_file[env_name])
    load_dotenv(env_file_path, override=True)

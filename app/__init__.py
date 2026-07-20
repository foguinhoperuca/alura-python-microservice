import os

from dotenv import load_dotenv


# env_path = find_dotenv()
# dotenv_values(env_path)
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)

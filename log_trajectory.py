import argparse
import random

from intercode.envs import CTFEnv
from typing import Dict, List


def preprocess_ctf(record: Dict) -> List:
    cmds = [f"cd /ctf/{record['task_id']}"]
    if "setup" in record:
        cmds.append(record["setup"])
    return cmds


CTF_PARAMS = {"image_name": "intercode-ctf", "data_path": "./data/ctf/ic_ctf.json", "preprocess": preprocess_ctf}
CTF_IDS = list(set(range(100)) - {9, 16, 20, 28, 29, 35, 39, 41, 42, 43, 54, 57, 62, 66, 73, 87, 88, 89, 95})
RANDOM_ID = -1


def main(ctf_id: int, log_directory: str):
    if ctf_id == RANDOM_ID:
        ctf_id = random.choice(CTF_IDS)
    else:
        assert ctf_id in CTF_IDS
    log_directory = log_directory or './'

    try:
        env = CTFEnv(traj_dir=log_directory, verbose=True, **CTF_PARAMS)
        env.reset(index=ctf_id)
        done = False

        while not done:
            action = input('> ')
            obs, reward, done, info = env.step(action)

    except KeyboardInterrupt:
        print("Exiting InterCode environment...")
    finally:
        env.close()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('ctf_id', type=int, nargs='?', default=RANDOM_ID, help='Index of the CTF to run. Defaults to random.')
    argparser.add_argument('log_directory', type=str, nargs='?', default='', help='Where to store logs.')
    args = argparser.parse_args()
    main(**vars(args))

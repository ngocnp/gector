import json
from train import main
import argparse


parameters = json.load(open("test/ja_params.json"))
args = argparse.Namespace(**parameters)
main(args)

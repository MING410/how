#!/usr/bin/env python3
import os.path
import sys
import argparse
import ast
from pathlib import Path
import yaml

# Add package root to pythonpath
'''
os.path.dirname(os,path.realname(__file__))：指的是，获得你刚才所引用的模块 所在的绝对路径，__file__为内置属性。 
用__file__ 来获得脚本所在的路径是比较方便的，但这可能得到的是一个相对路径
所以为了得到绝对路径，我们需要 os.path.realpath(__file__)。
print( __file__)
D:/python/file/Demo/practice/test.py
'''
sys.path.append(os.path.realpath(f"{__file__}/../../"))

from how.utils import io_helpers, logging, download
from how.stages import evaluate, train

DATASET_URL = "http://ptak.felk.cvut.cz/personal/toliageo/share/how/dataset/"


def add_parameter_arguments(parser_train, parser_eval):
    """Add arguments to given parsers, enabling to overwrite chosen yaml parameters keys"""

    # Dest parameter must be equal to a key in the yaml parameters, separate nested keys by a dot
    # Type parameter can be used for data conversion
    # Metavar parameter for pretty help printing

    # Train

    # 如果提供dest，例如dest="a"，那么可以通过args.a访问该参数
    parser_train.add_argument("--experiment", "-e", metavar="NAME", dest="experiment")
    parser_train.add_argument("--epochs", metavar="EPOCHS", dest="training.epochs", type=int)
    parser_train.add_argument("--architecture", metavar="ARCH", dest="model.architecture")
    parser_train.add_argument("--skip-layer", metavar="ARCH", dest="model.skip_layer", type=int)
    parser_train.add_argument("--loss-margin", "-lm", metavar="MARGIN", dest="training.loss.margin",
                              type=float)

    # Eval
    parser_eval.add_argument("--experiment", "-e", metavar="NAME", dest="experiment")
    parser_eval.add_argument("--model-load", "-ml", metavar="PATH", dest="demo_eval.net_path")
    parser_eval.add_argument("--features-num", metavar="NUM",
                             dest="evaluation.inference.features_num", type=int)
    parser_eval.add_argument("--scales", metavar="SCALES", dest="evaluation.inference.scales",
                             type=ast.literal_eval)


def main(args):
    """Argument parsing and parameter preparation for the demo"""
    '''
    创建parse：
    1:import argparse
    2：parser = argparse.ArgumentParser()
    3：parser.add_argument()
    4：parser.parse_args()
    '''

    '''
    创建子parse,每个子parse对应自己的输入参数
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')
    # A list command
    list_parser = subparsers.add_parser('list', help='Listcontents')
    list_parser.add_argument('dirname', action='store',    help='Directory tolist')
    list_parse.set_defaults(func=subcmd_list)
    '''
    parser = argparse.ArgumentParser(description="HOW demo replicating results from ECCV 2020.")
    subparsers = parser.add_subparsers(title="command", dest="command")
    parser_train = subparsers.add_parser("train", help="Train demo")
    parser_train.add_argument('parameters', type=str,
                              help="Relative path to a yaml file that contains parameters.")
    parser_eval = subparsers.add_parser("eval", help="Eval demo")
    parser_eval.add_argument('parameters', type=str,
                             help="Relative path to a yaml file that contains parameters.")
    # 上方函数
    add_parameter_arguments(parser_train, parser_eval)
    # parse_args 用来解析
    args = parser.parse_args(args)

    # Load yaml params
    '''
    path.resolve('/foo/bar', './baz') 
     -> '/foo/bar/baz' 
    '''
    package_root = Path(__file__).resolve().parent.parent
    # 父parse可以调用子parse参数？
    parameters_path = args.parameters
    if not parameters_path.endswith(".yml"):
        # *folders ?
        *folders, fname = parameters_path.split(".")
        # ?
        fname = f"{args.command}_{fname}.yml"
        parameters_path = package_root / "examples/params" / "/".join(folders) / fname
    params = io_helpers.load_params(parameters_path)
    # Overlay with command-line arguments

    # vars()将属性/参数和属性值/参数值变为字典输出
    for arg, val in vars(args).items():
        if arg not in {"command", "parameters"} and val is not None:
            io_helpers.dict_deep_set(params, arg.split("."), val)
    # breakpoint()
    # Resolve experiment name
    exp_name = params.pop("experiment")
    if not exp_name:
        exp_name = Path(parameters_path).name[:-len(".yml")]

    # Resolve data folders
    globals = {}
    # args.command=eval or train
    # e.g.  eval_how_r50-_1000.yml
    globals["root_path"] = (package_root / params['demo_%s' % args.command]['data_folder'])
    globals["root_path"].mkdir(parents=True, exist_ok=True)
    _overwrite_cirtorch_path(str(globals['root_path']))
    globals["exp_path"] = (package_root / params['demo_%s' % args.command]['exp_folder']) / exp_name
    globals["exp_path"].mkdir(parents=True, exist_ok=True)
    # Setup logging
    globals["logger"] = logging.init_logger(globals["exp_path"] / f"{args.command}.log")

    # Run demo
    #f-string用大括号 {} 表示被替换字段，其中直接填入替换内容
    io_helpers.save_params(globals["exp_path"] / f"{args.command}_params.yml", params)
    if args.command == "eval":
       # params['evaluation']->params['evaluation']['global(local)_descriptor']['datasets'] 
        download.download_for_eval(params['evaluation'], params['demo_eval'], DATASET_URL, globals)
        evaluate.evaluate_demo(**params, globals=globals)
        print(params['evaluation'])
    elif args.command == "train":
        download.download_for_train(params['validation'], DATASET_URL, globals)
        train.train(**params, globals=globals)


def _overwrite_cirtorch_path(root_path):
    """Hack to fix cirtorch paths"""
    from cirtorch.datasets import traindataset
    from cirtorch.networks import imageretrievalnet

    traindataset.get_data_root = lambda: root_path
    imageretrievalnet.get_data_root = lambda: root_path


if __name__ == "__main__":
    '''
    sys.argv是命令行调用脚本时的参数。
    test.py ab c d
    那么这里的sys.argv[0]是test.py，然后argv[1]是ab，以此类推。
    '''
    main(sys.argv[1:])

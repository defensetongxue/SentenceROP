import argparse,json

def get_config():
    parser = argparse.ArgumentParser()
    # cleansing
    parser.add_argument('--data_path', type=str, default='../autodl-tmp/dataset_ROP',
                        help='Path to the target folder to store the processed datasets.')
    # split
    parser.add_argument('--split_name', type=str, default='1',
                        help='which split to use.')
    
    # Model
    parser.add_argument('--ridge_seg_number', type=int, default=5,
                        help='Name of the model architecture to be used for training.')
    # train and test
    parser.add_argument('--save_dir', type=str, default="./checkpoints",
                        help='Name of the file to save the best model during training.')
    parser.add_argument('--result_path', type=str, default="experiments",
                        help='Path to the visualize result or the pytorch model will be saved.')
    
    # config file 
    parser.add_argument('--cfg', help='experiment configuration filename',
                        default="./configs/defalut.json", type=str)
    
    args = parser.parse_args()
    # Merge args and config file 
    with open(args.cfg,'r') as f:
        args.configs=json.load(f)
    return args
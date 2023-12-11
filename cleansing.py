import os,json
from util.tools  import crop_patches,sample_patch
from configs  import get_config
from PIL import Image
import numpy as np
if __name__ == '__main__':
    args=get_config()
    with open(os.path.join(args.data_path,'annotations.json'),'r') as f:
        data_dict=json.load(f)
    os.makedirs(os.path.join(args.data_path,'stage_sentence'),exist_ok=True)
    os.system(f"rm -rf {os.path.join(args.data_path,'stage_sentence')}/*")
    
    unbalance_sample={
        1:1,
        2:1,
        3:0.5
    }
    
    for image_name in data_dict:
        data=data_dict[image_name]
        if data['stage']<=0:
            continue
        if 'ridge_diffusion_path' in data:
            sample_dense=int(args.sample_dense*unbalance_sample[data['stage']])
            if data['stage'] ==3:
                max_number=100 
                # build abnormal_mask
                abnormal_mask=np.zeros((1200,1600))
                for x,y in data['ridge']["vessel_abnormal_coordinate"]:
                    abnormal_mask[y,x]=1
                
            else:
                max_number=args.max_sample_number
            
            sample_list= sample_patch(data['ridge_diffusion_path'],sample_dense,max_number)
            img=Image.open(data['image_path']).convert("RGB")
            
            save_dir=os.path.join(args.data_path,'stage_sentence',image_name[:-4])
            os.makedirs(save_dir,exist_ok=True)
            
            for cnt,(x,y) in enumerate(sample_list):
                save_path= os.path.join(save_dir,str(cnt)+'.jpg')
                # for convinient the stage is call by save_image name
                # save_path=os.path.join(save_dir,f"{str(patch_stage)}_{image_cnt}.jpg")
                patch_stage=crop_patches(img,args.patch_size,x,y,abnormal_mask,data['stage'],
                            save_dir=save_dir,image_cnt=str(cnt))
            data_dict[image_name]['stage_sentence_path']=save_dir
            
    with open(os.path.join(args.data_path,'annotations.json'),'w') as f:
        json.dump(data_dict,f)
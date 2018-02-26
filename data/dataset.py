import os 
from PIL import Image
import numpy as np 
from torch.utils import data 
from torchvision import transforms as T 

VALIDATE_PERCENT = 0.3

class DogCat(data.Dataset):

    def __init__(self, root, transforms=None, train=True, test=False):
        '''
        获取所有图片的地址，并根据训练、验证、测试划分数据
        '''
        self.test = test
        imgs = [os.path.join(root, img) for img in os.listdir(root)]

        if self.test:
            imgs = sorted(imgs, key=lambda x: int(x.split('.')[-2].split('/')[-1]))
        else:
            imgs = sorted(imgs, key=lambda x: int(x.split('.')[-2]))

        imgs_num = len(imgs)

        if self.test:
            self.imgs = imgs 
        elif train:
            self.imgs = imgs[:int((1-VALIDATE_PERCENT)*imgs_num)]
        else:
            self.imgs = imgs[int((1-VALIDATE_PERCENT)*imgs_num):]

        
        # 数据集拓展，train阶段和test阶段有区别
        if transforms is None:

            normalize = T.Normalize(mean = [0.485, 0.456, 0.406],
                                    std = [0.229, 0.224, 0.225])

            # 测试集和验证集
            if self.test or not train:
                self.transforms = T.Compose([
                    T.Scale(224),
                    T.CenterCrop(224),
                    T.ToTensor(),
                    normalize
                ]) 
            else:
                self.transforms = T.Compose([
                    T.Scale(256),
                    T.RandomSizedCrop(224),
                    T.RandomHorizontalFlip(),
                    T.ToTensor(),
                    normalize
                ]) 


    def __getitem__(self, index):
        '''
        返回一张图片的数据
        对于测试集，没有label，返回图片id，如1000.jpg返回1000
        '''
        img_path = self.imgs[index]
        if self.test:
            label = int(self.imgs[index].split('.')[-2].split('/')[-1])
        else:
            label = 1 if 'dog' in img_path.split('/')[-1] else 0
        data = Image.open(img_path)
        data = self.transforms(data)
        return data, label

    
    def __len__(self):
        '''
            返回数据集中所有图片的个数
        '''
        return len(self.imgs)
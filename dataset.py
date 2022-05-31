import torch
from torch.utils.data import Dataset

from utils import strings_to_images

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class ImageClassifierDataset(Dataset):
    def __init__(self, image_list, transformation):
        image_classes = [
            "men" if "men" in image_list[i] else "women" if "women" in image_list[i] else "other" for i in range(len(image_list))
        ]
        image_list = strings_to_images(image_list)
        self.images = []
        self.labels = []
        self.class_to_label = {"men": 1, "women": 1, "other": 0}
        for image, image_class in zip(image_list, image_classes):
            transformed_image = transformation(image)
            self.images.append(transformed_image)
            label = self.class_to_label[image_class]
            self.labels.append(label)

    def __getitem__(self, index):
        return self.images[index], self.labels[index]

    def __len__(self):
        return len(self.images)
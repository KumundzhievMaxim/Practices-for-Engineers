# ------------------------------------------
# 
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------

import torch.nn as nn
import torchvision.models as models


class ColorNet(nn.Module):
    def __init__(self, input_size=128):
        super(ColorNet, self).__init__()
        mid_level_feature_size = 128

        resnet = models.resnet18(num_classes=365)
        resnet.conv1.weight = nn.Parameter(resnet.conv1.weight.sum(dim=1).unsqueeze(1))
        self.midlevel_resnet = nn.Sequential(*list(resnet.children())[0:6])

        self.upsample = nn.Sequential(
            nn.Conv2d(mid_level_feature_size, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d (128),
            nn.ReLU (),
            nn.Upsample (scale_factor=2),
            nn.Conv2d (128, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d (64),
            nn.ReLU (),
            nn.Conv2d (64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d (64),
            nn.ReLU (),
            nn.Upsample (scale_factor=2),
            nn.Conv2d (64, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d (32),
            nn.ReLU (),
            nn.Conv2d (32, 2, kernel_size=3, stride=1, padding=1),
            nn.Upsample (scale_factor=2)
        )

    def forward(self, input):
        mid_level_features = self.midlevel_resnet(input)
        output = self.upsample(mid_level_features)
        return output



"""Layers producing a 2D attention map from a feature map"""

from torch import nn


class L2Attention(nn.Module):
    def forward(self, x):
        return (x.pow(2.0).sum(1) + 1e-10).sqrt().squeeze(0)
    """Compute the attention as L2-norm of local descriptors"""
'''
pow() 如果接收两个参数，如 pow(x, y)，则结果相当于 x**y，也就是 x 的 y 次方
pow() 如果接收三个参数，如 pow(x, y, z)，则结果相当于 (x**y) % z，也就是 x 的 y 次方再对 z 进行取余

sum(1)列相加
输入是一个两行三列的矩阵[[0,1,2]

                    [2,1,3]]
然后设置axis=1，则计算每一行的向量之和，即为[3,6]
'''
# Inspired by http://libnoise.sourceforge.net/

import cupy as cp
import numpy as np
import math

__BN_X_NOISE_GEN = 1619
__BN_Y_NOISE_GEN = 31337
__BN_Z_NOISE_GEN = 6971
__BN_SEED_NOISE_GEN = 1013
__BN_SHIFT_NOISE_GEN = 8

import random

random.seed(42)
g_randomVectors = []
for i in range(256):
    g_randomVectors.append(random.uniform(-1.0, 1.0))
    g_randomVectors.append(random.uniform(-1.0, 1.0))
    g_randomVectors.append(random.uniform(-1.0, 1.0))
    g_randomVectors.append(0)

g_randomVectors = cp.array(g_randomVectors)

#print(cp.mean(g_randomVectors))

def int_value_noise_3d(x, y, z, seed):
    x = x.astype(int)
    y = y.astype(int)
    z = z.astype(int)
    c = (__BN_X_NOISE_GEN * x) + (__BN_Y_NOISE_GEN * y) + (__BN_Z_NOISE_GEN * z) + __BN_SEED_NOISE_GEN * seed
    c = cp.bitwise_and(c, 0x7fffffff)
    c = cp.bitwise_xor(cp.right_shift(c, 13), c)
    c = cp.bitwise_and((c * (c * c * 60493 + 19990303) + 1376312589), 0x7fffffff)
    return c


def value_noise_3d(icp, seed):
    return 1.0 - int_value_noise_3d(icp[..., 0], icp[..., 1], icp[..., 2], seed) / 1073741824.0


def __NGEN_SCurve5(a):
    a3 = a * a * a
    a4 = a3 * a
    a5 = a4 * a
    return (6.0 * a5) - (15.0 * a4) + (10.0 * a3)


def scale(y):
    return (y - cp.min(y)) / (cp.max(y) - cp.min(y))


def gradient_noise_3d(fx, fy, fz, ix, iy, iz, seed):
    vi = (__BN_X_NOISE_GEN * ix) + (__BN_Y_NOISE_GEN * iy) + (__BN_Z_NOISE_GEN * iz) + __BN_SEED_NOISE_GEN * seed
    vi = cp.bitwise_and(vi, 0xffffffff)
    vi = cp.bitwise_xor(vi, cp.right_shift(vi, __BN_SHIFT_NOISE_GEN))
    vi = cp.bitwise_and(vi, 0xff)

    vi_l2 = cp.left_shift(vi, 2)

    xvGrad = g_randomVectors[vi_l2]
    yvGrad = g_randomVectors[vi_l2 + 1]
    zvGrad = g_randomVectors[vi_l2 + 2]

    xvPoint = fx - ix
    yvPoint = fy - iy
    zvPoint = fz - iz

    return ((xvGrad * xvPoint) + (yvGrad * yvPoint) + (zvGrad * zvPoint)) * 2.12


def linear_interp(n0, n1, a):
    return ((1.0 - a) * n0) + (a * n1)


def gradient_coherent_noise_3d(icp, seed):
    """
    Uses the icput values to generate integer noise using the given seed value


    :param icp: tensor with 3d locations -> [w, h, 3] (xyz)
    :param seed: seed value
    :returns: generated value [w, h, 1]

    """
    if icp.shape[-1] != 3:
        raise ValueError("gradient_coherent_noise_3d icput shape does not fit the 3d description: " + str(icp.shape))
    if icp.dtype != cp.float32 and icp.dtype != cp.float64:
        raise ValueError("gradient_coherent_noise_3d icput type is not f32 or f64: " + str(icp.dtype))
    if not isinstance(seed, int):
        raise ValueError("gradient_coherent_noise_3d seed is not an int")

    x = icp[..., 0]
    y = icp[..., 1]
    z = icp[..., 2]

    x0 = cp.array(x, dtype=int)
    x0[x0 < 0] -= 1
    y0 = cp.array(y, dtype=int)
    y0[y0 < 0] -= 1
    z0 = cp.array(z, dtype=int)
    z0[z0 < 0] -= 1

    x1 = x0 + 1
    y1 = y0 + 1
    z1 = z0 + 1

    xs = __NGEN_SCurve5(x - x0)  # not that idiot from flash, jesus that show sucks...
    ys = __NGEN_SCurve5(y - y0)
    zs = __NGEN_SCurve5(z - z0)

    n0 = gradient_noise_3d(x, y, z, x0, y0, z0, seed)
    n1 = gradient_noise_3d(x, y, z, x1, y0, z0, seed)
    ix0 = linear_interp(n0, n1, xs)
    n0 = gradient_noise_3d(x, y, z, x0, y1, z0, seed)
    n1 = gradient_noise_3d(x, y, z, x1, y1, z0, seed)
    ix1 = linear_interp(n0, n1, xs)
    iy0 = linear_interp(ix0, ix1, ys)
    n0 = gradient_noise_3d(x, y, z, x0, y0, z1, seed)
    n1 = gradient_noise_3d(x, y, z, x1, y0, z1, seed)
    ix0 = linear_interp(n0, n1, xs)
    n0 = gradient_noise_3d(x, y, z, x0, y1, z1, seed)
    n1 = gradient_noise_3d(x, y, z, x1, y1, z1, seed)
    ix1 = linear_interp(n0, n1, xs)
    iy1 = linear_interp(ix0, ix1, ys)

    return linear_interp(iy0, iy1, zs)


def value_coherent_noise_3d(icp, seed):
    """
    Uses the icput values to generate integer noise using the given seed value


    :param icp: tensor with 3d locations -> [w, h, 3] (xyz)
    :param seed: seed value
    :returns: generated value [w, h, 1]

    """
    if icp.shape[-1] != 3:
        raise ValueError("value_coherent_noise_3d icput shape does not fit the 3d description: " + str(icp.shape))
    if icp.dtype != cp.float32 and icp.dtype != cp.float64 and icp.dtype != cp.int:
        raise ValueError("value_coherent_noise_3d icput type is not f32 or f64 or int: " + str(icp.dtype))
    if not isinstance(seed, int):
        raise ValueError("value_coherent_noise_3d seed is not an int")

    x = icp[..., 0]
    y = icp[..., 1]
    z = icp[..., 2]

    icp_int = icp
    icp_int = icp.astype(int)
    icp_int[icp <= 0.0] = (icp_int - 1)[icp <= 0.0]

    x0 = icp_int[..., 0]
    y0 = icp_int[..., 1]
    z0 = icp_int[..., 2]

    x1 = x0 + 1
    y1 = y0 + 1
    z1 = z0 + 1

    xs = __NGEN_SCurve5(x - x0)  # not that idiot from flash, jesus that show sucks...
    ys = __NGEN_SCurve5(y - y0)
    zs = __NGEN_SCurve5(z - z0)

    n0 = int_value_noise_3d(x0, y0, z0, seed)
    n1 = int_value_noise_3d(x1, y0, z0, seed)
    ix0 = linear_interp(n0, n1, xs)
    n0 = int_value_noise_3d(x0, y1, z0, seed)
    n1 = int_value_noise_3d(x1, y1, z0, seed)
    ix1 = linear_interp(n0, n1, xs)
    iy0 = linear_interp(ix0, ix1, ys)
    n0 = int_value_noise_3d(x0, y0, z1, seed)
    n1 = int_value_noise_3d(x1, y0, z1, seed)
    ix0 = linear_interp(n0, n1, xs)
    n0 = int_value_noise_3d(x0, y1, z1, seed)
    n1 = int_value_noise_3d(x1, y1, z1, seed)
    ix1 = linear_interp(n0, n1, xs)
    iy1 = linear_interp(ix0, ix1, ys)
    return linear_interp(iy0, iy1, zs)


def create_point_grid(lu, ru, rd, ld, h, w):
    lu = cp.array(lu)
    ru = cp.array(ru)
    rd = cp.array(rd)
    ld = cp.array(ld)
    indices = cp.indices([w, h, 3])
    ih = indices[0] / (h-1)
    iw = indices[1] / (w-1)
    rows = ((lu + (ru - lu) * iw) + (ld + (rd - ld) * iw)) / 2.0
    rows[..., 1] = 0.0
    cols = ((lu + (ld - lu) * ih) + (ru + (rd - ru) * ih)) / 2.0
    cols[..., 0] = 0.0

    return cols + rows


def perlin(func, icp, seed, octaves, frequency=1.0, lacunarity=2.0, persistance=0.5):
    val_shape = np.array(icp.shape)
    val_shape = val_shape[0:-1]
    value = cp.zeros(val_shape)
    c_per = 1.0

    icp_f = frequency * icp

    for i in range(octaves):
        seed = (seed + i) & 0xffffffff
        value += func(icp_f, seed) * c_per
        icp_f *= lacunarity
        c_per *= persistance

    return value


def rigged_multi(func, icp, seed, octaves, frequency=1.0, lacunarity=2.0, exp=-1.0, gain=2.0, offset=1.0):
    val_shape = np.array(icp.shape)
    val_shape = val_shape[0:-1]
    value = cp.zeros(val_shape)

    icp_f = frequency * icp

    weight = 1.0

    spectral_weights = []

    d_freq = 1.0
    for i in range(octaves):
        spectral_weights.append(math.pow(d_freq, exp))
        d_freq *= lacunarity

    for i in range(octaves):
        seed = (seed + i) & 0x7fffffff

        signal = func(icp_f, seed)

        signal = cp.abs(signal)
        signal = offset - signal

        signal *= signal
        weight *= weight

        weight = signal * gain
        weight[weight>1.0] = 1.0
        weight[weight<0.0] = 0.0

        value += (signal * spectral_weights[i])

        icp_f *= lacunarity

    return value


def voronoi(func, icp, seed, frequency=1.0, displacement=1.0, distance_enabled=False):
    val_shape = np.array(icp.shape)
    val_shape = val_shape[0:-1]
    value = None

    icp_f = frequency * icp

    icp_int = icp_f
    icp_int = icp_f.astype(int)
    icp_int[icp_f <= 0.0] = (icp_int - 1)[icp_f <= 0.0]
    temp = icp_int.copy()

    xInt = icp_int[..., 0]
    yInt = icp_int[..., 1]
    zInt = icp_int[..., 2]

    xc = cp.zeros(xInt.shape)
    yc = cp.zeros(yInt.shape)
    zc = cp.zeros(zInt.shape)

    minDist = cp.ones(val_shape) * 2147483647.0

    for xi in range(-2, 3):
        for yi in range(-2, 3):
            for zi in range(-2, 3):
                xcur = xInt + xi
                ycur = yInt + yi
                zcur = zInt + zi

                temp[..., 0] = xcur
                temp[..., 1] = ycur
                temp[..., 2] = zcur

                xp = xcur + func(temp, seed=seed)
                yp = ycur + func(temp, seed=seed+1)
                zp = zcur + func(temp, seed=seed+2)

                xd = xp - icp_f[..., 0]
                yd = yp - icp_f[..., 1]
                zd = zp - icp_f[..., 2]

                dist = xd * xd + yd * yd + zd * zd

                xc[dist < minDist] = xp[dist < minDist]
                yc[dist < minDist] = yp[dist < minDist]
                zc[dist < minDist] = zp[dist < minDist]
                minDist[dist < minDist] = dist[dist < minDist]
    
    if distance_enabled:
        xd = xc - icp_f[..., 0]
        yd = yc - icp_f[..., 1]
        zd = zc - icp_f[..., 2]
        value = cp.sqrt(xd * xd + yd * yd + zd * zd) * 1.7320508075688772935 - 1.0
    else:
        value = 0.0
    
    temp[..., 0] = cp.floor(xc)
    temp[..., 1] = cp.floor(yc)
    temp[..., 2] = cp.floor(zc)

    return value + displacement * func(temp, seed=0)



if __name__=='__main__':
    print("BASE NOISE TEST")

    import cv2
    x = create_point_grid([0, 0, 0], [0.5, 0, 0], [0.5, 1, 0], [0, 1, 0], 2000, 1000)
    print(x[0, 0])
    print(x[0, 49])
    print(x[49, 49])
    print(x[49, 0])

    y = gradient_coherent_noise_3d(x, 33)
    print(cp.max(y))
    print(cp.min(y))
    y = scale(y)

    cv2.imshow("y", cp.asnumpy(y))
    cv2.waitKey()

    y = value_coherent_noise_3d(x, 33)
    print(cp.max(y))
    print(cp.min(y))
    y = scale(y)

    cv2.imshow("y", cp.asnumpy(y))
    cv2.waitKey()

    def billow(icp, seed):
        return abs(gradient_coherent_noise_3d(icp, seed))

    y = rigged_multi(gradient_coherent_noise_3d, x, 44, 6, frequency=10.0, lacunarity=2.0)
    y += perlin(billow, x, 44, 6, frequency=30.0, lacunarity=2.0)
    print(cp.max(y))
    print(cp.min(y))
    y = scale(y)
    
    cv2.imshow("y", cp.asnumpy(y))
    cv2.waitKey()

    y = voronoi(value_noise_3d, x, 44, frequency=100.0, distance_enabled=True)
    #x1 = create_point_grid([0, 0, 0], [0.5*100, 0, 0], [0.5*100, 1*100, 0], [0, 1*100, 0], 2000, 1000)
    #y = value_noise_3d(x1, 44)
    print(cp.max(y))
    print(cp.min(y))
    y = scale(y)
    

    cv2.imshow("y", cp.asnumpy(y))
    cv2.waitKey()



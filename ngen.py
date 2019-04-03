# Inspired by http://libnoise.sourceforge.net/

import importlib
cp_existance = importlib.util.find_spec('cupy')
if cp_existance:
    import numpy as np
    import cupy as cp
else:
    import numpy as np
    cp = np
import math

__BN_X_NOISE_GEN = 1619
__BN_Y_NOISE_GEN = 31337
__BN_Z_NOISE_GEN = 6971
__BN_SEED_NOISE_GEN = 1013
__BN_SHIFT_NOISE_GEN = 8

import random

random.seed(42)
g_randomVectors = [-0.763874, -0.596439, -0.246489, 0.0,
    0.396055, 0.904518, -0.158073, 0.0,
    -0.499004, -0.8665, -0.0131631, 0.0,
    0.468724, -0.824756, 0.316346, 0.0,
    0.829598, 0.43195, 0.353816, 0.0,
    -0.454473, 0.629497, -0.630228, 0.0,
    -0.162349, -0.869962, -0.465628, 0.0,
    0.932805, 0.253451, 0.256198, 0.0,
    -0.345419, 0.927299, -0.144227, 0.0,
    -0.715026, -0.293698, -0.634413, 0.0,
    -0.245997, 0.717467, -0.651711, 0.0,
    -0.967409, -0.250435, -0.037451, 0.0,
    0.901729, 0.397108, -0.170852, 0.0,
    0.892657, -0.0720622, -0.444938, 0.0,
    0.0260084, -0.0361701, 0.999007, 0.0,
    0.949107, -0.19486, 0.247439, 0.0,
    0.471803, -0.807064, -0.355036, 0.0,
    0.879737, 0.141845, 0.453809, 0.0,
    0.570747, 0.696415, 0.435033, 0.0,
    -0.141751, -0.988233, -0.0574584, 0.0,
    -0.58219, -0.0303005, 0.812488, 0.0,
    -0.60922, 0.239482, -0.755975, 0.0,
    0.299394, -0.197066, -0.933557, 0.0,
    -0.851615, -0.220702, -0.47544, 0.0,
    0.848886, 0.341829, -0.403169, 0.0,
    -0.156129, -0.687241, 0.709453, 0.0,
    -0.665651, 0.626724, 0.405124, 0.0,
    0.595914, -0.674582, 0.43569, 0.0,
    0.171025, -0.509292, 0.843428, 0.0,
    0.78605, 0.536414, -0.307222, 0.0,
    0.18905, -0.791613, 0.581042, 0.0,
    -0.294916, 0.844994, 0.446105, 0.0,
    0.342031, -0.58736, -0.7335, 0.0,
    0.57155, 0.7869, 0.232635, 0.0,
    0.885026, -0.408223, 0.223791, 0.0,
    -0.789518, 0.571645, 0.223347, 0.0,
    0.774571, 0.31566, 0.548087, 0.0,
    -0.79695, -0.0433603, -0.602487, 0.0,
    -0.142425, -0.473249, -0.869339, 0.0,
    -0.0698838, 0.170442, 0.982886, 0.0,
    0.687815, -0.484748, 0.540306, 0.0,
    0.543703, -0.534446, -0.647112, 0.0,
    0.97186, 0.184391, -0.146588, 0.0,
    0.707084, 0.485713, -0.513921, 0.0,
    0.942302, 0.331945, 0.043348, 0.0,
    0.499084, 0.599922, 0.625307, 0.0,
    -0.289203, 0.211107, 0.9337, 0.0,
    0.412433, -0.71667, -0.56239, 0.0,
    0.87721, -0.082816, 0.47291, 0.0,
    -0.420685, -0.214278, 0.881538, 0.0,
    0.752558, -0.0391579, 0.657361, 0.0,
    0.0765725, -0.996789, 0.0234082, 0.0,
    -0.544312, -0.309435, -0.779727, 0.0,
    -0.455358, -0.415572, 0.787368, 0.0,
    -0.874586, 0.483746, 0.0330131, 0.0,
    0.245172, -0.0838623, 0.965846, 0.0,
    0.382293, -0.432813, 0.81641, 0.0,
    -0.287735, -0.905514, 0.311853, 0.0,
    -0.667704, 0.704955, -0.239186, 0.0,
    0.717885, -0.464002, -0.518983, 0.0,
    0.976342, -0.214895, 0.0240053, 0.0,
    -0.0733096, -0.921136, 0.382276, 0.0,
    -0.986284, 0.151224, -0.0661379, 0.0,
    -0.899319, -0.429671, 0.0812908, 0.0,
    0.652102, -0.724625, 0.222893, 0.0,
    0.203761, 0.458023, -0.865272, 0.0,
    -0.030396, 0.698724, -0.714745, 0.0,
    -0.460232, 0.839138, 0.289887, 0.0,
    -0.0898602, 0.837894, 0.538386, 0.0,
    -0.731595, 0.0793784, 0.677102, 0.0,
    -0.447236, -0.788397, 0.422386, 0.0,
    0.186481, 0.645855, -0.740335, 0.0,
    -0.259006, 0.935463, 0.240467, 0.0,
    0.445839, 0.819655, -0.359712, 0.0,
    0.349962, 0.755022, -0.554499, 0.0,
    -0.997078, -0.0359577, 0.0673977, 0.0,
    -0.431163, -0.147516, -0.890133, 0.0,
    0.299648, -0.63914, 0.708316, 0.0,
    0.397043, 0.566526, -0.722084, 0.0,
    -0.502489, 0.438308, -0.745246, 0.0,
    0.0687235, 0.354097, 0.93268, 0.0,
    -0.0476651, -0.462597, 0.885286, 0.0,
    -0.221934, 0.900739, -0.373383, 0.0,
    -0.956107, -0.225676, 0.186893, 0.0,
    -0.187627, 0.391487, -0.900852, 0.0,
    -0.224209, -0.315405, 0.92209, 0.0,
    -0.730807, -0.537068, 0.421283, 0.0,
    -0.0353135, -0.816748, 0.575913, 0.0,
    -0.941391, 0.176991, -0.287153, 0.0,
    -0.154174, 0.390458, 0.90762, 0.0,
    -0.283847, 0.533842, 0.796519, 0.0,
    -0.482737, -0.850448, 0.209052, 0.0,
    -0.649175, 0.477748, 0.591886, 0.0,
    0.885373, -0.405387, -0.227543, 0.0,
    -0.147261, 0.181623, -0.972279, 0.0,
    0.0959236, -0.115847, -0.988624, 0.0,
    -0.89724, -0.191348, 0.397928, 0.0,
    0.903553, -0.428461, -0.00350461, 0.0,
    0.849072, -0.295807, -0.437693, 0.0,
    0.65551, 0.741754, -0.141804, 0.0,
    0.61598, -0.178669, 0.767232, 0.0,
    0.0112967, 0.932256, -0.361623, 0.0,
    -0.793031, 0.258012, 0.551845, 0.0,
    0.421933, 0.454311, 0.784585, 0.0,
    -0.319993, 0.0401618, -0.946568, 0.0,
    -0.81571, 0.551307, -0.175151, 0.0,
    -0.377644, 0.00322313, 0.925945, 0.0,
    0.129759, -0.666581, -0.734052, 0.0,
    0.601901, -0.654237, -0.457919, 0.0,
    -0.927463, -0.0343576, -0.372334, 0.0,
    -0.438663, -0.868301, -0.231578, 0.0,
    -0.648845, -0.749138, -0.133387, 0.0,
    0.507393, -0.588294, 0.629653, 0.0,
    0.726958, 0.623665, 0.287358, 0.0,
    0.411159, 0.367614, -0.834151, 0.0,
    0.806333, 0.585117, -0.0864016, 0.0,
    0.263935, -0.880876, 0.392932, 0.0,
    0.421546, -0.201336, 0.884174, 0.0,
    -0.683198, -0.569557, -0.456996, 0.0,
    -0.117116, -0.0406654, -0.992285, 0.0,
    -0.643679, -0.109196, -0.757465, 0.0,
    -0.561559, -0.62989, 0.536554, 0.0,
    0.0628422, 0.104677, -0.992519, 0.0,
    0.480759, -0.2867, -0.828658, 0.0,
    -0.228559, -0.228965, -0.946222, 0.0,
    -0.10194, -0.65706, -0.746914, 0.0,
    0.0689193, -0.678236, 0.731605, 0.0,
    0.401019, -0.754026, 0.52022, 0.0,
    -0.742141, 0.547083, -0.387203, 0.0,
    -0.00210603, -0.796417, -0.604745, 0.0,
    0.296725, -0.409909, -0.862513, 0.0,
    -0.260932, -0.798201, 0.542945, 0.0,
    -0.641628, 0.742379, 0.192838, 0.0,
    -0.186009, -0.101514, 0.97729, 0.0,
    0.106711, -0.962067, 0.251079, 0.0,
    -0.743499, 0.30988, -0.592607, 0.0,
    -0.795853, -0.605066, -0.0226607, 0.0,
    -0.828661, -0.419471, -0.370628, 0.0,
    0.0847218, -0.489815, -0.8677, 0.0,
    -0.381405, 0.788019, -0.483276, 0.0,
    0.282042, -0.953394, 0.107205, 0.0,
    0.530774, 0.847413, 0.0130696, 0.0,
    0.0515397, 0.922524, 0.382484, 0.0,
    -0.631467, -0.709046, 0.313852, 0.0,
    0.688248, 0.517273, 0.508668, 0.0,
    0.646689, -0.333782, -0.685845, 0.0,
    -0.932528, -0.247532, -0.262906, 0.0,
    0.630609, 0.68757, -0.359973, 0.0,
    0.577805, -0.394189, 0.714673, 0.0,
    -0.887833, -0.437301, -0.14325, 0.0,
    0.690982, 0.174003, 0.701617, 0.0,
    -0.866701, 0.0118182, 0.498689, 0.0,
    -0.482876, 0.727143, 0.487949, 0.0,
    -0.577567, 0.682593, -0.447752, 0.0,
    0.373768, 0.0982991, 0.922299, 0.0,
    0.170744, 0.964243, -0.202687, 0.0,
    0.993654, -0.035791, -0.106632, 0.0,
    0.587065, 0.4143, -0.695493, 0.0,
    -0.396509, 0.26509, -0.878924, 0.0,
    -0.0866853, 0.83553, -0.542563, 0.0,
    0.923193, 0.133398, -0.360443, 0.0,
    0.00379108, -0.258618, 0.965972, 0.0,
    0.239144, 0.245154, -0.939526, 0.0,
    0.758731, -0.555871, 0.33961, 0.0,
    0.295355, 0.309513, 0.903862, 0.0,
    0.0531222, -0.91003, -0.411124, 0.0,
    0.270452, 0.0229439, -0.96246, 0.0,
    0.563634, 0.0324352, 0.825387, 0.0,
    0.156326, 0.147392, 0.976646, 0.0,
    -0.0410141, 0.981824, 0.185309, 0.0,
    -0.385562, -0.576343, -0.720535, 0.0,
    0.388281, 0.904441, 0.176702, 0.0,
    0.945561, -0.192859, -0.262146, 0.0,
    0.844504, 0.520193, 0.127325, 0.0,
    0.0330893, 0.999121, -0.0257505, 0.0,
    -0.592616, -0.482475, -0.644999, 0.0,
    0.539471, 0.631024, -0.557476, 0.0,
    0.655851, -0.027319, -0.754396, 0.0,
    0.274465, 0.887659, 0.369772, 0.0,
    -0.123419, 0.975177, -0.183842, 0.0,
    -0.223429, 0.708045, 0.66989, 0.0,
    -0.908654, 0.196302, 0.368528, 0.0,
    -0.95759, -0.00863708, 0.288005, 0.0,
    0.960535, 0.030592, 0.276472, 0.0,
    -0.413146, 0.907537, 0.0754161, 0.0,
    -0.847992, 0.350849, -0.397259, 0.0,
    0.614736, 0.395841, 0.68221, 0.0,
    -0.503504, -0.666128, -0.550234, 0.0,
    -0.268833, -0.738524, -0.618314, 0.0,
    0.792737, -0.60001, -0.107502, 0.0,
    -0.637582, 0.508144, -0.579032, 0.0,
    0.750105, 0.282165, -0.598101, 0.0,
    -0.351199, -0.392294, -0.850155, 0.0,
    0.250126, -0.960993, -0.118025, 0.0,
    -0.732341, 0.680909, -0.0063274, 0.0,
    -0.760674, -0.141009, 0.633634, 0.0,
    0.222823, -0.304012, 0.926243, 0.0,
    0.209178, 0.505671, 0.836984, 0.0,
    0.757914, -0.56629, -0.323857, 0.0,
    -0.782926, -0.339196, 0.52151, 0.0,
    -0.462952, 0.585565, 0.665424, 0.0,
    0.61879, 0.194119, -0.761194, 0.0,
    0.741388, -0.276743, 0.611357, 0.0,
    0.707571, 0.702621, 0.0752872, 0.0,
    0.156562, 0.819977, 0.550569, 0.0,
    -0.793606, 0.440216, 0.42, 0.0,
    0.234547, 0.885309, -0.401517, 0.0,
    0.132598, 0.80115, -0.58359, 0.0,
    -0.377899, -0.639179, 0.669808, 0.0,
    -0.865993, -0.396465, 0.304748, 0.0,
    -0.624815, -0.44283, 0.643046, 0.0,
    -0.485705, 0.825614, -0.287146, 0.0,
    -0.971788, 0.175535, 0.157529, 0.0,
    -0.456027, 0.392629, 0.798675, 0.0,
    -0.0104443, 0.521623, -0.853112, 0.0,
    -0.660575, -0.74519, 0.091282, 0.0,
    -0.0157698, -0.307475, -0.951425, 0.0,
    -0.603467, -0.250192, 0.757121, 0.0,
    0.506876, 0.25006, 0.824952, 0.0,
    0.255404, 0.966794, 0.00884498, 0.0,
    0.466764, -0.874228, -0.133625, 0.0,
    0.475077, -0.0682351, -0.877295, 0.0,
    -0.224967, -0.938972, -0.260233, 0.0,
    -0.377929, -0.814757, -0.439705, 0.0,
    -0.305847, 0.542333, -0.782517, 0.0,
    0.26658, -0.902905, -0.337191, 0.0,
    0.0275773, 0.322158, -0.946284, 0.0,
    0.0185422, 0.716349, 0.697496, 0.0,
    -0.20483, 0.978416, 0.0273371, 0.0,
    -0.898276, 0.373969, 0.230752, 0.0,
    -0.00909378, 0.546594, 0.837349, 0.0,
    0.6602, -0.751089, 0.000959236, 0.0,
    0.855301, -0.303056, 0.420259, 0.0,
    0.797138, 0.0623013, -0.600574, 0.0,
    0.48947, -0.866813, 0.0951509, 0.0,
    0.251142, 0.674531, 0.694216, 0.0,
    -0.578422, -0.737373, -0.348867, 0.0,
    -0.254689, -0.514807, 0.818601, 0.0,
    0.374972, 0.761612, 0.528529, 0.0,
    0.640303, -0.734271, -0.225517, 0.0,
    -0.638076, 0.285527, 0.715075, 0.0,
    0.772956, -0.15984, -0.613995, 0.0,
    0.798217, -0.590628, 0.118356, 0.0,
    -0.986276, -0.0578337, -0.154644, 0.0,
    -0.312988, -0.94549, 0.0899272, 0.0,
    -0.497338, 0.178325, 0.849032, 0.0,
    -0.101136, -0.981014, 0.165477, 0.0,
    -0.521688, 0.0553434, -0.851339, 0.0,
    -0.786182, -0.583814, 0.202678, 0.0,
    -0.565191, 0.821858, -0.0714658, 0.0,
    0.437895, 0.152598, -0.885981, 0.0,
    -0.92394, 0.353436, -0.14635, 0.0,
    0.212189, -0.815162, -0.538969, 0.0,
    -0.859262, 0.143405, -0.491024, 0.0,
    0.991353, 0.112814, 0.0670273, 0.0,
    0.0337884, -0.979891, -0.196654, 0.0]


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
    c_per = 0.5

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
        #seed = (seed + i) & 0x7fffffff

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


def radnorm_arg(arg):
    sqr = arg*arg
    total = cp.sum(sqr, axis=-1)
    length = cp.sqrt(total)
    length = cp.expand_dims(length, axis=-1)
    length = cp.repeat(length, 3, axis=-1)
    norm = arg/length
    norm = 1+norm/2.0
    return norm


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



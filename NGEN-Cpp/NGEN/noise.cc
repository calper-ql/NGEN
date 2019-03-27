//
// Created by calpe on 3/26/2019.
//

#include "noise.h"


namespace NGEN::Noise {

    PerlinNoise::PerlinNoise() {
        this->seed = 42;
        gen = std::default_random_engine(seed);
        dist = std::uniform_real_distribution<double>(0.0, 1.0);
        this->p.resize(256 * 4);
        for (size_t i = 0; i < p.size(); ++i) {
            p[i] = (uint8_t)(dist(gen) * 255.0f);
        }
    }

    PerlinNoise::PerlinNoise(unsigned seed) {
        this->seed = seed;
        gen = std::default_random_engine(seed);
        dist = std::uniform_real_distribution<double>(0.0, 1.0);
        this->p.resize(256 * 4);
        for (size_t i = 0; i < p.size(); ++i) {
            p[i] = (uint8_t)(dist(gen) * 255.0f);
        }
    }

    double PerlinNoise::clamp(double x, double ll, double ul) {
        if (x < ll) return ll;
        if (x > ul) return ul;
        return x;
    }

    double PerlinNoise::smooth_step(double a0, double a1, double w) {
        double x = clamp((w - a0) / (a1 - a0), 0.0, 1.0);
        return x * x * (3 - 2 * x);
    }

    double PerlinNoise::lerp(double a0, double a1, double w) {
        return a0 + smooth_step(0.0, 1.0, w) * (a1 - a0);
    }

    double fade(double t) { return t * t * t * (t * (t * 6 - 15) + 10); }

    int inc(int num) {
        num++;
        //if (1 > 0) num %= 1;
        return num;
    }

    double grad(int hash, double x, double y, double z)
    {
        switch (hash & 0xF)
        {
            case 0x0: return  x + y;
            case 0x1: return -x + y;
            case 0x2: return  x - y;
            case 0x3: return -x - y;
            case 0x4: return  x + z;
            case 0x5: return -x + z;
            case 0x6: return  x - z;
            case 0x7: return -x - z;
            case 0x8: return  y + z;
            case 0x9: return -y + z;
            case 0xA: return  y - z;
            case 0xB: return -y - z;
            case 0xC: return  y + x;
            case 0xD: return -y + z;
            case 0xE: return  y - x;
            case 0xF: return -y - z;
            default: return 0; // never happens
        }
    }

    double PerlinNoise::noise(double x, double y, double z) {
        int xi = ((int)floor(x)) & 255;                              // Calculate the "unit cube" that the point asked will be located in
        int yi = ((int)floor(y)) & 255;                              // The left bound is ( |_x_|,|_y_|,|_z_| ) and the right bound is that
        int zi = ((int)floor(z)) & 255;                              // plus 1.  Next we calculate the location (from 0.0 to 1.0) in that cube.
        double xf = x - (int)x;
        double yf = y - (int)y;
        double zf = z - (int)z;

        double u = fade(xf);
        double v = fade(yf);
        double w = fade(zf);

        int aaa, aba, aab, abb, baa, bba, bab, bbb;
        aaa = p[p[p[xi] + yi] + zi];
        aba = p[p[p[xi] + inc(yi)] + zi];
        aab = p[p[p[xi] + yi] + inc(zi)];
        abb = p[p[p[xi] + inc(yi)] + inc(zi)];
        baa = p[p[p[inc(xi)] + yi] + zi];
        bba = p[p[p[inc(xi)] + inc(yi)] + zi];
        bab = p[p[p[inc(xi)] + yi] + inc(zi)];
        bbb = p[p[p[inc(xi)] + inc(yi)] + inc(zi)];

        double x1, x2, y1, y2;
        x1 = lerp(grad(aaa, xf, yf, zf),           // The gradient function calculates the dot product between a pseudorandom
                  grad(baa, xf - 1, yf, zf),             // gradient vector and the vector from the input coordinate to the 8
                  u);                                     // surrounding points in its unit cube.
        x2 = lerp(grad(aba, xf, yf - 1, zf),           // This is all then lerped together as a sort of weighted average based on the faded (u,v,w)
                  grad(bba, xf - 1, yf - 1, zf),             // values we made earlier.
                  u);
        y1 = lerp(x1, x2, v);

        x1 = lerp(grad(aab, xf, yf, zf - 1),
                  grad(bab, xf - 1, yf, zf - 1),
                  u);
        x2 = lerp(grad(abb, xf, yf - 1, zf - 1),
                  grad(bbb, xf - 1, yf - 1, zf - 1),
                  u);
        y2 = lerp(x1, x2, v);

        return lerp(y1, y2, w);
    }

    VoronoiNoise::VoronoiNoise() {
        this->seed = 42;
        this->frequency = 1.0;
        this->distance = true;
    }

    VoronoiNoise::VoronoiNoise(unsigned seed, double frequency, bool distance) {
        this->seed = seed;
        this->frequency = frequency;
        this->distance = distance;
    }

    const int X_NOISE_GEN = 1619;
    const int Y_NOISE_GEN = 31337;
    const int Z_NOISE_GEN = 6971;
    const int SEED_NOISE_GEN = 1013;
    const int SHIFT_NOISE_GEN = 8;
    const double SQRT_3 = 1.7320508075688772935;

    int IntValueNoise3D(int x, int y, int z, int seed)
    {
        // All constants are primes and must remain prime in order for this noise
        // function to work correctly.
        int n = (
                        X_NOISE_GEN   * x
                        + Y_NOISE_GEN * y
                        + Z_NOISE_GEN * z
                        + SEED_NOISE_GEN * seed)
                & 0x7fffffff;
        n = (n >> 13) ^ n;
        return (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff;
    }

    double ValueNoise3D(int x, int y, int z, int seed)
    {
        return 1.0 - ((double)IntValueNoise3D(x, y, z, seed) / 1073741824.0);
    }


    double VoronoiNoise::noise(double x, double y, double z) {

        x *= frequency;
        y *= frequency;
        z *= frequency;

        int xInt = (x > 0.0 ? (int)x : (int)x - 1);
        int yInt = (y > 0.0 ? (int)y : (int)y - 1);
        int zInt = (z > 0.0 ? (int)z : (int)z - 1);

        double minDist = 2147483647.0;
        double xCandidate = 0;
        double yCandidate = 0;
        double zCandidate = 0;

        // Inside each unit cube, there is a seed point at a random position.  Go
        // through each of the nearby cubes until we find a cube with a seed point
        // that is closest to the specified position.
        for (int zCur = zInt - 2; zCur <= zInt + 2; zCur++) {
            for (int yCur = yInt - 2; yCur <= yInt + 2; yCur++) {
                for (int xCur = xInt - 2; xCur <= xInt + 2; xCur++) {

                    // Calculate the position and distance to the seed point inside of
                    // this unit cube.
                    double xPos = xCur + ValueNoise3D(xCur, yCur, zCur, seed);
                    double yPos = yCur + ValueNoise3D(xCur, yCur, zCur, seed + 1);
                    double zPos = zCur + ValueNoise3D(xCur, yCur, zCur, seed + 2);
                    double xDist = xPos - x;
                    double yDist = yPos - y;
                    double zDist = zPos - z;
                    double dist = xDist * xDist + yDist * yDist + zDist * zDist;

                    if (dist < minDist) {
                        // This seed point is closer to any others found so far, so record
                        // this seed point.
                        minDist = dist;
                        xCandidate = xPos;
                        yCandidate = yPos;
                        zCandidate = zPos;
                    }
                }
            }
        }

        return minDist/2.0;

        double value;
        if (distance) {
            // Determine the distance to the nearest seed point.
            double xDist = xCandidate - x;
            double yDist = yCandidate - y;
            double zDist = zCandidate - z;
            value = (sqrt(xDist * xDist + yDist * yDist + zDist * zDist)) * sqrt(3) - 1.0;
        }
        else {
            value = 0.0;
        }

        // Return the calculated distance with the displacement value applied.
        return value/2.0 + ((double)ValueNoise3D(
                (int)(floor(xCandidate)),
                (int)(floor(yCandidate)),
                (int)(floor(zCandidate)), seed+3))/2.0;

    }
}
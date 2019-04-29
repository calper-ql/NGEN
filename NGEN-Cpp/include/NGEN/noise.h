//
// Created by calpe on 3/26/2019.
//

#ifndef NGEN_CPP_NOISE_H
#define NGEN_CPP_NOISE_H

#include <cmath>
#include <random>

namespace NGEN::Noise {

    class PerlinNoise {
    public:
        explicit PerlinNoise();

        // expects a normalized value from 0 to 1 for each dim
        double noise(unsigned seed, double x, double y, double z);
    };

    class VoronoiNoise {
    public:
        unsigned seed;
        double frequency;
        bool distance;

        VoronoiNoise();

        VoronoiNoise(unsigned seed, double frequency, bool distance);

        // expects a normalized value from 0 to 1 for each dim
        double noise(double x, double y, double z);
    };
}


#endif //NGEN_CPP_NOISE_H

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
        unsigned seed;
        std::default_random_engine gen;
        std::uniform_real_distribution<double> dist;

        std::vector<uint8_t> p;

        explicit PerlinNoise();

        explicit PerlinNoise(unsigned seed);

        double lerp(double a0, double a1, double w);

        double smooth_step(double a0, double a1, double w);

        double clamp(double x, double ll, double ul);

        // expects a normalized value from 0 to 1 for each dim
        double noise(double x, double y, double z);
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

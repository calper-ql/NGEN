//
// Created by calpe on 3/25/2019.
//

#ifndef NGEN_CPP_SIMPLEMODULES_H
#define NGEN_CPP_SIMPLEMODULES_H

#include "Module.h"
#include "noise.h"

namespace NGEN {
	class TestModule : public Module {
	public:
		NGEN_FLOAT(test, 0.0)
			NGEN_INT(uwu, 0)
			NGEN_SEED(seed, 0)
			NGEN_BOOL(another_lol, 0)
			NGEN_STRING(name, "random name lul")

			NGEN_INPUT(test_input)
			NGEN_OUTPUT(test_output)

			explicit TestModule(ModulePool* mp) : Module(mp) {
			NGEN_SET_PROPERTY(test, 31.0)
		}

		~TestModule() override {
			std::cout << "Deleting test module" << std::endl;
		}
	};
	NGEN_REGISTER_MODULE(TestModule);

	class OutputModule : public Module {
	public:
		NGEN_STRING(name, "default")
			NGEN_INPUT(input)

			explicit OutputModule(ModulePool* mp) : Module(mp) {}
	};
	NGEN_REGISTER_MODULE(OutputModule);

	class RGBOutputModule : public Module {
	public:
		NGEN_STRING(name, "default")
			NGEN_INPUT(R)
			NGEN_INPUT(G)
			NGEN_INPUT(B)

			NGEN_FLOAT(r_mult, 1.0)
			NGEN_FLOAT(g_mult, 1.0)
			NGEN_FLOAT(b_mult, 1.0)

			float stored[3];

		explicit RGBOutputModule(ModulePool* mp) : Module(mp) {}
		void calculate(float x, float y, float z) override {
			if (!calculated) {
				stored[0] = R.calculate(x, y, z) * r_mult.value;
				stored[1] = G.calculate(x, y, z) * g_mult.value;
				stored[2] = B.calculate(x, y, z) * b_mult.value;
				if (stored[0] < 0.0) stored[0] = 0.0;
				if (stored[1] < 0.0) stored[1] = 0.0;
				if (stored[2] < 0.0) stored[2] = 0.0;
				if (stored[0] > 1.0) stored[0] = 1.0;
				if (stored[1] > 1.0) stored[1] = 1.0;
				if (stored[2] > 1.0) stored[2] = 1.0;
				calculated = true;
			}
		}
	};
	NGEN_REGISTER_MODULE(RGBOutputModule);

	class AddModule : public Module {
	public:
		NGEN_INPUT(A)
			NGEN_INPUT(B)
			NGEN_OUTPUT(C)

			explicit AddModule(ModulePool* mp) : Module(mp) {}

		void calculate(float x, float y, float z) override {
			if (!calculated) {
				C.stored_value = A.calculate(x, y, z) + B.calculate(x, y, z);
				calculated = true;
			}
		}
	};
	NGEN_REGISTER_MODULE(AddModule)

		class MultiplyModule : public Module {
		public:
			NGEN_INPUT(A)
				NGEN_INPUT(B)
				NGEN_OUTPUT(C)

				explicit MultiplyModule(ModulePool* mp) : Module(mp) {}

			void calculate(float x, float y, float z) override {
				if (!calculated) {
					C.stored_value = A.calculate(x, y, z) * B.calculate(x, y, z);
					calculated = true;
				}
			}
	};
	NGEN_REGISTER_MODULE(MultiplyModule);

	class ConstantModule : public Module {
	public:
		NGEN_OUTPUT(output)
			NGEN_FLOAT(value, 1.0)

			explicit ConstantModule(ModulePool* mp) : Module(mp) {}

		void calculate(float x, float y, float z) override {
			if (!calculated) {
				output.stored_value = value.value;
				calculated = true;
			}
		}
	};
	NGEN_REGISTER_MODULE(ConstantModule);

	class PerlinModule : public Module {
	public:

		NGEN_SEED(seed, 42)
			NGEN_INT(octave, 4)
			NGEN_FLOAT(frequency, 1.0)
			NGEN_FLOAT(lacunarity, 1.0)
			NGEN_FLOAT(persistance, 1.0)

			NGEN_OUTPUT(output)

			Noise::PerlinNoise pn;

		explicit PerlinModule(ModulePool* mp) : Module(mp) {
			pn = Noise::PerlinNoise();
		}

		void calculate(float x, float y, float z) override {
			if (!calculated) {
				float var = 0;
				float f = frequency.value;
				float p = 0.5;

				for (int i = 0; i < octave.value; i++) {
					var += static_cast<float>(pn.noise(seed.value, x*f, y*f, z*f)) * p;
					p *= persistance.value;
					f *= lacunarity.value;
				}

				output.stored_value = var;
				calculated = true;
			}
		}
	};
	NGEN_REGISTER_MODULE(PerlinModule);

	class RiggedMultiModule : public Module {
	public:

		NGEN_SEED(seed, 42)
			NGEN_INT(octave, 4)
			NGEN_FLOAT(frequency, 1.0)
			NGEN_FLOAT(lacunarity, 1.0)
			NGEN_FLOAT(exp, 1.0)
			NGEN_FLOAT(offset, 1.0)

			NGEN_OUTPUT(output)

			Noise::PerlinNoise pn;

		explicit RiggedMultiModule(ModulePool* mp) : Module(mp) {
			pn = Noise::PerlinNoise();
		}

		void calculate(float x, float y, float z) override {
			if (!calculated) {
				float var = 0;
				float f = frequency.value;
				float weight = 1.0;
				float d_freq = 1.0;
				float signal = 0.0;

				for (int i = 0; i < octave.value; i++) {
					signal = static_cast<float>(pn.noise(seed.value, x*f, y*f, z*f));
					signal = abs(signal);
					signal = offset.value - signal;
					weight *= weight;

					weight = static_cast<float>(signal * 2.0);
					if (weight > 1.0) weight = 1.0;
					if (weight < 0.0) weight = 0.0;

					var += (signal * pow(d_freq, exp.value));

					f *= lacunarity.value;
					d_freq *= lacunarity.value;
				}

				output.stored_value = var;
				calculated = true;
			}
		}
	};
	NGEN_REGISTER_MODULE(RiggedMultiModule);

	class VoronoiModule : public Module {
	public:

		NGEN_SEED(seed, 42)
			NGEN_FLOAT(frequency, 1.0)
			NGEN_FLOAT(displacement, 1.0)
			NGEN_BOOL(distance_enabled, false)

			NGEN_OUTPUT(output)

			Noise::VoronoiNoise vn;

		explicit VoronoiModule(ModulePool* mp) : Module(mp) {
			vn = Noise::VoronoiNoise(
				static_cast<unsigned int>(seed.value),
				frequency.value,
				distance_enabled.value);
		}

		void calculate(float x, float y, float z) override {
			if (!calculated) {
				output.stored_value = static_cast<float>(vn.noise(x, y, z));
				calculated = true;
			}
		}
	};
	NGEN_REGISTER_MODULE(VoronoiModule);

	class RadNormModule : public Module {
	public:
		NGEN_INPUT(input)
			NGEN_OUTPUT(output)

			explicit RadNormModule(ModulePool* mp) : Module(mp) {

		}

		void calculate(float x, float y, float z) override {
			if (!calculated) {
				float dist = sqrtf(x*x + y * y + z * z)*2.0;
				float nx = 1.0f + (x / dist);
				float ny = 1.0f + (y / dist);
				float nz = 1.0f + (z / dist);
				output.stored_value = input.calculate(nx, ny, nz);
				calculated = true;
			}
		}
	};
	NGEN_REGISTER_MODULE(RadNormModule);

	inline double __Select_Module_SCurve5(double a)
	{
		double a3 = a * a * a;
		double a4 = a3 * a;
		double a5 = a4 * a;
		return (6.0 * a5) - (15.0 * a4) + (10.0 * a3);
	}

	class SelectModule : public Module {
	public:
		NGEN_INPUT(control)
			NGEN_INPUT(A)
			NGEN_INPUT(B)
			NGEN_OUTPUT(output)
			NGEN_FLOAT(falloff, 0.0)
			NGEN_FLOAT(low_bound, 0.0)
			NGEN_FLOAT(high_bound, 1.0)

			explicit SelectModule(ModulePool* mp) : Module(mp) {

		}

		void calculate(float x, float y, float z) override {
			if (!calculated) {
				float ctrl = control.calculate(x, y, z);

				if (ctrl < low_bound.value - falloff.value) {
					output.stored_value = A.calculate(x, y, z);
				} else if(ctrl < low_bound.value + falloff.value) {
					float alpha = ((ctrl - (low_bound.value - falloff.value)) /
						((low_bound.value + falloff.value) - (low_bound.value - falloff.value)));
					alpha = __Select_Module_SCurve5(alpha);
					output.stored_value = B.calculate(x, y, z) * alpha + A.calculate(x, y, z) * (1.0 - alpha);
				} else if (ctrl < high_bound.value - falloff.value) {
					output.stored_value = B.calculate(x, y, z);
				}
				else if (ctrl < high_bound.value + falloff.value) {
					float alpha = ((ctrl - (high_bound.value - falloff.value)) /
						((high_bound.value + falloff.value) - (high_bound.value - falloff.value)));
					alpha = __Select_Module_SCurve5(alpha);
					output.stored_value = A.calculate(x, y, z) * alpha + B.calculate(x, y, z) * (1.0 - alpha);
				} else {
					output.stored_value = A.calculate(x, y, z);
				}

				calculated = true;
				//float ctrl = control.calculate(x, y, z) - cutoff.value;
				//float lin_val = (ctrl + falloff.value) / (2 * falloff.value);
				//output.stored_value = A.calculate(x, y, z) * lin_val +
				//	B.calculate(x, y, z) * (bound.value - lin_val);
			}
		}
	};
	NGEN_REGISTER_MODULE(SelectModule);



}

#endif //NGEN_CPP_SIMPLEMODULES_H

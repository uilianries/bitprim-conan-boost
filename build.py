from conan.packager import ConanMultiPackager
import os
import platform

if __name__ == "__main__":
    #TODO Specify combinations here using archs argument
    builder = ConanMultiPackager(username="bitprim", channel="stable")
    builder.add_common_builds(shared_option_name="bitprim-conan-boost:shared", pure_c=False)

    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        # filtered_builds.append([settings, options, env_vars, build_requires])
        print(settings)
        print(options)
        if settings["build_type"] == "Release" \
                and settings["arch"] == "x86_64" \
                and options["bitprim-conan-boost:shared"] == False:
            #TODO: Adding gcc 4.9 c++11 build manually until Conan fixes it
            if settings["compiler"] == "gcc" and settings["compiler.version"] == "4.9":
                builder.add(settings={'compiler.version': '4.9', 'compiler.libcxx': 'libstdc++11', 'arch': 'x86_64', 'build_type': 'Release', 'compiler': 'gcc'}, options={'bitprim-conan-boost:shared': False})
            else:
                if not "compiler.libcxx" in settings or settings["compiler"] == "apple-clang" or ("compiler.libcxx" in settings and settings["compiler.libcxx"] == "libstdc++"):
                    filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()

from conan.packager import ConanMultiPackager
import os
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(username="bitprim", channel="stable", archs=["x86_64"])
    builder.add_common_builds(shared_option_name="bitprim-conan-boost:shared", pure_c=False)

    filtered_builds = []
    add_special_case = False
    for settings, options, env_vars, build_requires in builder.builds:
        print(settings)
        print(options)
        if settings["build_type"] == "Release" \
                and options["bitprim-conan-boost:shared"] == False:
            #TODO: Adding gcc 4.9 c++11 build manually until Conan fixes it
            if settings["compiler"] == "gcc" and settings["compiler.version"] == "4.9":
                add_special_case = True
            else:
                if not "compiler.libcxx" in settings or settings["compiler"] == "apple-clang" or ("compiler.libcxx" in settings and settings["compiler.libcxx"] == "libstdc++"):
                    filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    if add_special_case:
        builder.add(settings={'compiler.version': '4.9', 'compiler.libcxx': 'libstdc++11', 'arch': 'x86_64', 'build_type': 'Release', 'compiler': 'gcc'}, options={'bitprim-conan-boost:shared': False})
    builder.run()

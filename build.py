from conan.packager import ConanMultiPackager
import os
import platform

if __name__ == "__main__":
    #TODO Specify combinations here using archs argument
    builder = ConanMultiPackager(username="bitprim", channel="stable", pure_c=False)
    builder.add_common_builds(shared_option_name="bitprim-conan-boost:shared")

    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        print(settings)
        print(options)
        if settings["build_type"] == "Release" \
                and settings["arch"] == "x86_64" \
                and options["bitprim-conan-boost:shared"] == False:
            #TODO Test
            #if platform.system() == "Windows":
            #     if settings["compiler"] == "gcc":
            #        settings["compiler.libcxx"] = "libstdc++11"
            #else:
            #    if settings["compiler.libcxx"] == "libstdc++":
            #        settings["compiler.libcxx"] = "libstdc++11"
            if "compiler.libcxx" in settings and settings["compiler"] == "gcc" and settings["compiler.libcxx"] != "libstdc++11":
                continue
            filtered_builds.append([settings, options, env_vars, build_requires])        

    builder.builds = filtered_builds
    builder.run()

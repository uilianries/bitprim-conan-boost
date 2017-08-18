from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="bitprim", channel="stable", archs=["x86_64"])
    builder.add_common_builds(shared_option_name="bitprim-conan-boost:shared", pure_c=False)

    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        # print(settings)
        # print(options)
        if settings["build_type"] == "Release" \
                and options["bitprim-conan-boost:shared"] == False:

            filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()

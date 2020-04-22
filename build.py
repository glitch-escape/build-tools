#!/usr/bin/env python3
import argparse
import os

# check if we're (probably) in a tools folder in a glitch escape projects directory or not
# if we are, make the build dir there; if not, use a build folder in the same dir we're
# running this script from
if os.path.exists('../Assets'):
    BUILD_DIR = '../Builds'
else:
    BUILD_DIR = 'Builds'


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', metavar='VERSION',
                        dest='version', type=str, default=None,
                        help='build version #, eg. v0.2.1')
    parser.add_argument('--build-target', metavar='BUILD TARGET',
                        dest='build_target', type=str, default=None,
                        help='build for target platform (mac, windows, linux)')
    parser.add_argument('--build-all',
                        dest='build_all', action='store_true', default=False,
                        help='build for all target platforms')
    parser.add_argument('--build',
                        dest='build_current', action='store_true',
                        default=False,
                        help='build target for current platform')
    parser.add_argument('--run',
                        dest='run', action='store_true', default=False,
                        help='runs a new (or existing) build version on your current platform')
    parser.add_argument('--fetch',
                        dest='fetch', action='store_true', default=False,
                        help='downloads a build version from the glitch escape repository')
    parser.add_argument('--publish',
                        dest='publish', action='store_true', default=False,
                        help='creates and/or uploads builds to a new release draft on the glitch escape repository using github-release-cli')
    parser.add_argument('--clean',
                        dest='clean', action='store_true', default=False,
                        help='deletes all local build files')
    args = parser.parse_args()
    return args


class PlatformInfo:
    ALL_PLATFORMS = ('mac', 'windows', 'linux')
    PLATFORM_ALIASES = {
        'macos': ('mac', 'x86_64'),
        'win': ('windows', 'x86_64'),
        'win32': ('windows', 'x86'),
        'win64': ('windows', 'x86_64'),
    }

    def __init__(self, platform, arch='x86_64'):
        platform = platform.lower()
        arch = arch.lower()
        platform = platform.lower()
        arch = arch.lower()
        if platform in PlatformInfo.PLATFORM_ALIASES:
            platform, arch = PlatformInfo.PLATFORM_ALIASES[platform]
        if platform not in PlatformInfo.ALL_PLATFORMS:
            raise Exception(f"invalid platform target {platform}")
        if arch not in ('x86_64'):
            raise Exception(
                f"invalid architecture (expected x86_64) '{platform}'")
        self.platform = platform
        self.arch = arch

    def __repr__(self):
        return f"{self.platform} {self.arch}"

    def __cmp__(self, other):
        if type(self) != type(other):
            return cmp(type(self), type(other))
        return cmp((self.platform, self.arch), (other.platform, other.arch))

    @staticmethod
    def all():
        return map(PlatformInfo, PlatformInfo.ALL_PLATFORMS)

    @staticmethod
    def current():
        import platform
        platform_info = platform.platform().lower()
        current_platform = None
        current_platform_arch = None
        if 'darwin' in platform_info:
            current_platform = 'mac'
        elif 'windows' in platform_info:
            current_platform = 'windows'
        elif 'linux' in platform_info:
            current_platform = 'linux'
        else:
            raise Exception(
                f"Unhandled platform returned by platform.platform()! {platform_info}")
        if '64' in platform_info:
            current_platform_arch = 'x86_64'
        else:
            raise Exception(
                f"You don't seem to be running on a 64 bit OS...? (got platform info '{platform_info}'")
        return PlatformInfo(current_platform, current_platform_arch)


class BuildDir:
    instance = None

    @staticmethod
    def get():
        if not BuildDir.instance:
            BuildDir.instance = BuildDir(BUILD_DIR)
        return BuildDir.instance

    @staticmethod
    def get_builds():
        return BuildDir.get().get_build_list()

    @staticmethod
    def get_or_create_build_info(self, platform, version):
        instance = B

    def __init__(self, build_dir=None):
        self.build_dir = build_dir or BUILD_DIR
        self._build_list = None

    @property
    def path(self):
        return self.build_dir

    def rebuild(self):
        self._build_list = None

    def get_build_list(self):
        if self._build_list is None:
            self._build_list = set()
            self.load()
        return self._build_list

    def get_build(self, platform, version):
        for build in self.get_build_list():
            if build.platform == platform and build.version == version:
                return build
        return None

    def get_or_create_build(self, platform, version):
        build_info = self.get_build(platform, version)
        if build_info is None:
            build_info = BuildInfo(self.path, platform.platform, version)
            self.add_build(build_info)
        return build_info

    def add_build(self, build):
        self.get_build_list().add(build)

    def load(self):
        if not os.path.exists(self.build_dir):
            return

        base_path = self.build_dir
        for platform_folder in os.listdir(base_path):
            path = os.path.join(base_path, platform_folder)
            for version_folder in os.listdir(path):
                self.add_build(BuildInfo(self.path, platform_folder, version_folder))

    def clean(self):
        # delete all files using shutil.rmtree(), iff build dir exists
        if os.path.exists(self.build_dir):

            # find + list all the current builds we have that we'll be deleting
            builds = self.get_build_list()
            print("removing {} local build(s):{}".format(
                len(builds),
                ''.join([
                    f'\n  {build_info}'
                    for build_info in builds
                    if build_info.exists()
                ])))

            # delete the files
            import shutil
            shutil.rmtree(build_dir)

            # clear all entries
            self._build_list = set()


class BuildInfo:
    @staticmethod
    def get(platform, version):
        return BuildDir.get().get_build(platform, version)

    @staticmethod
    def get_or_create(platform, version):
        return BuildDir.get().get_or_create_build(platform, version)

    def __init__(self, build_path, platform, version):
        # print((build_path, platform, version))
        # print(list(map(type, (build_path, platform, version))))
        self.build_path = os.path.join(build_path, platform, version)
        self.build_info_path = os.path.join(
            self.build_path, 'build_info.yaml')
        self.platform = platform
        self.version = version
        if os.path.exists(self.build_info_path):
            self.read()
        else:
            self.status = None
            self.app_path = None
            self.exec_path = None
            self.zip_path = None
            self.branch = None
            self.commit = None

    def read(self):
        pass

    def write(self):
        pass


def build_target(target, version):
    print(f"building {version} for {target}")
    info = BuildInfo.get_or_create(target, version)


def fetch_build(target, version):
    print(f"fetching {version} for {target}")
    info = BuildInfo.get_or_create(target, version)


def run_build(target, version):
    print(f"running {version} as {target}")
    info = BuildInfo.get(target, version)


def ask_user_if_build_ok():
    def ask_is_build_ok():
        while True:
            result = input("is build ok? y/n\n").lower()
            if 'y' in result:
                return True
            if 'n' in result:
                return False
            print("invalid response")

    if not ask_is_build_ok():
        exit()


def publish_build(version):
    print(f"publishing build(s) as {version} (TBD)")


def clean_builds():
    BuildDir.get().clean()


if __name__ == '__main__':
    current_platform = PlatformInfo.current()
    args = parse_cli_args()
    print(f"detected platform: {current_platform}")
    build_targets = set()
    if args.build_all:
        build_targets = set(PlatformInfo.all())
    elif args.build_target is not None:
        build_targets.add(PlatformInfo(args.build_target))
    elif args.build_current:
        build_targets.add(current_platform)

    if build_targets and args.fetch:
        print("ignoring --fetch since build target(s) provided: {0}".format(
            ", ".join(map(str, build_targets))))
        args.fetch = False

    args.version = args.version or 'latest'

    if args.clean:
        clean_builds()

    for target in build_targets:
        build_target(target, args.version)

    if args.fetch:
        fetch_build(current_platform, args.version)

    if args.run:
        run_build(current_platform, args.version)

    if args.publish and args.run:
        ask_user_if_build_ok()

    if args.publish:
        publish_build(args.version)

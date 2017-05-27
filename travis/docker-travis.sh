#!/bin/bash
# Copyright (C) 2017 Pier Luigi Fiorini
# Copyright (C) 2016 Mikkel Oscar Lyderik Larsen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

set -e

simulate=0
[ "$1" = "test" ] && simulate=1

# docker image
docker_image="liri-docker-build.bintray.io/archlinux/devel"

# script to run in the container
docker_script="/tmp/docker-travis.sh"

GOROOT=""

# read value from .travis.yml
travis_yml() {
    ruby -ryaml -e 'puts ARGV[1..-1].inject(YAML.load(File.read(ARGV[0]))) {|acc, key| acc[key] }' .travis.yml $@
}

# read config from .travis.yml arch section
read_config() {
    local old_ifs=$IFS
    IFS=$'\n'
    CONFIG_BUILD_SCRIPTS=($(travis_yml arch script))
    CONFIG_PACKAGES=($(travis_yml arch packages))
    CONFIG_REPOS=($(travis_yml arch repos))
    CONFIG_ARTIFACTS=($(travis_yml arch artifacts))
    IFS=$old_ifs
}

# run build scripts defined in .travis.yml
build_scripts() {
    if [ ${#CONFIG_BUILD_SCRIPTS[@]} -gt 0 ]; then
        for script in "${CONFIG_BUILD_SCRIPTS[@]}"; do
            echo "echo \"\$ $script\"" >> $docker_script
            echo "$script" >> $docker_script
        done
    else
        echo "No build scripts defined"
        exit 1
    fi
}

# install packages defined in .travis.yml
install_packages() {
    for package in "${CONFIG_PACKAGES[@]}"; do
        echo "pacman -S $package --noconfirm --noprogressbar" >> $docker_script
    done
}

# install custom compiler if CC != gcc
install_c_compiler() {
    if [ "$CC" != "gcc" ]; then
        echo "pacman -S $CC --noconfirm --noprogressbar" >> $docker_script
    fi
}

# download and unpack artifacts to /
unpack_artifacts() {
    if [ ${#CONFIG_ARTIFACTS[@]} -gt 0 ]; then
        for artifact in "${CONFIG_ARTIFACTS[@]}"; do
            filename=$(basename "$artifact")
            echo "curl -u $FTP_USER:$FTP_PASSWORD $FTP_URL/artifacts/$TRAVIS_BRANCH/$artifact > $filename" >> $docker_script
            echo "tar xf $filename -C /" >> $docker_script
        done
    fi
}

arch_msg() {
    lightblue='\033[1;34m'
    reset='\e[0m'
    echo -e "${lightblue}$@${reset}"
}

[ -z "$CC" ] && CC=gcc

cat > $docker_script <<EOF
#!/bin/bash

set -e

arch_msg() {
    lightblue='\\033[1;34m'
    reset='\\e[0m'
    echo -e "\${lightblue}$@\${reset}"
}

env

EOF
chmod 755 $docker_script

read_config

echo 'arch_msg "Install packages"' >> $docker_script
echo "pacman -Syy --noprogressbar" >> $docker_script
echo "pacman -Syu --noconfirm --noprogressbar" >> $docker_script
install_packages
install_c_compiler
unpack_artifacts

echo 'echo "travis_fold:end:arch_travis"' >> $docker_script
echo 'echo ""' >> $docker_script

echo 'arch_msg "Running travis build"' >> $docker_script
build_scripts

# run
if [ $simulate -eq 0 ]; then
    env_vars="-e CC=$CC -e CLAZY_CHECKS=$CLAZY_CHECKS"
    for line in $(env | grep ^FTP); do
        env_vars="$env_vars -e $line"
    done
    for line in $(env | grep ^TRAVIS); do
        env_vars="$env_vars -e $line"
    done

    docker pull $docker_image
    docker run -i --rm -v $docker_script:/build.sh -v $(pwd):/home $env_vars --workdir /home $docker_image /build.sh
    rm -f $docker_script
fi

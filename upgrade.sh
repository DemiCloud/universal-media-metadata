#!/usr/bin/env bash

declare -A COLORS
COLORS["RED"]=$(printf "\e[31m")
COLORS["GREEN"]=$(printf "\e[32m")
COLORS["YELLOW"]=$(printf "\e[33m")
COLORS["BLUE"]=$(printf "\e[34m")
COLORS["PURPLE"]=$(printf "\e[35m")
COLORS["CYAN"]=$(printf "\e[36m")
COLORS["NORMAL"]=$(printf "\e[0m")
declare -r COLORS

SWD="${BASH_SOURCE%/*}"
VENV_DIR="${SWD}/.venv"
PKGS_DEBIAN=(
  "python3-venv"
)
PKGS_RHEL=(
  "python3-virtualenv"
)

main(){
  regex_debian="\bdebian\b"
  regex_rhel="\brhel\b|\bcentos\b|\bfedora\b"
  if [[ "${EUID}" != "0" ]]; then
    # shellcheck disable=SC2059 # Variables are formatting
    printf "${COLORS["RED"]}ERROR${COLORS["NORMAL"]}: You must run this script as ${COLORS["BLUE"]}root${COLORS["NORMAL"]} or via ${COLORS["BLUE"]}sudo${COLORS["NORMAL"]}\n\n"
    return 1
  fi
  source /etc/os-release
  # shellcheck disable=SC2059 # Variables are formatting
  printf "${COLORS[BLUE]}%s${COLORS["NORMAL"]}\n" "Managing OS Packages..."
  if [[ "${ID_LIKE,,}" =~ $regex_debian || "${ID,,}" =~ $regex_debian ]] ; then
    for pkg in "${PKGS_DEBIAN[@]}"; do
      # shellcheck disable=SC2059 # Variables are formatting
      printf "${COLORS[BLUE]}%s${COLORS["NORMAL"]}\n" "- ${pkg}"
      apt install -y "${pkg}"
    done
  elif [[ "${ID_LIKE,,}" =~ $regex_rhel || "${ID,,}" =~ $regex_rhel ]]; then
    for pkg in "${PKGS_RHEL[@]}"; do
      # shellcheck disable=SC2059 # Variables are formatting
      printf "${COLORS[BLUE]}%s${COLORS["NORMAL"]}\n" "- ${pkg}"
      dnf install -y "${pkg}"
    done
  fi

  # shellcheck disable=SC2059 # Variables are formatting
  printf "\n${COLORS[BLUE]}%s${COLORS["NORMAL"]}\n" "Managing python virtual environment..."
  # Ensure virtual environment is setup
  python3 -m venv "${VENV_DIR}"
  python3 -m venv "${VENV_DIR}" --upgrade --upgrade-deps

  # source the virtual environment
  # shellcheck source=./.venv/bin/activate
  source "${VENV_DIR}"/bin/activate

  # upgrade pi
  # shellcheck disable=SC2059 # Variables are formatting
  printf "\n${COLORS[BLUE]}%s${COLORS["NORMAL"]}\n" "Managing pip packages..."
  pip3 install --upgrade pip
  pip3 install -r "${SWD}"/requirements.txt
}
main "$@"

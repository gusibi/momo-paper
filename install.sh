#!/usr/bin/env bash
#
# Momo Paper — CLI install script
# Usage:
#   ./install.sh                  # Install to default location (~/.momo-paper)
#   ./install.sh --dir /opt/momo  # Install to custom directory
#   ./install.sh --check          # Check if momo CLI is installed and up to date
#   ./install.sh --upgrade        # Upgrade an existing installation
#   ./install.sh --uninstall      # Remove the installation
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/.momo-install.json"
ENGINE_DIR="${SCRIPT_DIR}/scripts/json-engine"
MIN_PYTHON="3.10"

# ---- helpers ----

red()    { printf "\033[31m%s\033[0m\n" "$*"; }
green()  { printf "\033[32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[33m%s\033[0m\n" "$*"; }
bold()   { printf "\033[1m%s\033[0m\n" "$*"; }

die() { red "✗ $*"; exit 1; }

check_python() {
    local py
    py="${1:-python3}"
    if ! command -v "$py" &>/dev/null; then
        die "Python not found ($py). Install Python >= $MIN_PYTHON first."
    fi
    local ver
    ver=$("$py" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local maj min
    maj=$("$py" -c "import sys; print(sys.version_info.major)")
    min=$("$py" -c "import sys; print(sys.version_info.minor)")
    local min_maj min_min
    min_maj="${MIN_PYTHON%%.*}"
    min_min="${MIN_PYTHON##*.}"
    if (( maj < min_maj )) || { (( maj == min_maj )) && (( min < min_min )); }; then
        die "Python $ver too old. Need >= $MIN_PYTHON."
    fi
    echo "$py"
}

find_python() {
    # Prefer the python that has momo installed, then python3, then python
    for candidate in python3 python; do
        if command -v "$candidate" &>/dev/null; then
            check_python "$candidate" && return 0
        fi
    done
    return 1
}

get_installed_version() {
    local momo_bin="${1:-momo}"
    if command -v "$momo_bin" &>/dev/null; then
        "$momo_bin" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1
    else
        echo ""
    fi
}

get_package_version() {
    # Read version from pyproject.toml
    grep -oE 'version\s*=\s*"[^"]*"' "${ENGINE_DIR}/pyproject.toml" 2>/dev/null \
        | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown"
}

# ---- config read / write ----

read_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        cat "$CONFIG_FILE"
    else
        echo "{}"
    fi
}

write_config() {
    local python_path="$1"
    local pkg_version="$2"
    local install_dir="$3"
    local install_date
    install_date="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

    cat > "$CONFIG_FILE" <<JSON
{
  "version": "${pkg_version}",
  "install_dir": "${install_dir}",
  "engine_dir": "${install_dir}/scripts/json-engine",
  "python": "${python_path}",
  "install_date": "${install_date}",
  "last_check": "${install_date}"
}
JSON
    green "✓ Config written: ${CONFIG_FILE}"
}

# ---- commands ----

cmd_check() {
    bold "Momo Paper — install check"
    echo ""

    # Load config
    local config
    config="$(read_config)"

    local install_dir
    install_dir="$(echo "$config" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('install_dir',''))" 2>/dev/null || echo "")"

    if [[ -n "$install_dir" ]]; then
        echo "  Config file : ${CONFIG_FILE}"
        echo "  Install dir  : ${install_dir}"
        echo "  Version      : $(echo "$config" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('version','unknown'))" 2>/dev/null || echo unknown)"
        echo "  Python       : $(echo "$config" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('python','unknown'))" 2>/dev/null || echo unknown)"
        echo "  Install date : $(echo "$config" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('install_date','unknown'))" 2>/dev/null || echo unknown)"
    else
        yellow "  No config file found at ${CONFIG_FILE}"
    fi

    echo ""

    local installed_ver
    installed_ver="$(get_installed_version momo)"
    if [[ -z "$installed_ver" ]]; then
        installed_ver="$(get_installed_version momo-paper)"
    fi

    local pkg_ver
    pkg_ver="$(get_package_version)"

    if [[ -z "$installed_ver" ]]; then
        red "  ✗ momo CLI not found on PATH"
        echo ""
        echo "  Run ./install.sh to install."
        return 1
    fi

    green "  ✓ momo CLI found (v${installed_ver})"

    if [[ "$installed_ver" != "$pkg_ver" ]]; then
        yellow "  ! Package version is ${pkg_ver} — consider: ./install.sh --upgrade"
    else
        green "  ✓ Up to date"
    fi

    echo ""
    echo "Try: momo list"
}

cmd_install() {
    local install_dir="${INSTALL_DIR:-$SCRIPT_DIR}"
    local python_path
    python_path="$(find_python)" || exit 1

    bold "Momo Paper — installing"
    echo ""
    echo "  Install dir : ${install_dir}"
    echo "  Engine dir  : ${install_dir}/scripts/json-engine"
    echo "  Python      : ${python_path} ($("$python_path" --version 2>&1))"
    echo ""

    # Create venv if not exists
    local venv_dir="${install_dir}/scripts/json-engine/.venv"
    if [[ ! -d "$venv_dir" ]]; then
        echo "Creating virtual environment..."
        "$python_path" -m venv "$venv_dir"
    fi

    # Activate and install
    local pip="${venv_dir}/bin/pip"
    local py="${venv_dir}/bin/python"

    if [[ ! -f "$pip" ]]; then
        die "pip not found in venv. Check virtual environment creation."
    fi

    echo "Installing momo-paper engine..."
    "$pip" install -e "${install_dir}/scripts/json-engine" --quiet

    # Get installed version
    local momo_bin="${venv_dir}/bin/momo"
    local pkg_ver
    pkg_ver="$("$py" -c "import importlib.metadata; print(importlib.metadata.version('momo-paper'))" 2>/dev/null || echo "unknown")"

    echo ""
    green "✓ momo-paper v${pkg_ver} installed"

    # Write config
    write_config "$py" "$pkg_ver" "$install_dir"

    # Symlink to /usr/local/bin for global access
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    bold "  To make 'momo' available globally, add to PATH:"
    echo ""
    echo "    export PATH=\"${venv_dir}/bin:\$PATH\""
    echo ""
    echo "  Or create a symlink:"
    echo "    sudo ln -sf ${momo_bin} /usr/local/bin/momo"
    echo ""
    echo "  Verify with: momo list"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    green "✓ Installation complete"
}

cmd_upgrade() {
    bold "Momo Paper — upgrading"
    echo ""

    local config
    config="$(read_config)"

    local install_dir
    install_dir="$(echo "$config" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('install_dir', ''))" 2>/dev/null || echo "")"
    if [[ -z "$install_dir" ]]; then
        yellow "No existing installation found. Running fresh install..."
        cmd_install
        return
    fi

    local venv_dir="${install_dir}/scripts/json-engine/.venv"
    local pip="${venv_dir}/bin/pip"
    local py="${venv_dir}/bin/python"

    if [[ ! -f "$pip" ]]; then
        yellow "Virtual environment not found. Running fresh install..."
        cmd_install
        return
    fi

    echo "Upgrading in ${install_dir}..."
    "$pip" install -e "${install_dir}/scripts/json-engine" --quiet --upgrade

    local pkg_ver
    pkg_ver="$("$py" -c "import importlib.metadata; print(importlib.metadata.version('momo-paper'))" 2>/dev/null || echo "unknown")"

    green "✓ Upgraded to v${pkg_ver}"

    # Update config
    local install_date
    install_date="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    cat > "$CONFIG_FILE" <<JSON
{
  "version": "${pkg_ver}",
  "install_dir": "${install_dir}",
  "engine_dir": "${install_dir}/scripts/json-engine",
  "python": "${py}",
  "install_date": "$(echo "$config" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('install_date',''))" 2>/dev/null || echo "$install_date")",
  "last_check": "${install_date}"
}
JSON
}

cmd_uninstall() {
    bold "Momo Paper — uninstalling"
    echo ""

    local config
    config="$(read_config)"
    local install_dir
    install_dir="$(echo "$config" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('install_dir',''))" 2>/dev/null || echo "")"

    if [[ -n "$install_dir" ]]; then
        local venv_dir="${install_dir}/scripts/json-engine/.venv"
        if [[ -d "$venv_dir" ]]; then
            echo "Removing virtual environment..."
            rm -rf "$venv_dir"
        fi
        yellow "Note: Engine source files in ${install_dir}/scripts/json-engine/ were not removed."
    fi

    if [[ -f "$CONFIG_FILE" ]]; then
        rm "$CONFIG_FILE"
        green "✓ Config file removed"
    fi

    green "✓ Uninstall complete"
}

# ---- main ----

INSTALL_DIR=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir)
            shift
            INSTALL_DIR="$1"
            ;;
        --check)
            cmd_check
            exit $?
            ;;
        --upgrade)
            cmd_upgrade
            exit $?
            ;;
        --uninstall)
            cmd_uninstall
            exit $?
            ;;
        -h|--help)
            echo "Momo Paper install script"
            echo ""
            echo "Usage:"
            echo "  ./install.sh              Install to repo directory"
            echo "  ./install.sh --dir DIR    Install to custom directory"
            echo "  ./install.sh --check      Check installation status"
            echo "  ./install.sh --upgrade    Upgrade to latest version"
            echo "  ./install.sh --uninstall  Remove installation"
            exit 0
            ;;
        *)
            die "Unknown option: $1"
            ;;
    esac
    shift
done

cmd_install

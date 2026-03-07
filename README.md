# Dice-Roller

A Python dice rolling application using standard [dice notation](https://en.wikipedia.org/wiki/Dice_notation).

## Usage

```
roll <dice code>
```

Supports standard dice notation with arithmetic:

```
$ roll 2d8 + d12 + 3
Total: 20
  d8: 3
  d8: 2
  d12: 12
```

Special modes:

| Command | Description |
|---|---|
| `roll stats` | Roll 4d6 drop-lowest six times (D&D 5e stat block) |
| `roll dir` | Pick a random compass direction |
| `roll -h` | Show usage help |

## Installation

### pip

```sh
pip install dice-roller
```

### Podman / Docker

Pull from Docker Hub and run with podman (rootless, no daemon required):

```sh
podman run --rm metasikander/dice-roller <dice code/stats/dir>
```

Or with Docker:

```sh
docker run --rm metasikander/dice-roller <dice code/stats/dir>
```

To build the image yourself (from the repo root):

```sh
# Using the build script (buildah + podman, fully rootless):
./container/build.sh

# Or manually with buildah:
buildah build -f container/Dockerfile -t dice-roller .

# Or with podman/docker:
podman build -f container/Dockerfile -t dice-roller .
```

The image is based on `python:3.13-alpine` (~46 MB) and runs as UID 65532
(non-root) at runtime.

### From source

```sh
git clone https://git.xirion.net/victor/dice-roller/
cd dice-roller
pip install --user .
```

### Arch Linux

Available on the AUR as [`dice-roller-git`](https://aur.archlinux.org/packages/dice-roller-git).

### YUM-based distros (Fedora / CentOS / RHEL)

```sh
# dnf
dnf localinstall RPM/packages/Dice-Roller-1.9-1.noarch.rpm

# yum
yum localinstall RPM/packages/Dice-Roller-1.9-1.noarch.rpm

# rpm
rpm -i RPM/packages/Dice-Roller-1.9-1.noarch.rpm
```

## Web Interface

A browser-based interface with a text field for dice notation, a direction button,
and a stats roll button. Requires Flask (installed via the `web` dependency group).

### Run locally

```sh
uv sync --group web
uv run python web/app.py
```

Then open <http://localhost:5000> in your browser.

### Run via Docker / Podman

```sh
# Build the web image
podman build -f container/Dockerfile.web -t dice-roller-web .

# Run (accessible on port 5000)
podman run --rm -p 5000:5000 dice-roller-web
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for environment management.

```sh
# Set up the dev environment
uv sync

# Install web dependencies too
uv sync --group web

# Run without installing
uv run python roll 2d8+6

# Run the web interface
uv run python web/app.py

# Lint / format / type-check
uv run flake8 roll
uv run black roll
uv run mypy roll

# Run tests
uv run pytest
```

## License

[GPL-3.0](LICENSE)

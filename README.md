# Dice-Roller

A python dice rolling application using standard [dice
notation](https://en.wikipedia.org/wiki/Dice_notation)

## Usage

    roll <dice code>

Example:

![](https://i.imgur.com/KKlSb49.png)

Instead of a dice code you can also put "stats" or "dir" for a stats
roll or direction roll respectively.

## Installation

### Pip install

**System-wide install** *(sudo)*

``` sh
pip install dice-roller
```

**User install** *(no sudo)*

``` sh
pip install --user dice-roller

# Add local 'pip' to PATH:
# (In your .bashrc, .zshrc etc)
export PATH="${PATH}:${HOME}/.local/bin/"
```

### Docker
The docker image has been pushed to docker hub, and you can get it by running:  
```
docker run metasikander/dice-roller <dice code/stats/dir>
```  
If you prefer to build the image yourself, enter the Docker-folder and run:  
```
docker build --tag=dice-roller .
```  

### Manual/Git install

``` sh
git clone https://git.xirion.net/victor/dice-roller/
cd dice-roller
pip3 install --user .

# Add local 'pip' to PATH:
# (In your .bashrc, .zshrc etc)
export PATH="${PATH}:${HOME}/.local/bin/"
```

#### Arch Linux

`dice-roller` is available on the AUR as `dice-roller-git`.

#### YUM-based distros (Fedora/CentOS/RHEL/++)
Enter the RPM/packages-folder and run one of these commands.

**On distros with yum:**  
```
yum localinstall Dice-Roller-1.9-1.noarch.rpm
```
**On distros with dnf:**
```
dnf localinstall Dice-Roller-1.9-1.noarch.rpm
```
**Use rpm instead:**
```
rpm -i Dice-Roller-1.9-1.noarch.rpm
```
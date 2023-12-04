# Check if Python 3 is installed
if type -P python3 >/dev/null 2>&1; then
  # Check if pip for Python3 is installed
  if pip3 --version; then
    # Check if git is installed
    if git --version; then
      # Go to the user's home directory
      cd /home/$USER/ || exit
      # Create installation path if it does not exist
      if ! [ -d ./.inwerk ]; then
        mkdir .inwerk
      fi
      if ! [ -d ./.inwerk/apps ]; then
        mkdir .inwerk/apps
      fi
      # Clone the repository if not already available and install requirements
      if ! [ -d ./.inwerk/apps/mysports-collector ]; then
        cd ./.inwerk/apps
        if git clone https://github.com/inwerk/mysports-collector.git mysports-collector; then
          pip3 install -r ./mysports-collector/requirements.txt || exit
        fi
      # Update the repository if already available and install requirements
      elif [ -d ./.inwerk/apps/mysports-collector ]; then
        cd ./.inwerk/apps/mysports-collector
        if git pull; then
          if [ -f ./requirements.txt ]; then
            pip3 install -r ./requirements.txt || exit
          else
        	  if wget https://raw.githubusercontent.com/inwerk/mysports-collector/master/requirements.txt; then
        	    pip3 install -r ./requirements.txt || exit
        	  fi
          fi
        fi
      fi
      # Go to the user's home directory
      cd /home/$USER/
      # Add alias if it does not exist
      if ! grep -q 'if \[ -d ~/\.inwerk/apps/mysports-collector \]; then alias gymstalker="python3 /home/\$USER/\.inwerk/apps/mysports-collector/src/cli\.py"; fi' ~/.bashrc; then
        printf '\nif [ -d ~/.inwerk/apps/mysports-collector ]; then alias gymstalker="python3 /home/$USER/.inwerk/apps/mysports-collector/src/cli.py"; fi\n' >> ~/.bashrc
      fi
      # Feedback
      echo "https://github.com/inwerk/mysports-collector successfully installed!"
      echo "Enter »gymstalker --help« for help."
      # Reload terminal
      exec "$BASH"
    # Git is not installed
    else
      # Error message
      echo "Git is not installed. Please install git on your machine."
    fi
  # pip3 for Python 3 is not installed
  else
    # Error message
    echo "pip for Python 3 is not installed. Please install pip for Python 3 on your machine."
  fi
# Python 3 is not installed
else
  # Error message
  echo "Python3 is not installed. Please install Python3 on your machine."
fi
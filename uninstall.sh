# Go to the user's home directory
cd /home/$USER/
# Stop the application and remove alias from bashrc
if grep -q 'if \[ -d ~/\.inwerk/apps/mysports-collector \]; then alias gymstalker="python3 /home/\$USER/\.inwerk/apps/mysports-collector/src/cli\.py"; fi' ~/.bashrc; then
  if [ -f ./inwerk/mysports-collector/cli.py ]; then
    gymstalker stop
  fi
  sed -i 's,if \[ -d ~/\.inwerk/apps/mysports-collector \]; then alias gymstalker="python3 /home/\$USER/\.inwerk/apps/mysports-collector/src/cli\.py"; fi,,g' ~/.bashrc
fi
# Remove repository
if [ -d ./.inwerk/apps/mysports-collector ]; then
  rm -r ~/.inwerk/apps/mysports-collector
fi
# Remove app directory if empty
if [ -z "$(ls -A ~/.inwerk/apps)" ]; then
  rm -r ~/.inwerk/apps
fi
# Remove inwerk directory if empty
if [ -z "$(ls -A ~/.inwerk)" ]; then
  rm -r ~/.inwerk
fi
# Feedback
echo "https://github.com/inwerk/mysports-collector successfully removed from this system!"
# Reload terminal
exec "$BASH"
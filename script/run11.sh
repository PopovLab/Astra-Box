#export DISPLAY=$(ip route list default | awk '{print $3}'):0
INTEL=~/intel/oneapi/setvars.sh
if [ -f "$INTEL" ]; then
    echo "$INTEL exists."
else 
    echo "$INTEL does not exist."
    INTEL=/opt/intel/oneapi/setvars.sh
fi
source $INTEL
echo 'clear folder:' $1/dat/
rm $1/dat/* 
rm $1/lhcd/out/*
rm $1/lhcd/distribution/*
echo 'run astra' $1 $2 $3
$1/.exe/astra  $2 $3 
read -p "Press enter to continue"